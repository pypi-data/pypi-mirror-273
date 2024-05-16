import os
from threading import Thread

from libsrg.Config import Config

from Santa_IW.DataRecording import DataRecording
from Santa_IW.Discovery import Discovery
from Santa_IW.Flask.WebGUI import WebGUI
from Santa_IW.Naughty import Naughty
from Santa_IW.Node import Node
from Santa_IW.NodeFactory import NodeFactory
from Santa_IW.PluginFactory import PluginFactory
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly
from Santa_IW.TemplateFactory import TemplateFactory
from Santa_IW.TestFactory import TestFactory


class TreeRoot(Subassembly):
    """
    TreeRoot class is the top level class that instantiates all classes beyond the basic command line parser.

    TreeRoot was previously named Monitor.
    """

    def __init__(self, cli_args: Config):
        self._my_thread = None
        tree_root_name = cli_args.get('tree_root_name')

        super().__init__(parent=None, short_name=tree_root_name,
                         instance_config=cli_args)  # super defines self.logger

        tree_app_name = cli_args.get('tree_app_name')
        sw_args0: Config = Config({})
        sw_args: Config = Config({"propagate_child_status_in_overall": False})
        self.sw_subsystems = Node(instance_config=sw_args0, short_name=tree_app_name, parent=self, sw_node=True)

        self.data_recording = DataRecording(parent=self.sw_subsystems, short_name="DataRecording",
                                            instance_config=sw_args)

        self.webgui = WebGUI(parent=self.sw_subsystems, short_name="WebGUI", instance_config=sw_args)
        self.test_factory = TestFactory(parent=self.sw_subsystems, short_name="TestFactory", instance_config=sw_args)
        self.template_factory = TemplateFactory(parent=self.sw_subsystems, short_name="TemplateFactory",
                                                instance_config=sw_args)

        self.node_factory = NodeFactory(parent=self.sw_subsystems, short_name="NodeFactory", instance_config=sw_args)
        self.naughty = Naughty(parent=self.sw_subsystems, short_name="Naughty", instance_config=sw_args)
        self.test_types = Node(parent=self.sw_subsystems, short_name="TestTypes", instance_config=sw_args)

        self.plugin_factory = PluginFactory(parent=self.sw_subsystems, short_name="PluginFactory",
                                            instance_config=sw_args)
        self.discovery = Discovery(parent=self.sw_subsystems, short_name="Discovery",
                                   instance_config=sw_args)

        # These callback arguments will become visible in the children before start,
        # but are not valid within constructors
        self.sw_subsystems.config().set_item("node_factory", self.node_factory)
        self.sw_subsystems.config().set_item("test_factory", self.test_factory)
        self.sw_subsystems.config().set_item("template_factory", self.template_factory)
        self.sw_subsystems.config().set_item("data_recording", self.data_recording)
        self.sw_subsystems.config().set_item("naughty", self.naughty)
        self.sw_subsystems.config().set_item("test_types", self.test_types)
        self.sw_subsystems.config().set_item("plugin_factory", self.test_factory)
        self.sw_subsystems.config().set_item("discovery", self.discovery)

        secrets_file = self.config().get_item("secrets_file")
        Config.set_secrets(secrets_file, dict(os.environ))

    def start(self) -> None:
        self.mark_subsystem_enabled()
        self.log_internal_status(Status.OK, "Creating new thread for treeroot")
        if self._my_thread is None:
            self._my_thread = Thread(target=self._run_in_thread, daemon=True, name=self.name())
            self._my_thread.start()
        self.log_internal_status(Status.OK, "Letting GUI takeover main thread")
        self.webgui.takeover_main_thread()

    def _run_in_thread(self):
        self.logger.info("TreeRoot Started")
        self.set_annotation("Startup...")

        self.set_annotation("Loading Data Recording...")
        self.data_recording.start()

        self.set_annotation("Loading Test Classes...")
        self.test_factory.start()

        self.set_annotation("Network Discovery...")
        self.discovery.start()

        self.set_annotation("Plugin Factory...")
        self.plugin_factory.start()

        self.set_annotation("Loading Templates...")
        self.template_factory.start()

        self.set_annotation("Loading Nodes...")
        self.node_factory.start()

        self.set_annotation("Naughty List...")
        self.naughty.start()

        self.set_annotation("Spawning tests...")
        self.spawn()
        self.set_annotation("Running tests...")

    def shutdown_instance(self):
        super().shutdown_instance()
        self.logger.info("===================================================================================")
        msg = self.template_factory.report_all_templates()
        self.logger.info(f"\n\nreport_all_templates: {msg}\n")
        msg = self.test_factory.report_all_tests()
        self.logger.info(f"report_all_tests \n\n{msg}\n")
        self.logger.info("TreeRoot exiting")
