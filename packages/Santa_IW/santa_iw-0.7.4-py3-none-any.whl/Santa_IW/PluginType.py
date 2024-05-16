from typing import Type

from libsrg.Config import Config

from Santa_IW.Node import Node
from Santa_IW.PluginBase import PluginBase
from Santa_IW.Subassembly import Subassembly


class PluginType(Node):
    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly,
                 plugin_class: Type[PluginBase]) -> None:
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name, sw_node=True)  # super defines self.logger
        self._plugin_class = plugin_class
        self._pull_up_child_annotation = True

    def get_plugin_class(self) -> Type[PluginBase]:
        return self._plugin_class
