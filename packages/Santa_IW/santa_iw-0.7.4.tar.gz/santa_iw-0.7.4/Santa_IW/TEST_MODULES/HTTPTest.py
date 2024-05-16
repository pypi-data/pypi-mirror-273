from datetime import datetime
from typing import Optional

import requests
from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading
from libsrg.Statistics.DiscreteStatsCumulative import DiscreteStatsCumulative
from requests import Response, get

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status
from Santa_IW.TestBase import TestBase


class HTTPTest(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        # self.ttl_stats = AnalogStatsFading(self.prefix_name("Ping_ms"))
        # self.miss_stats = AnalogStatsFading(self.prefix_name("ReplyRatio"))
        self.reply_stats = AnalogStatsFading(self.prefix_name("ReplyTime"))
        self.cert_stats = AnalogStatsFading(self.prefix_name("CertificateDaysToLive"))
        self.code_stats = DiscreteStatsCumulative(self.prefix_name("ReplyCode"))

    def run_test_once(self) -> Status:
        # url can use {{fqdn}} for portable defaults
        # see helper.alias lines at EOF
        url_ = self.config().get_item("url", jinja=True)
        ok_stats = self.config().get_item("allowed_status_codes")
        msg = "bad response"
        response_: Optional[Response]=None
        try:
            # self.page = requests.get(self.url, auth=HTTPBasicAuth(self.args.user, self.args.password), verify=self.v)
            for try_ in range(0, 2):
                et = ElapsedTime()
                response_: Response = get(url_, stream=True)
                reply_time = et.current()
                self.reply_stats.sample(reply_time)
                msg = f"{response_.status_code=} {reply_time=} {url_}"
                if url_.startswith("https:"):
                    connection = response_.raw.connection
                    if connection is not None and connection.sock is not None:
                        certificate_info_ = connection.sock.getpeercert()
                        if certificate_info_ is not None:
                            for k, v in certificate_info_.items():
                                self.log_test_status(Status.OK, f"{k}: {v}")
                            # subject = dict(x[0] for x in certificate_info['subject'])
                            # issuer = dict(x[0] for x in certificate_info['issuer'])
                            # noinspection PyPep8Naming
                            notAfter = certificate_info_['notAfter']
                            # notAfter: Jun 4 22:57:04 2024 GMT
                            fmt = "%b %d %H:%M:%S %Y %Z"
                            cert_dt = datetime.strptime(notAfter, fmt)
                            now_dt = datetime.utcnow()
                            ttl = cert_dt - now_dt
                            seconds_to_live = ttl.total_seconds()
                            days_to_live = seconds_to_live / self.sc.day
                            self.cert_stats.sample(days_to_live)
                            msg = f"cert remaining {ttl} / {days_to_live:6.2f} days / {seconds_to_live:,.0f} s"
                            if days_to_live < 7:
                                self.log_test_status(Status.WARNING, msg)
                            elif days_to_live < 21:
                                self.log_test_status(Status.MAINT, msg)
                            else:
                                self.log_test_status(Status.OK, msg)

                self.code_stats.sample(response_.status_code)
                if response_.status_code in ok_stats:
                    break
            if response_.status_code not in ok_stats:
                self.log_test_status(Status.CRITICAL, message=msg)
                return Status.CRITICAL
            self.log_test_status(Status.OK, message=msg)
            return Status.OK
        except Exception as e:
            self.logger.exception(e, stack_info=True, exc_info=True)
            self.log_test_status(Status.CRITICAL, message=f"Exception: {type(e)} {str(e)}")
            return Status.CRITICAL


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper = DiscoveryHelper(HTTPTest)
# noinspection HttpUrlsUsage
helper.alias("HTTPTest", {"allowed_status_codes": [200], "url": "http://{{fqdn}}", "period": 5 * TestBase.sc.minute})
helper.alias("CockpitTest",
             {"allowed_status_codes": [200], "url": "https://{{fqdn}}:9090", "period": 10 * TestBase.sc.minute})

if __name__ == "__main__":
    with requests.get("https://kylo.home.goncalo.name:9090", stream=True) as response:
        certificate_info = response.raw.connection.sock.getpeercert()
        subject = dict(x[0] for x in certificate_info['subject'])
        issuer = dict(x[0] for x in certificate_info['issuer'])

        print("commonName:", subject['commonName'])
        print("issuer:", issuer['commonName'])
