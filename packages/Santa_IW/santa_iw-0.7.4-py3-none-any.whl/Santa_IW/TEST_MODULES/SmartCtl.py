#!/usr/bin/env  python3

import json

from libsrg.Config import Config
from libsrg.Runner import Runner
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status, TestBase

"""
      Bit 0: Command line did not parse.

      Bit 1: Device open failed, device did not  return  an  IDENTIFY  DEVICE
             structure,  or  device  is  in a low-power mode (see ´-n´ option
             above).

      Bit 2: Some SMART or other ATA command to the disk failed, or there was
             a  checksum  error  in  a  SMART data structure (see ´-b´ option
             above).

      Bit 3: SMART status check returned "DISK FAILING".

      Bit 4: We found prefail Attributes <= threshold.

      Bit 5: SMART status check returned "DISK OK" but  we  found  that  some
             (usage  or  prefail)  Attributes  have been <= threshold at some
             time in the past.

      Bit 6: The device error log contains records of errors.

      Bit 7: The device self-test log contains records of errors.  [ATA only]
             Failed  self-tests outdated by a newer successful extended self-
             test are ignored.
"""


class SmartCtl(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.run_hours = AnalogStatsFading(self.prefix_name("PowerOnHours"))
        self.dev: str = self.config().get_item("dev", "par_0")
        self.mask: int = int(self.config().get_item("mask", default=0x3f))

    # def extendParser(self):
    #     self.parser.add_argument("-D", "--device", action="store", dest='dev', default="/dev/sda",
    #                              help="full name of device (ex /dev/sda)")
    #     self.parser.add_argument("-M", "--mask", action="store", dest="mask", default=0x3f,
    #                              help="full name of device (ex /dev/sda)")

    def run_test_once(self):

        cmd = ["/usr/sbin/smartctl", "-a", "--json", self.dev]
        r = Runner(cmd, userat=self.userat)
        ret = r.ret
        retm = ret & self.mask
        fulltext = r.so_str
        if len(fulltext) > 30 and fulltext.startswith("{"):
            jdata = json.loads(fulltext)
        else:
            self.log_test_status(Status.UNKNOWN,f"Bad reply from smartctl {r}")
            return
        # self.logger.info(jdata)
        poweron = "(hours not reported)"
        if "power_on_time" in jdata:
            try:

                hours = jdata['power_on_time']['hours']
                years = hours / (24 * 365)
                poweron = f"Powered On {years:4.2f} years ({hours} hours)"
                self.run_hours.sample(hours)
            except Exception as e:
                self.logger.exception(e, stack_info=True, exc_info=True)

        if retm == 0:
            self.log_test_status(Status.OK, message=f"{poweron} ret=0x{ret:02x} {self.dev}")
        elif ret == 0x7f or ret == 0xff:
            self.log_test_status(Status.UNKNOWN, message=f"Command Error 0x{ret:02x} {poweron} {self.dev}")
        elif retm & 0x01:
            msg = f"COMMAND LINE DID NOT PARSE 0x{ret:02x} {poweron} {self.dev}"
            self.log_test_status(Status.UNKNOWN, message=msg)
        elif retm & 0x2:
            self.log_test_status(Status.CRITICAL, message=f"DEVICE OPEN FAILED 0x{ret:02x} {poweron} {self.dev}")
        elif retm & 0x4:
            self.log_test_status(Status.OK, message=f"ATA COMMAND 0x{ret:02x} {poweron} {self.dev}")
        elif retm & 0x8:
            self.log_test_status(Status.CRITICAL, message=f"DISK FAILING 0x{ret:02x} {poweron} {self.dev}")
        elif retm & 0x10:
            self.log_test_status(Status.WARNING, message=f"PREFAIL 0x{ret:02x} {poweron} {self.dev}")
        elif retm & 0x20:
            self.log_test_status(Status.WARNING, message=f"Past Errors 0x{ret:02x} {poweron} {self.dev}")
        elif retm & 0x40:
            self.log_test_status(Status.WARNING, message=f"DEVICE ERR LOGGED 0x{ret:02x} {poweron} {self.dev}")
        elif retm & 0x80:
            self.log_test_status(Status.WARNING, message=f"SELF-TEST ERRS 0x{ret:02x} {poweron} {self.dev}")
        else:
            self.log_test_status(Status.UNKNOWN, message=f"Other error 0x{ret:02x} {poweron} {self.dev}")


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper = DiscoveryHelper(SmartCtl)
helper.alias("SmartCtl",{"period":6*TestBase.sc.minute})
