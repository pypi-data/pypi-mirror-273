from typing import Type

from libsrg.Config import Config

from Santa_IW.Node import Node
from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import TestBase


class TestType(Node):
    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly,
                 test_class: Type[TestBase]) -> None:
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name,sw_node=True)  # super defines self.logger
        self._test_class = test_class
        self._pull_up_child_annotation = True

    def get_test_class(self) -> Type[TestBase]:
        return self._test_class
