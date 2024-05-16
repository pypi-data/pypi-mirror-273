import argparse
import atexit
import logging
import logging.config
import os
import pprint

try:
    import tomllib
except ImportError:
    tomllib = None

import libsrg.LoggingCounter
from libsrg.Config import Config
from libsrg.Info import Info
from libsrg.LoggingCounter import LoggingCounter

from Santa_IW.TreeRoot import TreeRoot
from Santa_IW.NorthPole import NorthPole


class Main:
    """
    Main starts up the application by:
    - Initializing the logger
    - Parsing the command line
    - Instantiating TreeRoot with args
    - Passing control to the TreeRoot

    TreeRoot will be the overall control class for this application.
    It is a singleton and all application objects will be discoverable from there.

    """

    def __init__(self):

        """ Initializing the santa application """
        self.np = NorthPole()
        np = self.np

        parser_args = {}
        self.parser = argparse.ArgumentParser(**parser_args)
        self.parser.add_argument("--level", help="Logging level at santa.log", action='store',
                                 choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")
        self.parser.add_argument("--console", help="Logging level at console (stderr)", action='store',
                                 choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="ERROR")

        self.args = self.parser.parse_args()

        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "detailed": {
                    "format": "%(asctime)s %(levelname)-8s %(lineno)4d %(name) 20s.%(funcName)-22s -- %(message)s"
                }
            },
            "handlers": {

                "counter": {
                    "class": "libsrg.LoggingCounter.LoggingCounter",
                    "level": "DEBUG",
                    "formatter": "detailed",
                },
                "stderr": {
                    "class": "logging.StreamHandler",
                    "level": self.args.console.upper(),
                    "formatter": "detailed",
                    "stream": "ext://sys.stderr"
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": self.args.level.upper(),
                    "formatter": "detailed",
                    "filename": np.santa_logs_dir / "santa.log",
                    "maxBytes": 100_000_000,
                    "backupCount": 5,
                    "mode": "a"
                }
            },
            "root": {
                "level": "DEBUG",
                "handlers": [
                    "stderr",
                    "file",
                    "counter"
                ]
            }
        }
        logging.config.dictConfig(log_config)
        self.logger = logging.getLogger(self.__class__.__name__)
        atexit.register(libsrg.LoggingCounter.LoggingCounter.log_counters)

        # any major issues here are assumed fatal
        # no heroics, but I do want to log what happens (as soon as logging is running).
        self.exit_counter = 0
        try:
            self.logger.info(pprint.pformat(self.np.as_dict()))
            startup_config = Config(np.setup_defaults_file, np.as_dict())

            if tomllib:
                with open(np.pyproject_toml_file, 'rb') as fp:
                    toml_dict = tomllib.load(fp)
                version = toml_dict["tool"]["poetry"]["version"]
            else:
                version = "0.0.0"
            startup_config["SANTA_IW_VERSION"] = version

            # Get localhost info
            localhost_info = Info()
            localhost_config = localhost_info.to_config("localhost_")
            localhost_config.set_item("localhost_is_root", os.geteuid() == 0)
            localhost_config.set_item("fqdn", localhost_info.fqdn)

            # load the defaults file
            defaults_config = Config(np.default_runtime_file, localhost_config, startup_config)

            # noinspection PyUnboundLocalVariable
            primary_config = Config(np.user_runtime_file, defaults_config)

            self.tree_root = TreeRoot(primary_config)
            self.tree_root.start()
            LoggingCounter.rotate_files()
            exit(0)

        except Exception as e:
            self.logger.exception(f"Fatal: {type(e)} {e}", stack_info=True, exc_info=True)
            exit(1)


def main():
    _ = Main()


if __name__ == '__main__':
    main()
