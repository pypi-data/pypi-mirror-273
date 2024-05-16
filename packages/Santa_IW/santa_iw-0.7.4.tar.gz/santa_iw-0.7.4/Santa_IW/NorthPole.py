import shutil
from pathlib import Path


class NorthPole:
    """
    This class locates the directory tree for Santa_IW and generates a set of paths to key directories and files.

    It gets the file path to the NorthPole module
    From there up 1 is the Santa_IW package directory __SETUP_SANTA_PACKAGE_DIR__
    From there up 1 is the santa_is_watching repo clone directory __SETUP_CLONE_DIR__
    From there up 1 is the Santa_IW main directory, __SETUP_OPT_DIR__

    Everything else gets located somewhere south of __SETUP_OPT_DIR__

    Instance member variables are Path's

    The dictionary produced has string values for the paths.
    """

    def __init__(self):
        my_file = __file__

        # We will fill this as we go
        self.paths: dict[str, Path] = dict()

        # __SETUP_*__ dirs are created by SantaSetup (not SantaSetupInner)
        # this module lives below these directories, so they are assumed to exist already
        self.santa_package_dir = Path(my_file).parent  # locate Santa_IW module directory
        self.paths["__SETUP_SANTA_PACKAGE_DIR__"] = self.santa_package_dir
        self.santa_clone_dir = self.santa_package_dir.parent  # where santa_is_watching was cloned
        self.paths["__SETUP_CLONE_DIR__"] = self.santa_clone_dir
        self.santa_opt_dir = self.santa_clone_dir.parent
        self.paths["__SETUP_OPT_DIR__"] = self.santa_opt_dir

        # __SANTA_*__ dirs are created by SantaSetupInner
        self.santa_logs_dir = self.santa_opt_dir / "LOGS"
        self.paths["__SANTA_LOGS_DIR__"] = self.santa_logs_dir
        self.santa_db_dir = self.santa_opt_dir / "DB"
        self.paths["__SANTA_DB_DIR__"] = self.santa_db_dir
        self.santa_secrets_dir = self.santa_opt_dir / "SECRETS"
        self.paths["__SANTA_SECRETS_DIR__"] = self.santa_secrets_dir

        # __USER_*__ dirs are created by SantaSetupInner
        self.santa_user_config_dir = self.santa_opt_dir / "USER_CONFIG"
        self.paths["__USER_CONFIG_DIR__"] = self.santa_user_config_dir
        self.santa_user_nodes_dir = self.santa_user_config_dir / "NODES"
        self.paths["__USER_NODES_DIR__"] = self.santa_user_nodes_dir
        self.santa_user_plugin_modules_dir = self.santa_user_config_dir / "PLUGIN_MODULES"
        self.paths["__USER_PLUGIN_MODULES_DIR__"] = self.santa_user_plugin_modules_dir
        self.santa_user_plugin_config_dir = self.santa_user_config_dir / "PLUGIN_CONFIG"
        self.paths["__USER_PLUGIN_CONFIG_DIR__"] = self.santa_user_plugin_config_dir
        self.santa_user_test_modules_dir = self.santa_user_config_dir / "TEST_MODULES"
        self.paths["__USER_TEST_MODULES_DIR__"] = self.santa_user_test_modules_dir
        self.santa_user_templates_dir = self.santa_user_config_dir / "TEMPLATES"
        self.paths["__USER_TEMPLATES_DIR__"] = self.santa_user_templates_dir

        # __DISCOVERY_*__ dirs are created by NetworkDiscovery
        self.santa_discovery_config_dir = self.santa_opt_dir / "DISCOVERY_CONFIG"
        self.paths["__DISCOVERY_CONFIG_DIR__"] = self.santa_discovery_config_dir
        self.santa_discovery_nodes_dir = self.santa_discovery_config_dir / "NODES"
        self.paths["__DISCOVERY_NODES_DIR__"] = self.santa_discovery_nodes_dir
        self.santa_discovery_plugin_config_dir = self.santa_discovery_config_dir / "PLUGIN_CONFIG"
        self.paths["__DISCOVERY_PLUGIN_CONFIG_DIR__"] = self.santa_discovery_plugin_config_dir
        self.santa_discovery_templates_dir = self.santa_discovery_config_dir / "TEMPLATES"
        self.paths["__DISCOVERY_TEMPLATES_DIR__"] = self.santa_discovery_templates_dir
        # discovery does not need  TEST_MODULES or PLUGIN_MODULES directories


        # __INSTALL_*__ dirs are created by cloning the repo
        # modules are one level above INSTALL_CONFIG
        self.santa_install_config_dir = self.santa_package_dir / "INSTALL_CONFIG"
        self.paths["__INSTALL_CONFIG_DIR__"] = self.santa_install_config_dir
        self.santa_install_nodes_dir = self.santa_install_config_dir / "NODES"
        self.paths["__INSTALL_NODES_DIR__"] = self.santa_install_nodes_dir
        self.santa_install_plugin_modules_dir = self.santa_package_dir / "PLUGIN_MODULES"
        self.paths["__INSTALL_PLUGIN_MODULES_DIR__"] = self.santa_install_plugin_modules_dir
        self.santa_install_plugin_config_dir = self.santa_install_config_dir / "PLUGIN_CONFIG"
        self.paths["__INSTALL_PLUGIN_CONFIG_DIR__"] = self.santa_install_plugin_config_dir
        self.santa_install_test_modules_dir = self.santa_package_dir / "TEST_MODULES"
        self.paths["__INSTALL_TEST_MODULES_DIR__"] = self.santa_install_test_modules_dir
        self.santa_install_templates_dir = self.santa_install_config_dir / "TEMPLATES"
        self.paths["__INSTALL_TEMPLATES_DIR__"] = self.santa_install_templates_dir

        # special file paths ##################################################################
        # setup_defaults_file must agree with SantaSetup.py
        self.setup_defaults_file = self.santa_opt_dir / 'setup_defaults.json'
        self.paths["__SETUP_DEFAULTS_FILE__"] = self.setup_defaults_file

        self.user_discovery_file = self.santa_user_config_dir / 'discovery.json'
        self.paths["__USER_DISCOVERY_FILE__"] = self.user_discovery_file

        self.user_runtime_file = self.santa_user_config_dir / 'runtime.json'
        self.paths["__USER_RUNTIME_FILE__"] = self.user_discovery_file

        self.default_runtime_file = self.santa_install_config_dir / 'runtime_defaults.json'
        self.paths["__INSTALL_RUNTIME_FILE__"] = self.default_runtime_file

        self.pyproject_toml_file = self.santa_clone_dir / 'pyproject.toml'
        self.paths["__PYPROJECT_TOML_FILE__"] = self.pyproject_toml_file

        # these just get copied in setup, no need to show up in config files
        self.prototype_discovery_file = self.santa_install_config_dir / 'prototype_discovery.json'
        self.prototype_gnas_discovery_file = self.santa_install_config_dir / 'prototype_gnas_discovery.json'
        self.prototype_runtime_file = self.santa_install_config_dir / 'prototype_runtime.json'

    def as_dict(self) -> dict[str, str]:
        dct = {k: str(v) for k, v in self.paths.items()}
        return dct

    def create_santa_dirs(self):
        for k, v in self.paths.items():
            if k.startswith('__SANTA_') and k.endswith("_DIR__"):
                v.mkdir(parents=True, exist_ok=True, mode=0o700)

    def create_user_dirs(self):
        for k, v in self.paths.items():
            if k.startswith('__USER_') and k.endswith("_DIR__"):
                v.mkdir(parents=True, exist_ok=True, mode=0o700)

    def create_discovery_dirs(self):
        for k, v in self.paths.items():
            if k.startswith('__DISCOVERY_') and k.endswith("_DIR__"):
                v.mkdir(parents=True, exist_ok=True, mode=0o700)

    def rotate_out_discovery_dir(self):
        """
        This empties out the current discovery directory. A rolling history of
        prior settings is maintained.

        """
        self.rotate_out_file(self.santa_discovery_config_dir)

    def rotate_out_file(self, path: Path, depth: int = 0, keep_num: int = 8) -> Path:
        """
        Rotates out the current file/directory at path. A rolling history is maintained.
        User would normally call this with just the path and optionally keep_num
        :param path: Path to the file (with no rotation number)
        :param depth: How deep in the rotation are we, default is 0
        :param keep_num: Number of levels to retain in rotation, default is 8
        :return: Path to where the file *was* before rotation

        """
        old = Path(f"{path}_{depth}") if depth > 0 else path
        if old.exists():
            if depth < keep_num:
                nxt = self.rotate_out_file(path=path, depth=depth + 1, keep_num=keep_num)
            else:
                nxt = Path(f"{path}_{depth + 1}")
                print(f"Removing {nxt}")
                shutil.rmtree(nxt)
            print(f"Rotating {old} to {nxt}")
            shutil.move(old, nxt)
        return old
