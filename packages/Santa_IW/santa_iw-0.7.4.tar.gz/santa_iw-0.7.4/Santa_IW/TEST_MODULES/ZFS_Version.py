#!/usr/bin/env  python3

from libsrg.Runner import Runner

from Santa_IW.TestBase import Status, TestBase


# noinspection PyPep8Naming
class ZFS_Version(TestBase):

    # def extendParser(self):
    #     pass
    #     # can set thresholds to allow known count of uncorrectable errors if needed

    def run_test_once(self):
        cmd = ["zfs", "--version"]
        self.logger.info(cmd)
        r = Runner(cmd, userat=self.userat)
        ret = r.ret
        self.logger.info(ret)
        if ret == 127:
            self.log_test_status(Status.OK, message="zfs not found")
        elif ret != 0:
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:04x}")
        else:
            lines = r.so_lines
            self.logger.info(lines)
            first = lines[0]

            self.log_test_status(Status.OK, message=first)


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(ZFS_Version)
helper.alias("ZFS_Version", period=1 * TestBase.sc.hour)
