#!/usr/bin/env  python3
from libsrg.Config import Config
from libsrg.Runner import Runner
from libsrg.Statistics.AnalogStatsSlidingWindow import AnalogStatsSlidingWindow

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status, TestBase


class DiskFree(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        # self.ttl_stats = AnalogStatsFading(self.prefix_name("Ping_ms"))
        # self.miss_stats = AnalogStatsFading(self.prefix_name("ReplyRatio"))
        self.used_stats = AnalogStatsSlidingWindow(self.prefix_name("PercentUsed"))

    def run_test_once(self):
        warn_t = self.config().get_item("warning")
        crit_t = self.config().get_item("critical")
        path = self.config().get_item("path")
        cmd = [
            "df", path, "--output=pcent,size,used,avail,file,target"]
        r = Runner(cmd, userat=self.userat)

        ret = r.ret
        self.logger.info(ret)
        if ret != 0:
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:04x} {path}")
        else:
            lines = r.so_lines
            if len(lines) != 2:
                self.log_test_status(Status.UNKNOWN, message=f"Expected 2 lines in {lines}")
            else:
                line = lines[-1].strip()
                parts = line.split(' ')
                self.logger.info("Split")
                n = 6
                if len(parts) < n:
                    self.logger.warning(parts)
                    self.log_test_status(Status.UNKNOWN, message=f"Expected {n} parts in {line}")
                else:
                    val = (parts[0])[:-1]
                    self.logger.info(val)
                    used = float(val)
                    msg = f"Used {used:6.2f}% on {path}"
                    self.used_stats.sample(used)
                    if used > crit_t:
                        self.log_test_status(Status.CRITICAL, message=msg)
                    elif used > warn_t:
                        self.log_test_status(Status.WARNING, message=msg)
                    else:
                        self.log_test_status(Status.OK, message=msg)


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(DiskFree)
helper.alias("DiskFree", {"warning": 75, "critical": 80,"period":10*TestBase.sc.minute})
