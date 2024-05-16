import os
from math import nan, isnan

from libsrg.Config import Config
from libsrg.Runner import Runner
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading
from libsrg.Statistics.AnalogStatsSlidingWindow import AnalogStatsSlidingWindow

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status
from Santa_IW.TestBase import TestBase


class PingTest(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.reply_time_stats = AnalogStatsFading(self.prefix_name("Reply_ms"))
        self.loss_percentage_stats_short_term = AnalogStatsSlidingWindow(self.prefix_name("LossPercent_ST"), window=12)
        self.loss_percentage_stats_long_term = AnalogStatsSlidingWindow(self.prefix_name("LossPercent_LT"), window=200)

    def run_test_once(self):
        if self.name() == "PingTest_D߸﹫switch-cr﹫Network﹫sys":
            self.logger.info("trigger")
        burst = bool(self.config().get_item("burst", default=True))
        ping_loss_critical_threshold_percent = float(self.config().get_item("ping_loss_critical_threshold_percent"))
        ping_loss_warning_threshold_percent = float(self.config().get_item("ping_loss_warning_threshold_percent"))
        ping_loss_stat_critical_threshold_percent = float(self.config().get_item(
            "ping_loss_stat_critical_threshold_percent"))
        ping_loss_stat_warning_threshold_percent = float(self.config().get_item(
            "ping_loss_stat_warning_threshold_percent"))
        ping_max_duration = int(self.config().get_item(
            "ping_max_duration"))
        ping_max_count = int(self.config().get_item(
            "ping_max_count"))
        ping_timeout = int(self.config().get_item(
            "ping_timeout"))
        ping_interval = float(self.config().get_item("ping_interval", default=0.1))
        # only root can ask for more
        if os.getuid() != 0:
            ping_interval = max(0.2, ping_interval)
        # Note: rate is limited to 5 hz (200ms) as a normal user
        cmd = (f"ping -q -c {ping_max_count} -w {ping_max_duration} " +
               f"-W {ping_timeout} -i {ping_interval} {self.fqdn}")
        if burst:
            cmd += "-A"
        r = Runner(cmd)
        self.logger.info(f"{self} perform_test {r}")
        self.log_test_status(Status.NODATA,f"{r.ret=} {cmd!r}")
        # 0= some returns, 1= no returns, 2= bad address,255 ssh error
        if r.ret >= 2:
            self.log_test_status(Status.UNKNOWN, message=str(r))
        xmit = 0
        rcvd = 0
        delta = nan
        sd = 0.
        for line in r.so_lines:
            if "packets transmitted" in line:
                parts = line.split()
                xmit += int(parts[0])
                rcvd += int(parts[3])
                self.log_test_status(Status.NODATA, line)
            elif "rtt min" in line:
                parts = line.split()
                bits = parts[3].split('/')
                self.logger.info(f"{parts=} {bits=}")
                delta = float(bits[1])  # min/avg/max/sd
                sd = float(bits[3])  # min/avg/max/sd
                self.log_test_status(Status.NODATA, line)

        #       -c count
        #            Stop after sending count ECHO_REQUEST packets. With deadline option, ping waits for count ECHO_REPLY
        #            packets, until the timeout expires.
        # xmit = min(xmit, ping_max_count)
        # rcvd = min(rcvd, ping_max_count)

        # collect statistics on ping time
        if not isnan(delta) and xmit > 0:
            self.reply_time_stats.sample(delta, weight=xmit, sd=sd)

        # collect statistics on loss
        if xmit > 0:
            loss_percent = (xmit - rcvd) * 100. / xmit
            self.loss_percentage_stats_short_term.sample(loss_percent)
            self.loss_percentage_stats_long_term.sample(loss_percent)
        else:
            loss_percent = 100

        if loss_percent >= ping_loss_critical_threshold_percent:
            self.log_test_status(Status.CRITICAL, tag="current run")
        elif loss_percent >= ping_loss_warning_threshold_percent:
            self.log_test_status(Status.WARNING, tag="current run")
        else:
            self.log_test_status(Status.OK, tag="current run")

        # only threshold statistics after sufficient count
        if self.loss_percentage_stats_short_term.count() >= self.loss_percentage_stats_short_term.window:
            mean_loss = self.loss_percentage_stats_short_term.mean()
            if mean_loss >= ping_loss_stat_critical_threshold_percent:
                self.log_test_status(Status.CRITICAL, tag="mean_loss")
            elif mean_loss >= ping_loss_stat_warning_threshold_percent:
                self.log_test_status(Status.WARNING, tag="mean_loss")
            else:
                self.log_test_status(Status.OK, tag="mean_loss")
        else:
            self.log_test_status(Status.NODATA, "mean_loss has insufficient history")

        msg = (f"Ping {delta:>8.2f}({self.reply_time_stats.mean():>8.2f}) ms, sd={sd:>8.3f} " +
               f"{rcvd=:4n} of {xmit=:4n} loss " +
               f"{loss_percent: 6.2f}%({self.loss_percentage_stats_short_term.mean(): 6.2f}%)")
        self.set_annotation(msg)


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper = DiscoveryHelper(PingTest)
base_config = helper.alias("PingTest_A",
                           burst=False,
                           ping_loss_critical_threshold_percent=10,
                           ping_loss_warning_threshold_percent=5,
                           ping_loss_stat_critical_threshold_percent=5,
                           ping_loss_stat_warning_threshold_percent=1,
                           ping_interval=0.0,
                           ping_max_duration=10,
                           ping_max_count=1000,
                           ping_timeout=1,
                           period=1 * TestBase.sc.minute
                           )

med = helper.alias("PingTest_B", base_config,
                   ping_interval=0.2,
                   ping_loss_stat_critical_threshold_percent=8,
                   ping_loss_stat_warning_threshold_percent=4,
                   ping_loss_critical_threshold_percent=60,
                   ping_loss_warning_threshold_percent=50,
                   period=2 * TestBase.sc.minute

                   )

slow = helper.alias("PingTest_C", med,
                    ping_interval=0.5,
                    ping_max_duration=10,
                    ping_max_count=10,
                    period=3 * TestBase.sc.minute
                    )

sloppy = helper.alias("PingTest_D", slow,
                      ping_loss_critical_threshold_percent=75,
                      ping_loss_warning_threshold_percent=60,
                      ping_loss_stat_critical_threshold_percent=8,
                      ping_loss_stat_warning_threshold_percent=4,
                      ping_max_duration=17,
                      ping_max_count=8,
                      ping_interval=1.0,
                      period=3 * TestBase.sc.minute

                      )

whatever = helper.alias("PingTest_D", sloppy,
                        ping_loss_stat_critical_threshold_percent=50,
                        ping_loss_stat_warning_threshold_percent=25,
                        )
