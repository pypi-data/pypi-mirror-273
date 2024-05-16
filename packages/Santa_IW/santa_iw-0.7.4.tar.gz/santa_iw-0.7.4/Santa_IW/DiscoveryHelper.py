import logging
from typing import Type, Optional, Any

from libsrg.Config import Config

from Santa_IW.PluginBase import PluginBase
from Santa_IW.TestBase import TestBase


class DiscoveryHelper:
    def __init__(self, loaded_class: Type[TestBase] | Type[PluginBase]):
        self.logger = logging.getLogger(__name__)
        self._loaded_class = loaded_class
        self._aliases: list[str] = []
        self._configs: dict[str, Config] = {}

    def alias(self, name: str, config: Optional[dict[str, Any] | Config] = None, **overrides) -> Config:
        """
        Allows TestFactory to create a test_type which can create a new instance of the test class with supplied config.
        Config is copied before storing it, so changes do not affect other test_types.
        Any overrides given will change the config defaults.

        :param name: The name of the "test_type" created
        :param config: The default configuration settings for the test_type
        :param overrides: zero or more changes to the config as passed in
        :return: A copy of the default configuration, including overrides
        """
        self._aliases.append(name)
        new_config = Config(config) if config is not None else Config({})
        self._configs[name] = new_config
        for k, v in overrides.items():
            new_config[k] = v

        return new_config.copy()

    def get_all_configs(self) -> dict[str, Config]:
        if not self._aliases:
            self.alias(self._loaded_class.__name__, {})
        return self._configs

    def get_loaded_class(self) -> Type[TestBase] | Type[PluginBase]:
        return self._loaded_class
