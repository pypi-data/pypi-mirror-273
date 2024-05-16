#!/usr/bin/env  python3
from libsrg.Runner import Runner

from Santa_IW.TestBase import Status, TestBase


class PendingUpdates(TestBase):

    # def extendParser(self):
    #     # can set thresholds to allow known count of uncorrectable errors if needed
    #     self.parser.add_argument("-C", "--critical", action="store", dest="critS", default=20,
    #                              help="critical % capacity used", type=int)
    #     self.parser.add_argument("-W", "--warning", action="store", dest="warnS", default=10,
    #                              help="warning % capacity used", type=int)

    def run_test_once(self):
        warn_threshold = self.config().get_item("warn_threshold")
        crit_threshold = self.config().get_item("crit_threshold")
        ignore_list = [
            "Last metadata expiration check",
            "apt does not have a stable CLI interface",
            "Listing...",
        ]
        kernel_count = 0
        package_count = 0
        last = None
        last_i = "no updates"

        cmd = ["dnf", "check-update"]
        self.logger.info(cmd)
        r = Runner(cmd, userat=self.userat)
        ret = r.ret
        kernel_locked = False
        if ret == 0x7f:
            # try again with apt
            cmd = ["apt", "list", "--upgradable"]
            self.logger.info(cmd)
            r = Runner(cmd, userat=self.userat)
            ret = r.ret
        else:
            # see if kernel locked on redhat
            cmd2 = ["grep", "-e", '^exclude=kernel',
                    "/etc/dnf/dnf.conf"]
            r2 = Runner(cmd2, userat=self.userat)
            if r2.ret == 0:
                kernel_locked = True

        self.logger.info(ret)
        if ret not in [0, 100]:
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:04x} {cmd}")
        else:
            lines = r.so_lines
            lines.reverse()
            for line in lines:
                skip = False
                for phrase in ignore_list:
                    if phrase in line:
                        skip = True
                        break

                if skip:
                    continue
                elif "kernel" in line:
                    last = line
                    kernel_count += 1
                else:
                    last_i = line
                    package_count += 1
            if last is None:
                last = last_i
            if kernel_locked:
                self.log_test_status(Status.OK, message=f'({kernel_count}K/{package_count}P) LOCKED {last}')
            else:
                if kernel_count >= crit_threshold:
                    self.log_test_status(Status.CRITICAL, message=f'({kernel_count}K/{package_count}P) {last}')
                elif kernel_count >= warn_threshold:
                    self.log_test_status(Status.WARNING, message=f'({kernel_count}K/{package_count}P) {last}')
                else:
                    self.log_test_status(Status.OK, message=f'({kernel_count}K/{package_count}P) {last}')


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(PendingUpdates)
helper.alias("PendingUpdates", {"warn_threshold": 10, "crit_threshold": 20,"period":2*TestBase.sc.hour})
