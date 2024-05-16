#!/usr/bin/env  python3

from datetime import datetime
from datetime import timedelta

from libsrg.Config import Config
from libsrg.Runner import Runner
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status, TestBase


# noinspection PyPep8Naming
class ZFS_Snapshots(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.vol: str = self.config().get_item("vol", "pool", "dev", "par_0")
        self.warnS = self.config().get_item("warnS", default=45)
        self.critS = self.config().get_item("critS", default=90)
        self.age = AnalogStatsFading(self.prefix_name("ageSeconds"))
        self.snapshots = AnalogStatsFading(self.prefix_name("snapshotsCount"))

    # def extendParser(self):
    #
    #     self.parser.add_argument("-C", "--critical",
    #                              action="store", dest="critS", default=60, help="critical age threshold in minutes",
    #                              type=int)
    #     self.parser.add_argument("-W", "--warning",
    #                              action="store", dest="warnS", default=25, help="warning age threshold in minutes",
    #                              type=int)
    #     self.parser.add_argument("-V", "--volume",
    #                              action="store", dest="vol", default="ZRaid/PRIMARY/NFSPUB/GPUB",
    #                              help="full name of device (ex /dev/sda)")

    def run_test_once(self):
        zargs = ["/sbin/zfs", "list", "-H", "-t",
                 "snapshot", "-r",
                 "-d1", "-o", "name,creation", "-S", "creation", self.vol]
        r = Runner(zargs, userat=self.userat)
        lines = r.so_lines
        ret = r.ret
        if ret != 0:
            res_str = f"UNKNOWN - Command Error 0x{ret:04x} {self.vol}"
            self.log_test_status(Status.UNKNOWN, message=res_str)
        else:
            minutes = 60
            warn_t = timedelta(0, minutes * int(self.warnS))
            crit_t = timedelta(0, minutes * int(self.critS))

            # reg=re.compile(r'auto-([-0-9:_.]*)')
            # regp=re.compile(r'[-:_.]+')
            dtnow = datetime.now()
            if lines:
                nlines = len(lines)
                for line in lines:
                    parts = line.split('\t')
                    self.logger.info(parts)
                    name = parts[0]
                    if len(parts) > 1:
                        dat_a = parts[1]
                        dt = datetime.strptime(dat_a, '%a %b %d %H:%M %Y')
                        age = dtnow - dt
                        self.age.sample(age.total_seconds())
                        self.snapshots.sample(nlines)
                        if age >= crit_t:
                            res_str = f"CRITICAL - Age {age} for {name} of {nlines}"
                            self.log_test_status(Status.CRITICAL, message=res_str)
                        elif age > warn_t:
                            res_str = f"WARNING - Age {age} for {name} of {nlines}"
                            self.log_test_status(Status.WARNING, message=res_str)
                        elif nlines > 500:
                            res_str = f"WARNING - Age {age} for {name} of {nlines}>500"
                            self.log_test_status(Status.WARNING, message=res_str)
                        else:
                            res_str = f"OK - Age {age} for {name} of {nlines}"
                            self.log_test_status(Status.OK, message=res_str)
                        break
            else:
                res_str = f"CRITICAL - No snapshots for {self.vol}"
                self.log_test_status(Status.CRITICAL, message=res_str)


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(ZFS_Snapshots)
helper.alias("ZFS_Snapshots_Primary", {"warnS": 15, "critS": 30, "period": 10 * TestBase.sc.minute})
helper.alias("ZFS_Snapshots_Copy", {"warnS": 45, "critS": 90, "period": 10 * TestBase.sc.minute})
