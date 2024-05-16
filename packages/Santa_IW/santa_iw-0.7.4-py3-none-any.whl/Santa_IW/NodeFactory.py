from collections import ChainMap
from pathlib import Path
from typing import Any

from libsrg.Config import Config

from Santa_IW.Node import Node
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly
from Santa_IW.TemplateFactory import TemplateFactory
from Santa_IW.TestBase import TestBase
from Santa_IW.TestFactory import TestFactory
from Santa_IW.Utils import log_entry_and_exit


class NodeFactory(Subassembly):
    """
    Factory for creating Nodes from json data.

    """

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        # self.logger.info(map_chain_as_str(self.args))
        self.node_dict: dict[str, Any] = {}

    def start(self) -> None:
        self.set_annotation("Loading Nodes...")
        self.log_internal_status(Status.OK, "Started", assess=True)
        # self.logger.info("Started")
        # self.logger.info(map_chain_as_str(self.args))
        tf: TestFactory = self.config().get_item("test_factory")
        tpf: TemplateFactory = self.config().get_item("template_factory")
        node_dirs: list[str] = self.config().get_item("node_dirs")
        for node_dir in node_dirs:
            dpath = Path(node_dir).resolve()
            self.process_node_subdir(dpath, group_below=self.tree_root_subassembly, tf=tf, tpf=tpf)

        self.set_annotation("Done")
        self.log_internal_status(Status.OK, message=f"Loaded {len(self.node_dict)} nodes", assess=True)
        # self.logger.info("Finished")

    def process_node_subdir(self, dpath, group_below: Subassembly, tf: TestFactory, tpf: TemplateFactory):
        if not dpath.is_dir():
            self.log_internal_status(Status.OK, f"Not a directory: {dpath} for group below {group_below.name()}", assess=True)
        else:
            self.log_internal_status(Status.OK, f"Looking in {dpath} for group below {group_below.name()}", assess=True)
            # first pass (group_pass=True) we are looking for special __file
            for group_pass in [True, False]:
                count_in_pass = 0
                for node_file in dpath.glob("*.json"):
                    special = node_file.stem.startswith("__")
                    if group_pass != special:
                        continue
                    self.logger.info(f"loading {node_file}")
                    # noinspection PyBroadException
                    try:
                        data = Config(node_file)
                        data["__LOADED_FROM__"] = str(node_file)
                    except Exception as e:
                        msg = f"Error parsing {node_file} {e}"
                        self.log_internal_status(Status.CRITICAL, msg)
                        self.logger.exception(msg, stack_info=True, exc_info=True)
                        continue
                    if int(data.get_item("register", default=1)) == 0:
                        self.logger.info(f"node not registered {node_file} to {data}")
                        continue
                    if group_pass:
                        count_in_pass += 1
                        if count_in_pass > 1:
                            msg = f"More than one special node file in directory {node_file}"
                            self.logger.info(msg)
                            self.log_internal_status(Status.CRITICAL, msg, assess=True)
                            raise Exception(msg)
                        if "group_below" in data:
                            group_below = data["group_below"]
                    self.logger.info(f"parsed {node_file} to {data} below {group_below.name()}")
                    tpf.apply_templates(data)
                    short_name = data.get_item("short_name")
                    self.log_internal_status(Status.OK, f"Creating node {short_name} below {group_below.name()}")
                    node = Node(instance_config=data, short_name=short_name, parent=group_below)
                    self.node_dict[short_name] = node
                    if group_pass:
                        group_below = node
                    tf.create_tests_for_node(node, data)
            # all files in this directory processed, examine sub_dirs
            for subdir in dpath.iterdir():
                if not subdir.is_dir():
                    continue
                self.process_node_subdir(subdir, group_below, tf=tf, tpf=tpf)

    def start_nodes(self):
        self.logger.info(self.node_dict)
        for node in self.node_dict.values():
            self.logger.info(f"Starting {node}")
            node.start()

    @log_entry_and_exit
    def create(self, node_args: ChainMap[str, Any], test_args: dict[str, Any]) -> TestBase:
        name = test_args["test_type"]
        test_class = self.node_dict[name]
        test = test_class(node_args, test_args)
        return test
