#!/usr/bin/env  python3

from libsrg.Runner import Runner

from Santa_IW.TestBase import Status, TestBase


class RemoteProcess(TestBase):

    # def extendParser(self):
    #     self.parser.add_argument("-p", "--proc", action="store", dest="remote_proc",
    #                              default="Mail.app/Contents/MacOS/Mail", help="name of process")

    def run_test_once(self):
        process_name = self.config().get_item("process_name")
        process_user = self.config().get_item("process_user")
        cmd = ["ps", "-fu", process_user]
        self.logger.info(cmd)
        r = Runner(cmd, userat=self.userat)
        ret = r.ret
        self.logger.info(ret)
        if ret != 0:
            self.logger.warning(r)
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:04x}")
        else:
            lines = r.so_lines
            for line in lines:
                if process_name in line:
                    self.log_test_status(Status.OK, message=line)
                    break
            else:  # no break
                self.log_test_status(Status.WARNING,
                                     message=f"Process {process_name} for user {process_user} not found")


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(RemoteProcess)
helper.alias("RemoteProcess",
             {"process_name": "/sbin/zed", "process_user": "root", "period": 5 * TestBase.sc.minute})
