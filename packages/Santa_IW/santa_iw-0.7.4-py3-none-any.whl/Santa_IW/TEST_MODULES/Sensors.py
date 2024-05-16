#!/usr/bin/env  python3

import json
from typing import Any, Optional, Tuple

from libsrg.Config import Config
from libsrg.Runner import Runner
from libsrg.Statistics.ADStatsBase import ADStatsBase
from libsrg.Statistics.AnalogStatsSlidingWindow import AnalogStatsSlidingWindow

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status, TestBase

"""
https://github.com/lm-sensors/lm-sensors/blob/master/prog/sensors/chips.c

# sensors -j
{
   "coretemp-isa-0000":{
      "Adapter": "ISA adapter",
      "Package id 0":{
         "temp1_input": 41.000,
         "temp1_max": 80.000,
         "temp1_crit": 100.000,
         "temp1_crit_alarm": 0.000
      },
      "Core 0":{
         "temp2_input": 38.000,
         "temp2_max": 80.000,
         "temp2_crit": 100.000,
         "temp2_crit_alarm": 0.000
      },
      "Core 1":{
         "temp3_input": 41.000,
         "temp3_max": 80.000,
         "temp3_crit": 100.000,
         "temp3_crit_alarm": 0.000
      },
      "Core 2":{
         "temp4_input": 39.000,
         "temp4_max": 80.000,
         "temp4_crit": 100.000,
         "temp4_crit_alarm": 0.000
      },
      "Core 3":{
         "temp5_input": 40.000,
         "temp5_max": 80.000,
         "temp5_crit": 100.000,
         "temp5_crit_alarm": 0.000
      }
   },
   "acpitz-acpi-0":{
      "Adapter": "ACPI interface",
      "temp1":{
         "temp1_input": 27.800,
         "temp1_crit": 119.000
      },
      "temp2":{
         "temp2_input": 29.800,
         "temp2_crit": 119.000
      }
   },
   "amdgpu-pci-0300":{
      "Adapter": "PCI adapter",
      "vddgfx":{
         "in0_input": 0.775
      },
      "fan1":{
         "fan1_input": 0.000,
         "fan1_min": 0.000,
         "fan1_max": 3300.000
      },
      "edge":{
         "temp1_input": 56.000,
         "temp1_crit": 100.000,
         "temp1_crit_hyst": -273.150,
         "temp1_emergency": 105.000
      },
      "junction":{
         "temp2_input": 58.000,
         "temp2_crit": 110.000,
         "temp2_crit_hyst": -273.150,
         "temp2_emergency": 115.000
      },
      "mem":{
         "temp3_input": 62.000,
         "temp3_crit": 100.000,
         "temp3_crit_hyst": -273.150,
         "temp3_emergency": 105.000
      },
      "PPT":{
         "power1_average": 41.000,
         "power1_cap": 272.000
      }
   }
}
"""


