import math
import random
from abc import ABC, abstractmethod
from threading import Event, Thread, Timer
from time import sleep
from typing import Optional

from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading
from libsrg.Statistics.DiscreteStatsCumulative import DiscreteStatsCumulative

from Santa_IW.Status import Status, StatusSummation
from Santa_IW.Subassembly import Subassembly


class TestBase(Subassembly, ABC):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name, stepparent=stepparent)  # super defines self.logger
        self._always_send_assessments = True
        self._test_summation = StatusSummation(name="test")

        self._test_due_to_run = Event()
        self._my_thread = Thread(target=self._run_in_thread, daemon=True,name=self.name())
        self._due_timer: Optional[Timer] = None
        self.mark_test_due_to_run()  # start ready on first cycle
        self._test_results_stats = DiscreteStatsCumulative(self.prefix_name("TestResults"))

        self.passed_stats = AnalogStatsFading(self.prefix_name("TestBase_PassRatio"), alpha=0.8)

        self.revisit_period = AnalogStatsFading(self.prefix_name("TestBase_Revisit_Period"), alpha=0.8)
        self.revisit_period_et: ElapsedTime | None = ElapsedTime("revisit_period")

        self.queue_delay = AnalogStatsFading(self.prefix_name("TestBase_Queue_Delay"), alpha=0.8)
        self.queue_delay_et: ElapsedTime | None = ElapsedTime("queue_delay")

        self.run_time = AnalogStatsFading(self.prefix_name("TestBase_Run_Time"), alpha=0.8)
        self.run_time_et: ElapsedTime | None = ElapsedTime("run_time")

        self.first_run: bool = True

        # fetch the usual suspects
        # a default period is set in TreeRoot if not already in global config data
        # it can be overriden at many levels, but I have removed the default here
        # since it would never have any effect other than misleading people
        self.period = float(self.config().get_item("period"))
        self.fqdn = self.config().get_item("fqdn", )
        self.userat = self.config().get_item("userat")
        self.period_et: ElapsedTime | None = ElapsedTime("period")
        self.config().set_item_if_missing("host", self.fqdn)
        self.config().set_item_if_missing("verbose", False)
        self.curReturn = Status.NODATA
        self.curReturnStr = "nocall?"
        self.defReturn = Status.UNKNOWN
        self.defReturnStr = "no status reported?"
        self._observer_period_nochange = -1  # force reporting always

    def _wait_all_enabled(self):
        self._subassembly_enabled.wait()
        self._test_due_to_run.wait()
        self._test_due_to_run.clear()  # clearing make this a one-shot per timer

    def _run_in_thread(self):
        # randomize start time first pass
        # bias towards running quick tests first
        delay0 = math.log10(self.period)
        delay = delay0 + random.uniform(5.0, 7.0)
        self.log_internal_status(Status.NODATA, f"Startup delay is {delay=} {delay0=} {self.name()}")
        sleep(delay)
        self.log_internal_status(Status.NODATA, f"Startup delay complete, entering queue {self.name()}")
        while True:
            # Timer is single use
            if self._due_timer:
                self._due_timer.cancel()
            self._due_timer = Timer(interval=self.period, function=self.mark_test_due_to_run)
            self._due_timer.start()

            self._wait_all_enabled()
            if self._due_timer:
                self._due_timer.cancel()
            self.queue_delay_et.start()
            self._parent.queue_test_on_node(self)

    def mark_test_due_to_run(self, enable: bool = True):
        if enable:
            self._test_due_to_run.set()
        else:
            self._test_due_to_run.clear()

    def spawn(self):
        if not self._my_thread.is_alive():
            self.logger.info(f"Starting test {self.name()}")
            self._my_thread.start()
        else:
            self.logger.info(f"Ignoring Duplicate starting test {self.name()}")

    def node_runs_queued_test(self):
        self.queue_delay_et.stop()
        if not self.first_run:
            self.queue_delay.sample(self.queue_delay_et.elapsed())

        self._test_summation.reset()
        self.logger.info(f"node_runs_queued_test {self.name()} start")
        self.revisit_period_et.stop()
        if not self.first_run:
            self.revisit_period.sample(self.revisit_period_et.elapsed())
        self.first_run = False
        self.revisit_period_et.start()
        try:
            with self.run_time_et:
                result: Status | None = self.run_test_once()
            self.logger.info(f"node_runs_queued_test {self.name()} test returned")
            if result:
                self.log_test_status(result, "completed")
        except Exception as e:
            self.log_test_status(Status.UNKNOWN, f"{type(e)} {str(e)}")
            self.logger.error(f"{self} caught {e}", stack_info=True, exc_info=True)
        finally:
            self.run_time.sample(self.run_time_et.elapsed())
            self._internal_summation.copy_from(self._test_summation)
            self.assess_overall_status()
        code = self._internal_summation.worst()
        passed = code.is_ok()
        self.passed_stats.sample_bool(passed)
        self._test_results_stats.sample(code)
        self.logger.info(f"node_runs_queued_test {self.name()} end")

    def report(self) -> str:
        out = super().report()
        try:
            out += f"{self.latest_status().name} {self._test_results_stats}\n"
            return out
        except Exception as e:
            self.logger.error(f"{self._name} {e}", stack_info=True, exc_info=True)
            raise e

    @abstractmethod
    def run_test_once(self):
        self.logger.error("runTest should be overridden in Subclass")

    def log_test_status(self, status: Status, tag: str | None = None, message: str | None = None) -> None:
        """
        This is overriden within tests to save data to a _test_summation attribute which
        gets double-buffered into _internal_status at test completion

        assess is ignored here

        """
        assert isinstance(status, Status)
        if message is not None and tag is None:
            tag = message
        if tag is None:
            tag = "internal status"
        self._test_summation.add(status, tag=tag, message=message)
        if message is not None:
            if status.is_bad():
                self.logger.warning(message)
            else:
                self.logger.info(message)

    def set_annotation(self, text: str | None = None) -> None:
        self._test_summation.set_message(text)


