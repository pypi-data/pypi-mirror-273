#!/usr/bin/env  python3
from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Runner import Runner
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading
from libsrg.Statistics.DiscreteStatsCumulative import DiscreteStatsCumulative

from Santa_IW.Subassembly import Subassembly
from Santa_IW.DiscoveryHelper import DiscoveryHelper
from Santa_IW.TestBase import Status, TestBase


class SystemctlFailed(TestBase):
    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.filtered_count = AnalogStatsFading(self.prefix_name("filtered_count"))
        self.ignored_count = AnalogStatsFading(self.prefix_name("ignored_count"))
        self.failed_process_count = DiscreteStatsCumulative(self.prefix_name("failed_process"))
        self.restarted_process_count = DiscreteStatsCumulative(self.prefix_name("restarted_process"))
        self.restart_throttle = ElapsedTime("since last restart")
        self.first_restart = True

    # def extendParser(self):
    #     # can set thresholds to allow known count of uncorrectable errors if needed
    #     self.parser.add_argument("-C", "--critical", action="store", dest="critS", default=2,
    #                              help="critical % capacity used", type=int)
    #     self.parser.add_argument("-W", "--warning", action="store", dest="warnS", default=1,
    #                              help="warning % capacity used", type=int)

    def run_test_once(self):
        warning_cnt = int(self.config().get_item("warning_cnt"))
        critical_cnt = int(self.config().get_item("critical_cnt"))
        ignore_list = self.config().get_item("ignore_list")
        dont_restart_list = self.config().get_item("dont_restart_list")
        min_restart_period = float(self.config().get_item("min_restart_period"))
        restart_enable = bool(self.config().get_item("restart_enable"))

        # tried without ssh but failed -- systemctl not in same directory all hosts
        cmd = ["systemctl", "--failed"]
        count = 0
        ignored = 0
        fnames = []
        r = Runner(cmd, userat=self.userat)
        ret = r.ret
        self.logger.info(r)
        r2 = Runner(["systemctl", "is-system-running"], userat=self.userat)
        if ret != 0:
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:04x}")
        else:
            lines2 = r2.so_lines
            state = ",".join(lines2)
            self.logger.info(state)
            lines = r.so_lines
            for line in lines:
                if "failed" in line:
                    lparts = line.split()
                    proc = lparts[1]
                    if "snap-" in line and ".mount" in line:
                        self.logger.warning(f'ignoring "{line}" with "snap-*.mount"')
                        ignored += 1
                        break
                    self.failed_process_count.sample(proc)
                    fnames.append(proc)
                    for item in ignore_list:
                        if item in line:
                            self.log_test_status(Status.MAINT, f'ignoring "{line}" with "{item}"')
                            ignored += 1
                            break
                    else:
                        self.log_test_status(Status.WARNING, line)
                        # only count if nothing from ignored list found
                        count += 1
            self.filtered_count.sample(count)
            self.ignored_count.sample(ignored)
            failed_set = set(fnames)
            dont_restart_set = set(dont_restart_list)
            restart_set = failed_set - dont_restart_set
            msg = f'({count=}/{ignored=}) {state=} {fnames=} {restart_set=}'
            if count >= critical_cnt:
                self.log_test_status(Status.CRITICAL, message=msg)
            elif count >= warning_cnt:
                self.log_test_status(Status.WARNING, message=msg)
            else:
                self.log_test_status(Status.OK, message=msg)

            if restart_enable and len(restart_set) > 0:
                if self.first_restart or self.restart_throttle.current() > min_restart_period:
                    self.first_restart = False
                    self.log_test_status(Status.MAINT, f"About to restart {str(restart_set)}")
                    self.restart_throttle.start()
                    for proc in restart_set:
                        self.restarted_process_count.sample(proc)
                        r = Runner(f"systemctl restart {proc}", userat=self.userat)
                        self.log_test_status(Status.MAINT, str(r))
                else:
                    self.log_test_status(Status.MAINT, f"Too soon to restart {str(restart_set)}")


helper = DiscoveryHelper(SystemctlFailed)

helper.alias("SystemctlFailed",
             period=2 * TestBase.sc.minute,
             warning_cnt=1,
             critical_cnt=2,
             dont_restart_list=[
                 "plymouth-start.service",
                 "dkms.service"
             ],
             ignore_list=[
                 "fwupd-refresh.service",
                 "zfs-share.service",
                 "fwupd.service",
                 "pmlogger_daily.service",
                 "pmie_daily.service",
                 "dnf-makecache.service",
                 "nvidia-powerd.service",
                 "bthelper@hci0.service",
                 "plymouth-start.service",
                 "serial-getty@ttyAMA0.service",
                 "insights-client.service",
                 # "dkms.service"
             ],
             min_restart_period=15 * TestBase.sc.minute,
             restart_enable=True
             )
