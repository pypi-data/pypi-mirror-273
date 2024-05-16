#!/usr/bin/env  python3
import re

from libsrg.Runner import Runner

from Santa_IW.TestBase import Status, TestBase


# noinspection PyPep8Naming
class IPVx_Address(TestBase):

    # def extendParser(self):
    #     # can set thresholds to allow known count of uncorrectable errors if needed
    #     self.parser.add_argument("-g", "--global", action="store_const", dest="scope",
    #     const="global", default="global",
    #                              help="scope: global")
    #     self.parser.add_argument("-l", "--link", action="store_const", dest="scope",
    #     const="link", default="global",
    #                              help="scope: link")
    #     self.parser.add_argument("-4", "--ipv4", action="store_const", dest="inet",
    #     const="inet", default="inet",
    #                              help="inet: inet ")
    #     self.parser.add_argument("-6", "--ipv6", action="store_const", dest="inet",
    #     const="inet6", default="inet",
    #                              help="inet: inet ")

    def run_test_once(self):
        scope = self.config().get_item("scope", default="global")  # link
        inet = self.config().get_item("inet", default="inet")  # inet6
        cmd = ["ip", "-oneline", "addr"]
        self.logger.info(cmd)
        r = Runner(cmd, userat=self.userat)
        ret = r.ret
        self.logger.info(ret)
        r2=Runner("ip r", userat=self.userat)
        if r2.success:
            route=r2.so_lines[0]
            for line in r2.so_lines:
                self.log_test_status(Status.OK,line)
        else:
            route=" no route"
        if ret != 0:
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:04x}")
        else:
            lines = r.so_lines

            for line in lines:
                if "deprecated" in line:
                    continue
                if re.match("1:\\slo\\s", line):
                    continue

                if not re.search(r"\s" + inet + r"\s", line):
                    continue
                if not re.search("scope\\s" + scope + "\\s", line):
                    continue
                parts = line.split()
                self.log_test_status(Status.OK, message=f"{parts[3]:<20} {route}")
                break
            else:
                self.log_test_status(Status.NODATA, message=f'no match for {inet}')


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(IPVx_Address)
helper.alias("IPV4_Address", {"scope": "global", "inet": "inet","period":5*TestBase.sc.minute})
helper.alias("IPV6_Address", {"scope": "global", "inet": "inet6","period":5*TestBase.sc.minute})
