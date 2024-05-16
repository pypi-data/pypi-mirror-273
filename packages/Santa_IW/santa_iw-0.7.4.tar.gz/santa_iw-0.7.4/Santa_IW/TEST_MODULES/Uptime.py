#!/usr/bin/env  python3
from libsrg.Config import Config
from libsrg.Runner import Runner
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status, TestBase

"""
uptime outputs:
 14:37:05 up 4 days,  3:23,  0 users,  load average: 0.41, 1.30, 1.25
 09:28:23 up 1 day, 23:01,  1 user,  load average: 0.00, 0.00, 0.00
 14:39:07 up  5:41,  1 user,  load average: 0.24, 0.19, 0.18
 09:55:10 up 25 min,  0 user,  load average: 0.10, 0.10, 0.08
 09:42:32 up 12 min,  0 user,  load average: 0.00, 0.04, 0.04
 09:31:25 up 1 min,  0 user,  load average: 0.67, 0.23, 0.08
 09:29:54 up 0 min,  0 user,  load average: 0.41, 0.10, 0.03
 
"""


# # uptime --pretty
# up 1 week, 2 days, 21 minutes
# # ssh root@santa uptime --pretty
# up 20 hours, 9 minutes

class Uptime(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.uptime_stats = AnalogStatsFading(self.prefix_name("Uptime"))
        self.last_net_seconds = 0

    def run_test_once(self):

        cmd = ["uptime --pretty"]
        r = Runner(cmd, userat=self.userat)
        ret = r.ret
        self.logger.info(ret)
        if ret != 0:
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:04x}")
        else:
            if len(r.so_lines) != 1:
                self.log_test_status(Status.UNKNOWN, message=f"expected 1 line but got {len(r.so_lines)}")
                return
            line = r.so_lines[0]
            net_seconds = 0
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                self.log_test_status(Status.UNKNOWN, message=f"expected output to start with 'up' got {line}")
                return
            chunks = parts[1].split(",")
            for chunk in chunks:
                chunk = chunk.strip()
                tokens = chunk.split(" ")
                if len(tokens) != 2:
                    self.log_test_status(Status.UNKNOWN, message=f"expected number unit pair got {tokens}")
                num = int(tokens[0].strip())
                units = tokens[1].strip()
                # startswith because uptime shows week/weeks, etc
                if units.startswith("week"):
                    net_seconds += num * self.sc.week
                elif units.startswith("day"):
                    net_seconds += num * self.sc.day
                elif units.startswith("hour"):
                    net_seconds += num * self.sc.hour
                elif units.startswith("minute"):
                    net_seconds += num * self.sc.minute
                elif units.startswith("second"):
                    net_seconds += num * self.sc.second  # don't think this happens, but just in case
                else:
                    self.log_test_status(Status.UNKNOWN, message=f"unexpected unit {units}")
            self.uptime_stats.sample(net_seconds)
            flat = line + f" -- Total {net_seconds} seconds "
            if self.last_net_seconds > net_seconds:
                flat = "Reboot -- " + flat
                self.log_test_status(Status.MAINT, message=flat)
            else:
                self.log_test_status(Status.OK, message=flat)
            self.last_net_seconds = net_seconds

from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(Uptime)
helper.alias("Uptime", period=2 * TestBase.sc.minute)
