import importlib
import importlib.util
import sys
from pathlib import Path
from typing import List, Type

from libsrg.Config import Config

from Santa_IW.PluginBase import PluginBase
from Santa_IW.PluginType import PluginType
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly


# noinspection DuplicatedCode
class PluginFactory(Subassembly):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        self.plugin_type_map: dict[str, PluginType] = {}
        self.plugin_instance_map: dict[str, PluginBase] = {}
        self.plugin_names_not_found: set[str] = set()
        # failure within a test type does not imply factory failure
        self._propagate_child_stats_in_overall = False

    def start(self) -> None:
        self.scan_plugin_classes()
        self.scan_plugin_configs()
        self.log_internal_status(Status.OK,
                                 message=f"Loaded {len(self.plugin_type_map)} Plugin Types and {len(self.plugin_instance_map)} Plugin Instances",
                                 assess=True)

    def scan_plugin_classes(self):
        self.set_annotation("Loading Plugin Classes...")
        self.log_internal_status(Status.OK, "Started", assess=True)
        module_dirs = self.config().get_item("plugin_modules_dirs")
        for module_dir in module_dirs:
            dpath = Path(module_dir).resolve()
            if not dpath.is_dir():
                self.log_internal_status(Status.WARNING, f"{dpath} is not a directory", assess=True)
            else:
                self.log_internal_status(Status.OK, f"Looking in {dpath}", assess=True)
                for module_file in dpath.glob("*.py"):
                    file_name = module_file.stem
                    # problem with __init__.py
                    if file_name.startswith("_"):
                        continue
                    # noinspection PyBroadException
                    try:
                        self.load_module_file(module_file)
                    except Exception as e:
                        self.logger.exception(e, stack_info=True, exc_info=True)
                        self.log_internal_status(Status.CRITICAL, f"Failed to load test file {module_file} {e}",
                                                 assess=True)

    def load_module_file(self, module_file):
        self.logger.info(f"Loading {module_file!s}")
        module_name = module_file.stem
        file_path = str(module_file)
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        # noinspection PyBroadException
        helper = module.plugin_helper
        plugin_class = helper.get_loaded_class()
        all_configs = helper.get_all_configs()
        self.logger.info(f"{file_path} supports DiscoveryHelper")
        module_types_parent = self
        for alias, config in all_configs.items():
            plugin_type: PluginType = PluginType(instance_config=config, parent=module_types_parent, short_name=alias,
                                                 plugin_class=plugin_class)
            self.plugin_type_map[alias] = plugin_type

    def create_plugin_instance(self, plugin_args: Config) -> None:
        name = plugin_args.get_item("plugin_type")
        short = plugin_args.get_item("short_name")
        if name in self.plugin_type_map:
            plugin_type: PluginType = self.plugin_type_map[name]
            plugin_class: Type[PluginBase] = plugin_type.get_plugin_class()

            try:
                self.logger.info("About to create plugin instance {name}")
                plugin: PluginBase = plugin_class(instance_config=plugin_args, short_name=short, parent=plugin_type)
                self.logger.info("About to save plugin type {name}")
                self.plugin_instance_map[plugin.name()] = plugin
                # self.log_internal_status(Status.OK, f"created {test.name()}", assess=True)
            except Exception as e:
                self.logger.exception(f"constructor {name} failed for {plugin_args}\n{e}", stack_info=True,
                                      exc_info=True)
                plugin_type.log_internal_status(Status.CRITICAL, f"constructor failed {name} {short}", assess=True)
        else:
            self.logger.error(f"plugin {name} not found")
            self.plugin_names_not_found |= {name}
            self.log_internal_status(Status.WARNING, f"no plugin class {name}", assess=True)

    def get_all_plugins(self) -> List[PluginBase]:
        return sorted(list(self.plugin_instance_map.values()))

    def report_all_plugins(self) -> str:
        return self.report()

    def report(self) -> str:

        out = super().report()
        out += "\n"
        all_plugins = self.get_all_plugins()
        out += f"There are {len(all_plugins)} instances of {len(self.plugin_type_map)} plugin types\n"
        if self.plugin_names_not_found:
            out += f"\nThere are {len(self.plugin_names_not_found)} plugin class names not found:\n"
            for missing in self.plugin_names_not_found:
                out += f"  {missing}\n"

        out += f"\n\nPlugin classes defined:\n"
        for k, v in self.plugin_type_map.items():
            out += f"  {k:<30} {str(v.get_plugin_class())}\n"

        # out += "\n\nTest Statistics"
        # for test in all_tests:
        #     out += test.report()
        #     out += "------\n"
        return out

    def scan_plugin_configs(self):
        self.set_annotation("Loading Plugin Configs...")
        self.log_internal_status(Status.OK, "Started Plugin Configs", assess=True)
        config_dirs = self.config().get_item("plugin_config_dirs")
        for config_dir in config_dirs:
            dpath = Path(config_dir).resolve()
            self.logger.info(f"Looking in {dpath}")
            if dpath.is_dir():
                for config_file in dpath.glob("*.json"):
                    # noinspection PyBroadException
                    try:
                        mod_config = Config(config_file)
                        self.create_plugin_instance(plugin_args=mod_config)
                    except Exception as e:
                        self.logger.exception(e, stack_info=True, exc_info=True)
                        self.log_internal_status(Status.CRITICAL,
                                                 f"Failed to load plugin config file {config_file} {e}",
                                                 assess=True)
