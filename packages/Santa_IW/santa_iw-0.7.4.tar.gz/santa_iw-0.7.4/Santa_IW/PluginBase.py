from abc import ABC

from libsrg.Config import Config

from Santa_IW.Subassembly import Subassembly


class PluginBase(Subassembly, ABC):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger

        # fetch the usual suspects
        self.fqdn = self.config().get_item("fqdn", )
        self.userat = self.config().get_item("userat")
