import importlib
import importlib.util
import sys
from collections import Counter
from pathlib import Path
from typing import List, Type, Any

from libsrg.Config import Config

from Santa_IW.Node import Node
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import TestBase
from Santa_IW.TestType import TestType


# noinspection DuplicatedCode
class TestFactory(Subassembly):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        self.test_class_map: dict[str, Any] = {}
        self.test_type_map: dict[str, TestType] = {}
        self.test_instance_map: dict[str, TestBase] = {}
        self.tests_names_not_found: set[str] = set()
        # failure within a test type does not imply factory failure
        self._propagate_child_stats_in_overall = False
        self.test_used_by: dict[str, set[str]] = {}

    def start(self) -> None:
        self.set_annotation("Loading Test Classes...")
        self.log_internal_status(Status.OK, "Started", assess=True)
        test_dirs = self.config().get_item("test_modules_dirs")
        for test_dir in test_dirs:
            dpath = Path(test_dir).resolve()
            if not dpath.is_dir():
                self.log_internal_status(Status.WARNING, f"{dpath} is not a directory", assess=True)
            else:
                self.log_internal_status(Status.OK,f"Loading tests from {dpath}...", assess=True)
                for testfile in dpath.glob("*.py"):
                    file_name = testfile.stem
                    # problem with __init__.py
                    if file_name.startswith("_"):
                        continue
                    # noinspection PyBroadException
                    try:
                        self.load_testfile(testfile)
                    except Exception as e:
                        self.logger.exception(e, stack_info=True, exc_info=True)
                        self.log_internal_status(Status.CRITICAL, f"Failed to load test file {testfile} {e}",
                                                 assess=True)

        self.set_annotation("Done")
        self.log_internal_status(Status.OK, message=f"Loaded {len(self.test_type_map)} test types and {len(self.test_instance_map)} test instances", assess=True)
        self.logger.info("Finished")

    def spawn(self):
        # no new thread, but update status
        self.log_internal_status(Status.OK, message=f"Loaded {len(self.test_class_map)} Test Classes, {len(self.test_type_map)} Test Types, and {len(self.test_instance_map)} Test Instances", assess=True)


    def load_testfile(self, testfile):
        self.logger.info(f"Loading {testfile!s}")
        module_name = testfile.stem
        file_path = str(testfile)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        helper = module.helper
        test_class = helper.get_loaded_class()
        all_configs = helper.get_all_configs()
        self.logger.info(f"{file_path} supports DiscoveryHelper")
        self.test_class_map[module_name]= file_path
        test_types = self.config().get_item("test_types")
        for alias, config in all_configs.items():
            test_type: TestType = TestType(instance_config=config, parent=test_types, short_name=alias,
                                           test_class=test_class)
            self.test_used_by[alias] = set()
            self.test_type_map[alias] = test_type

    def create_one_test(self, node: Node, test_args: Config, short: str) -> None:
        name = test_args["test_type"]
        if name in self.test_type_map:
            test_type: TestType = self.test_type_map[name]
            test_class: Type[TestBase] = test_type.get_test_class()
            stepparent: TestType = test_type
            self.test_used_by[name] |= {node.short_name()}
            try:
                self.logger.info("About to create test type {name} for {node.name()}")
                test: TestBase = test_class(instance_config=test_args, short_name=short, parent=node,
                                            stepparent=stepparent)
                self.logger.info("About to save test type {name} for {node.name()}")
                self.test_instance_map[test.name()] = test
                # self.log_internal_status(Status.OK, f"created {test.name()}", assess=True)

            except Exception as e:
                self.logger.exception(f"constructor {name} failed for {test_args}\n{e}", stack_info=True, exc_info=True)
                test_type.log_internal_status(Status.CRITICAL, f"constructor failed {name} {short}", assess=True)
        else:
            self.logger.error(f"test_class {name} not found")
            self.tests_names_not_found |= {name}
            self.log_internal_status(Status.WARNING, f"no test class {name}", assess=True)

    def get_test(self, name: str) -> TestBase:
        return self.test_instance_map[name]

    def get_all_tests(self) -> List[TestBase]:
        return sorted(list(self.test_instance_map.values()))

    def report_all_tests(self) -> str:
        return self.report()

    def report(self) -> str:

        out = super().report()
        out += "\n"
        all_tests = self.get_all_tests()
        out += f"There are {len(all_tests)} instances of {len(self.test_type_map)} test types\n"
        if self.tests_names_not_found:
            out += f"\nThere are {len(self.tests_names_not_found)} test class names not found:\n"
            for test in self.tests_names_not_found:
                out += f"  {test}\n"

        out += f"\n\nTest Alias -> Module.Class :\n"
        for k, v in self.test_type_map.items():
            tc:Type[TestBase] = v.get_test_class()
            out += f"\t{k:<30} -> {tc.__module__}.{tc.__name__}\n"

        out += "\nTest Alias Usage:\n"
        names: list[str] = list(self.test_used_by.keys())
        names.sort()
        for name in names:
            val = self.test_used_by[name]
            if len(val) != 0:
                out += f"\t{name}: {val}\n"
        out += "\nTest Alias Not Used:\n"
        for name in names:
            val = self.test_used_by[name]
            if len(val) == 0:
                out += f"\t{name}\n"
        return out

    def create_tests_for_node(self, node: Node, data: Config) -> None:
        test_args: list[Config] = [Config(ti) for ti in data["tests"]]
        dup_counter = Counter()
        test_sep = self.config().get_item("tree_test_separator")
        # first pass determines short name and counts duplicate names within same node

        for test_info in test_args:
            if int(test_info.get_item("register", default=1)) > 0:
                test_class = test_info["test_type"]
                name = test_info.get_item("instance_name", "name", "copy", default="")
                short: str = test_class + test_sep + name
                if short.startswith("Check"):
                    short = short.replace("Check", "", 1)
                test_info["short_name"] = short
                dup_counter[short] += 1
        instance_counter = Counter()
        # second pass adds numeric suffix where first pass found duplicates
        # then constructs test
        for test_info in test_args:
            reg = int(test_info.get_item("register", default=1)) > 0
            if reg:
                short = test_info["short_name"]
                if dup_counter[short] > 1:
                    n = instance_counter[short]
                    instance_counter[short] += 1
                    if not short.endswith(test_sep):
                        short += "_"
                    short += f"{n:02d}"
                self.create_one_test(node=node, test_args=test_info, short=short)
        if self.tests_names_not_found:
            msg = f"{len(self.tests_names_not_found)} Test Classes not found "
            self.log_internal_status(Status.WARNING, msg)
