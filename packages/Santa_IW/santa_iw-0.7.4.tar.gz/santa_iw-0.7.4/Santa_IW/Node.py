import threading
from threading import Semaphore

from libsrg.Config import Config
from libsrg.Info import Info
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading

from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import TestBase


class Node(Subassembly):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, sw_node: bool = False) -> None:
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        self.node_name = short_name
        self.config().set_item("short_name", short_name, overwrite=False)
        do_info = bool(self.config().get_item("get_node_info", default=False))
        if do_info:
            try:
                # get node Info and copy into args
                self.node_info = Info(self.node_name)
                self.logger.info(self.node_info)
                for k, v in self.node_info.__dict__.items():
                    if isinstance(v, str):
                        self.config().set_item("node_" + k, v)
            except Exception as e:
                self.logger.warning(f"caught {e} processing Info", stack_info=True, exc_info=True)
                self.node_info = None

        if not sw_node:
            tmp = self.config().get_item("fqdn")
            self.config().set_item("user", "root", overwrite=False)
            self.config().set_item("userat", f"{self.config().get_item('user')}@{tmp}", overwrite=True)

        self.sched_with_parent = bool(self.config().get_item("sched_with_parent", default=False))
        max_concurrent_tests_on_node = int(self.config().get_item("max_concurrent_tests_on_node"))
        self._node_serialization_sem = Semaphore(max_concurrent_tests_on_node)
        self._queue_depth_lock = threading.Lock()
        self._queue_depth: int = 0
        self._queue_depth_stats = AnalogStatsFading(self.prefix_name("QueueDepth"), alpha=0.99)

        # self.logger.info(map_chain_as_str(self.args))

    def queue_test_on_node(self, test: TestBase) -> None:
        """queue_test_on_node waits for a node enabled event, acquires a semaphore
        for rate limiting within the node and calls back to test.perform_test()
        """
        self.logger.info(f"queue_test_on_node: {test}")
        if self.sched_with_parent:
            self._parent.queue_test_on_node(test)
        else:
            with self._queue_depth_lock:
                self._queue_depth += 1
            with self._node_serialization_sem:
                with self._queue_depth_lock:
                    self._queue_depth -= 1
                    self._queue_depth_stats.sample(self._queue_depth)
                self._subassembly_enabled.wait()
                try:
                    self.logger.info(f"queue_test_on_node: {test} before call")
                    test.node_runs_queued_test()
                    self.logger.info(f"queue_test_on_node: {test} after call")
                except Exception as e:
                    self.logger.error(f"queue_test_on_node caught Exception {e} from {test}", stack_info=True,exc_info=True)
                    self.log_internal_status(Status.CRITICAL, message=f"Test {test} raised {type(e)} {e}")