# noinspection DuplicatedCode
class Sensors(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.statistics_dict: [str, ADStatsBase] = {}

    # def extendParser(self):
    #     self.parser.add_argument("-D", "--device", action="store", dest='dev', default="/dev/sda",
    #                              help="full name of device (ex /dev/sda)")
    #     self.parser.add_argument("-M", "--mask", action="store", dest="mask", default=0x3f,
    #                              help="full name of device (ex /dev/sda)")

    def run_test_once(self):
        r = Runner(f"sensors -j", userat=self.userat)

        if r.success:
            self.log_test_status(Status.OK, f"sensors returned {r.ret=}")
        else:
            self.log_test_status(Status.UNKNOWN, f"sensors returned {r.ret=} {r.success=}")
            return

        jdata = json.loads(r.so_str)
        for outer_name in jdata.keys():
            outer_block = jdata[outer_name]
            if isinstance(outer_block, dict):
                for inner_name in outer_block.keys():
                    inner_block = outer_block[inner_name]
                    if isinstance(inner_block, dict):
                        self.process_block(outer_name, inner_name, inner_block)
        self.log_test_status(Status.OK, message=f"Total sensors checked {len(self.statistics_dict)}")

    def process_block(self, outer_name: str, inner_name: str, inner_block: dict[str, Any]):
        block, prefix = self.repack_block(inner_block)

        if prefix in ["power"]:
            self.process_power_block(outer_name, inner_name, block)
        elif prefix in ["temp", "fan", "in"]:
            self.process_temp__fan_in_block(outer_name, inner_name, block)
        else:
            self.log_test_status(Status.NODATA, f"Unknown prefix {prefix} at {inner_name} {outer_name} {block}")

    @staticmethod
    def float_or_def(block: dict[str, Any], key: str, default_value: Any) -> Optional[float]:
        if key in block:
            return float(block[key])
        return default_value

    def process_temp__fan_in_block(self, outer_name: str, inner_name: str, block: dict[str, Any]):
        input_ = self.float_or_def(block, "input", None)
        max_ = self.float_or_def(block, "max", None)
        min_ = self.float_or_def(block, "min", None)
        crit_ = self.float_or_def(block, "crit", None)
        emergency_ = self.float_or_def(block, "emergency", None)

        if input_ is None:
            self.log_test_status(Status.NODATA, f"no input detected {outer_name} {inner_name} {block=}")
            return

        stat = self.get_sensor_stats(outer_name, inner_name)
        stat.sample(input_)

        if max_ is not None and max_ > 0:
            if input_ < max_:
                status = Status.OK
            else:
                status = Status.WARNING
            self.log_test_status(status, f"Compare {outer_name} {inner_name} {input_=} < {max_=}")
        if min_ is not None:
            if input_ >= min_:
                status = Status.OK
            else:
                status = Status.WARNING
            self.log_test_status(status, f"Compare {outer_name} {inner_name} {input_=} >= {min_=}")
        if crit_ is not None and crit_ > 0:
            if input_ < crit_:
                status = Status.OK
            else:
                status = Status.CRITICAL
            self.log_test_status(status, f"Compare {outer_name} {inner_name} {input_=} < {crit_=}")
        if emergency_ is not None and emergency_ > 0:
            if input_ < emergency_:
                status = Status.OK
            else:
                status = Status.CRITICAL
            self.log_test_status(status, f"Compare {outer_name} {inner_name} {input_=} < {emergency_=}")

    def process_power_block(self, outer_name: str, inner_name: str, block: dict[str, Any]):
        average_ = self.float_or_def(block, "average", None)
        cap_ = self.float_or_def(block, "cap", None)

        if average_ is None:
            self.log_test_status(Status.NODATA, f"no input detected {outer_name} {inner_name} {block=}")
            return

        stat = self.get_sensor_stats(outer_name, inner_name)
        stat.sample(average_)

        if cap_ is not None and cap_ > 0:
            if average_ < cap_:
                status = Status.OK
            else:
                status = Status.WARNING
            self.log_test_status(status, f"Compare {outer_name} {inner_name} {average_=} < {cap_=}")

    def get_sensor_stats(self, outer_name, inner_name) -> ADStatsBase:
        name = self.prefix_name(f"{outer_name}_{inner_name}")
        if name in self.statistics_dict:
            stat = self.statistics_dict[name]
        else:
            stat = AnalogStatsSlidingWindow(name=name, window=100)
            self.statistics_dict[name] = stat
        return stat

    @staticmethod
    def repack_block(block: dict[str, Any]) -> Tuple[dict[str, Any], str]:
        names = list(block.keys())
        prefix = names[0].split("_")[0].strip("0123456789")
        repacked = {key.split("_", maxsplit=1)[-1]: val for key, val in block.items()}
        return repacked, prefix

from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper = DiscoveryHelper(Sensors)
helper.alias("Sensors", {"period": 4 * TestBase.sc.minute})
