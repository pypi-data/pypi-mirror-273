#!/usr/bin/env  python3
from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Info import Info
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status, TestBase


class Uname(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.reply_stats = AnalogStatsFading(self.prefix_name("ReplyTime"))

    def run_test_once(self):
        fqdn = self.config().get_item("fqdn")
        timer = ElapsedTime()
        try:
            with timer:
                info = Info(fqdn, retries=2, timeout=10)
        except Exception as ex:
            self.logger.exception(ex, stack_info=True, exc_info=True)
            self.log_test_status(Status.UNKNOWN, message="Command Error fetching node info")
            return
        self.reply_stats.sample(timer.elapsed())
        how = info.uefi
        ker = info.kernel
        locked = info.kernel_dnf
        self.log_test_status(Status.OK, message=f"{how} {ker} {locked}")


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper = DiscoveryHelper(Uname)
helper.alias("Uname", period=1 * TestBase.sc.hour)
