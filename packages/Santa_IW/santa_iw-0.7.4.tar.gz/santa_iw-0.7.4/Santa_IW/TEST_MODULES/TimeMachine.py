#!/usr/bin/env  python3
import plistlib
from datetime import datetime
from pathlib import Path

from libsrg.Config import Config
from libsrg.Runner import Runner
from libsrg.Statistics.AnalogStatsFading import AnalogStatsFading

from Santa_IW.Subassembly import Subassembly
from Santa_IW.TestBase import Status, TestBase


# /TM_MACOS/TM_IMAC/imac.sparsebundle
# ls *.plist
# com.apple.TimeMachine.MachineID.plist  com.apple.TimeMachine.SnapshotHistory.plist  Info.plist

class TimeMachine(TestBase):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly, stepparent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent, stepparent=stepparent,
                         short_name=short_name)  # super defines self.logger
        self.snapshot_age = AnalogStatsFading(self.prefix_name("Age_Days"))
        self.snapshot_count = AnalogStatsFading(self.prefix_name("Snapshots"))

    def plist_as_dict(self, name, bundle):
        fpath = bundle / name
        cmd = ["cat", str(fpath)]
        r = Runner(cmd, rethrow=True, verbose=True, userat=self.userat)
        pdict = plistlib.loads(r.so_bytes)
        self.log_test_status(Status.NODATA, f"{fpath} {pdict!r}")
        return pdict

    def run_test_once(self):
        warn_t = self.config().get_item("warning_threshold_days")
        crit_t = self.config().get_item("critical_threshold_days")
        path = self.config().get_item("path")
        r = Runner(f"ls {path}/*bundle -d", userat=self.userat)
        subs = r.so_lines
        self.logger.info(subs)
        if len(subs) < 1:
            self.log_test_status(Status.CRITICAL, message=f"*bundle not found in {path}")
        elif len(subs) > 1:
            self.log_test_status(Status.CRITICAL, message=f"MULTIPLE {subs} found in {path}")
        bpath = Path(subs[0])

        pdict = self.plist_as_dict("com.apple.TimeMachine.MachineID.plist", bpath)
        bdict = self.plist_as_dict("com.apple.TimeMachine.SnapshotHistory.plist", bpath)
        # idict = self.plist_as_dict("Info.plist", bpath)

        model_id = pdict["com.apple.backupd.ModelID"]
        backup = pdict['VerificationDate']
        # tz = backup.tzinfo # there was not tz info
        now = datetime.utcnow()
        age = now - backup
        age_days = age.total_seconds() / self.sc.day

        snaps = bdict["Snapshots"]
        nsnaps = len(snaps)
        if nsnaps > 0:
            last = snaps[-1]
            self.logger.info(last)
            when = last.get('com.apple.backupd.SnapshotCompletionDate', "???")
            # siz = last.get('com.apple.backupd.SnapshotTotalBytesCopied', -10)
            # isize = idict.get('size', -10)
            age = now - when
            age_days = age.total_seconds() / self.sc.day

        else:
            when = "?"
            # siz = -1
            # isize = -2

        self.snapshot_age.sample(age_days)
        self.snapshot_count.sample(nsnaps)
        msg = f"age {age} {bpath} snaps={nsnaps} {model_id} {when}"
        self.logger.info(msg)
        if age_days > crit_t:
            self.log_test_status(Status.CRITICAL, message=msg)
        elif age_days > warn_t:
            self.log_test_status(Status.WARNING, message=msg)
        else:
            self.log_test_status(Status.OK, message=msg)


from Santa_IW.DiscoveryHelper import DiscoveryHelper

helper: DiscoveryHelper = DiscoveryHelper(TimeMachine)
# no default for path
helper.alias("TimeMachine", {"warning_threshold_days": 14, "critical_threshold_days": 21},
             period=30 * TestBase.sc.minute)
