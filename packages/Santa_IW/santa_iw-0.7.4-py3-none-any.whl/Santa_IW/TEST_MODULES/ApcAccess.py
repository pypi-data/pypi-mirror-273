#!/usr/bin/env  python3
from libsrg.Config import Config
from libsrg.Runner import Runner
from libsrg.Statistics.ADStatsBase import ADStatsBase
from libsrg.Statistics.AnalogStatsSlidingWindow import AnalogStatsSlidingWindow
from libsrg.Statistics.DiscreteStatsCumulative import DiscreteStatsCumulative

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status, TestBase


class ApcAccess(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.apc_status_stats = DiscreteStatsCumulative(self.prefix_name("ReportedStatus"))
        self.statistics_dict: [str, ADStatsBase] = {}
        self.track_names = [
            "LINEV", "LOADPCT", "BCHARGE", "TIMELEFT", "MBATTCHG", "MINTIMEL",
            "MAXTIME", "BATTV", "NUMXFERS", "TONBATT",
            "CUMONBATT", ]

    def get_sensor_stats(self, outer_name, inner_name) -> ADStatsBase:
        name = self.prefix_name(f"{outer_name}_{inner_name}")
        if name in self.statistics_dict:
            stat = self.statistics_dict[name]
        else:
            stat = AnalogStatsSlidingWindow(name=name, window=100)
            self.statistics_dict[name] = stat
        return stat

    def run_test_once(self):
        r = Runner("apcaccess -u", userat=self.userat, timeout=5,retries=2)
        ret = r.ret
        stat = self.get_sensor_stats("APC", "return")
        stat.sample(ret)
        if ret != 0:
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:04x} {r}")
            return
        data = {}
        for line in r.so_lines:
            half = line.split(":", maxsplit=1)
            name = half[0].strip()
            value = half[1].strip()
            data[name] = value
            self.log_test_status(Status.OK, message=line)
        for name in self.track_names:
            if name in data:
                value = float(data[name])
                stat = self.get_sensor_stats("APC", name)
                stat.sample(value)
        status = data.get("STATUS", "missing")
        self.apc_status_stats.sample(status)
        if status == "ONLINE":
            self.log_test_status(Status.OK, message=f"APC ONLINE")
        else:
            self.log_test_status(Status.WARNING, message=f"APC {status}")


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(ApcAccess)
helper.alias("ApcAccess", {"period": 3 * TestBase.sc.minute})
