import logging
import os
import socket
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from ipaddress import IPv4Address, IPv4Network  # IPv4Network
from pathlib import Path
from typing import Any, Optional

from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Info import Info
from libsrg.Runner import Runner
from requests import Response, get

from Santa_IW.NorthPole import NorthPole
from Santa_IW.PluginBase import PluginBase
from Santa_IW.PluginType import PluginType
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly


class TestDiscoveryBase(ABC):
    def __init__(self, host_creator: "HostCreator"):
        self.host_creator = host_creator
        self.config = self.host_creator.config
        self.logger = self.host_creator.logger
        self.fqdn = self.host_creator.fqdn
        self.can_ping = self.host_creator.can_ping
        self.can_ssh = self.host_creator.can_ssh
        self.can_name = self.host_creator.can_name
        self.userat = self.host_creator.userat
        self.can_snmp = self.host_creator.can_snmp

    def add_test(self, d: dict[str, Any]):
        self.host_creator.add_test(d)

    def add_template(self, d: str):
        self.host_creator.add_template(d)

    @abstractmethod
    def discover(self):
        pass


class PingDiscovery(TestDiscoveryBase):

    def discover(self):
        if self.can_ping and not self.can_ssh:
            self.add_test(
                {
                    "test_type": "PingTest_D"
                })
        else:
            self.add_test(
                {
                    "test_type": "PingTest_A"
                })


class LinuxCommonDiscovery(TestDiscoveryBase):

    def discover(self):
        if self.can_ssh:
            self.add_test(
                {
                    "test_type": "Uname"
                })
            self.add_test(
                {
                    "test_type": "Uptime"
                })
            self.add_test(
                {
                    "test_type": "SystemctlFailed"
                })
            self.add_test(
                {
                    "test_type": "PendingUpdates"
                })
            self.add_test(
                {
                    "test_type": "IPV4_Address"
                })
            self.add_test(
                {
                    "test_type": "IPV6_Address"
                })


class SNMPDiscovery(TestDiscoveryBase):

    def discover(self):
        if not self.can_snmp:
            return
        self.add_test(
            {
                "test_type": "SNMP_id",
                "community": "{{__SNMP_COMMUNITY__}}",
            })


class SensorsDiscovery(TestDiscoveryBase):

    def discover(self):
        if self.can_ssh:
            r = Runner("sensors -j", userat=self.userat, timeout=5)
            if r.success:
                self.add_test(
                    {
                        "test_type": "Sensors"
                    })


class HostCreator:

    def __init__(self, address: IPv4Address, config: Config, group_paths: dict[str, Path], host_template_dir: Path):
        self.hostname_info = None
        self.is_localhost = None
        self.community = None
        self.map_dev_to_id: dict[str, str] = {}
        self.uname_hostname = "unknown"
        self.oui = None
        self.kernel_name: str = "unknown"
        self.mac_address: str = "unknown"
        self.oui: str = "unknown"
        self.group_path: Optional[Path] = None
        self.group_name: Optional[str] = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.address = address
        self.config = config
        self.group_paths = group_paths
        self.host_template_dir = host_template_dir
        #
        self.auto_tests: list[dict[str, Any]] = []
        self.auto_templates: list[str] = []
        self.can_ping = False
        self.can_ssh = False
        self.can_name = False
        self.can_snmp = False
        self.overwrite = self.config.get_item("overwrite")
        self.userat = None
        self.short = None
        self.ip_addr_list = None
        self.alias_list = None
        self.fqdn = None
        # self.logger.info(f"Starting {address}")

    def identify(self):
        et = ElapsedTime("identify " + str(self.address))
        self.identify_inner()
        self.logger.debug(f"ElapsedTime {et}")

    def identify_inner(self):
        r = Runner(f"ping -q -c 4 -w 4 -i .25 -W .25 {self.address}", timeout=5, silent=True)
        self.can_ping = r.success
        if not self.can_ping:
            self.logger.debug(f"Can't ping {self.address}")
            return
        self.logger.info(f"Pinged {self.address}")
        try:
            self.fqdn, self.alias_list, self.ip_addr_list = socket.gethostbyaddr(str(self.address))
            self.logger.info(f"Reverse DNS for Address: {self.address} Hostname: {self.fqdn}")
            self.can_name = True
        except socket.herror as e:
            self.logger.error(f"Reverse address lookup failed for {self.address} {e}", stack_info=True, exc_info=True)
        r2 = Runner(f"uname -n", timeout=5, userat=f"root@{self.address}", silent=True)
        self.can_ssh = r2.success
        if r2.success:
            self.uname_hostname = r2.so_lines[0]
        if r2.success and self.fqdn is None:
            self.fqdn = self.uname_hostname
            self.logger.info(f"uname -h for Address: {self.address} Hostname: {self.fqdn}")
            self.can_name = True
        if r2.success and self.fqdn != self.uname_hostname:
            self.logger.warning(
                f"Name conflict for {self.address} Reverse DNS: {self.fqdn} Uname: {self.uname_hostname}")
            self.can_name = False
        if self.fqdn is None:
            self.logger.warning(f"Can't find fqdn/hostname for {self.address}")
            self.can_name = False
            return
        localhost = self.config.get_item("localhost.fqdn")
        self.is_localhost = localhost == self.fqdn

        self.short = self.fqdn.split(".")[0]
        self.userat = f"root@{self.fqdn}"
        r = Runner(f"hostnamectl --json pretty", userat=self.userat, timeout=4, silent=True)
        self.can_ssh = r.success
        if r.success:
            self.hostname_info = Config.text_to_config(r.so_str)
            self.logger.info(r)
        r = Runner(f"uname -s", userat=self.userat, timeout=4, silent=True)
        if r.success:
            self.kernel_name = r.so_lines[0].strip()  # "Linux","Darwin"
        else:
            self.kernel_name = "unknown"
        r = Runner(f"arp {self.address}", timeout=4, silent=True)  # localhost not userat
        if r.success:
            for line in r.so_lines:
                parts = line.split()
                if parts[0] == "Address":
                    continue
                if parts[1] == "ether":
                    self.mac_address = parts[2].upper()
                    self.oui = self.mac_address[:8]
                    self.logger.info(f"{self.address=} {self.mac_address=} {self.oui=}")
        self.community = self.config.get_item("__SNMP_COMMUNITY__", secrets=True, default="public")
        cmd = ["snmpget", "-c", self.community, "-v2c", self.fqdn, "-Ovq", "iso.3.6.1.2.1.1.5.0"]
        r = Runner(cmd, timeout=4, silent=True)
        self.can_snmp = r.success

    def create_dev_map(self):
        """Builds a mapping between /dev/sdx and /dev/disk/by-id names"""
        if not self.can_ssh:
            return

        r = Runner("ls -l /dev/disk/by-id/*", userat=self.userat, timeout=4)
        if r.success:
            for line in r.so_lines:
                if "->" in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "->":
                            by_id = parts[i - 1]
                            dev = parts[i + 1].replace("../../", "/dev/")
                            self.map_dev_to_id[dev] = by_id
                            break

    def get_dev_id(self, dev: str):
        """return disk/by_id if found, else dev unchanged"""
        if dev in self.map_dev_to_id:
            return self.map_dev_to_id[dev]
        return dev

    def process_host(self):
        et = ElapsedTime("process_host " + str(self.address))
        self.process_host_inner()
        self.logger.debug(f"ElapsedTime {et}")

    def process_host_inner(self):

        if not (self.can_ping and self.can_name):
            self.logger.debug(f"Skip Processing {self.address} {self.can_name=} {self.can_ping=} {self.can_ssh=}")
            return

        if not self.determine_group():
            self.logger.info(
                f"Skip Processing (no group) {self.address} {self.can_name=} {self.can_ping=} {self.can_ssh=}")
            return

        # self.logger.info(f"Start Processing {self.address} {self.can_name=} {self.can_ping=} {self.can_ssh=}")

        self.create_dev_map()

        self.write_host_file()
        self.write_host_template()
        self.logger.info(f"End Processing {self.address} {self.can_name=} {self.can_ping=} {self.can_ssh=}")

    def determine_group(self) -> bool:
        # lst = self.config.to_list()
        # self.logger.info(lst)
        if self.kernel_name in self.config:
            self.group_name = self.config.get_item(self.kernel_name)
        else:
            self.logger.error(f"Can't find group for {self.kernel_name}, dropping {self.address} {self.fqdn}")
            return False

        self.logger.info(f"{self.address} {self.short} assigned group {self.group_name}")
        explicit_group_assignments = Config(self.config.get_item("explicit_group_assignments", default={}))
        group_name_init = self.group_name
        self.logger.info(f"searching {str(self.address)=}, {self.short=}, {self.mac_address=}, {self.oui=}")
        group_name_new = explicit_group_assignments.get_item(str(self.address), self.short, self.mac_address, self.oui,
                                                             default=group_name_init)
        if group_name_init != group_name_new:
            self.group_name = group_name_new
            self.logger.info(f"{self.address} {self.short} group reassigned {group_name_init} -> {self.group_name}")

        if self.group_name in self.group_paths:
            self.group_path = self.group_paths[self.group_name]
        else:
            if self.group_name.lower().startswith(("drop", "!")):
                self.logger.warning(f"Group {self.group_name}, dropping {self.address} {self.short}")
                return False
            self.logger.error(f"Group {self.group_name} does not exist, dropping {self.address} {self.short}")
            return False
        return True

    def write_host_file(self):
        host_file_path: Path = self.group_path / f"{self.fqdn}.json"
        if host_file_path.exists() and not self.overwrite:
            self.logger.warning(f"Host file {host_file_path} is already exists -- not overwriting")
            return
        additional_tests = Config(self.config.get_item("additional_per_node", "additional_tests", default={}))
        data = additional_tests.get_item(str(self.address), self.short, self.mac_address, self.oui, default={})

        ncon = Config(data)
        ncon.set_item("fqdn", self.fqdn)
        ncon.set_item("discovered_ipv4", str(self.address))
        ncon.set_item("discovered_mac", str(self.mac_address))
        ncon.set_item("discovered_oui", str(self.oui))

        ncon.set_item("short_name", self.short)
        templates = ncon.get_item("templates", default=[])
        templates.append(f"auto_{self.fqdn}")
        ncon.set_item("templates", templates)
        ncon.to_json_file(host_file_path, indent=4)
        self.logger.info(f"Host config for {self.fqdn} added at {host_file_path}")

    def add_test(self, d: dict[str, Any]):
        self.auto_tests.append(d)
        self.logger.info(f"{self.short} Adding test {len(self.auto_tests)} {d} ")

    def add_template(self, d: str):
        self.auto_templates.append(d)
        self.logger.info(f"{self.short} Adding template {len(self.auto_templates)} {d} ")

    def write_host_template(self):
        auto_file_path: Path = self.host_template_dir / f"auto_{self.fqdn}.json"
        if auto_file_path.exists() and not self.overwrite:
            self.logger.warning(f"Host file {auto_file_path} is already exists -- not overwriting")
            return
        ncon = Config()

        self.add_ping_intranet()
        self.add_linux_common()
        self.add_snmp()
        self.add_sensors()

        self.add_df()
        self.add_smart()
        self.add_zfs_stuff()
        self.add_cockpit()
        self.add_sestatus()
        self.add_apcaccess()
        self.add_nfs()
        self.add_smb()
        self.add_http()
        self.add_time_machine()

        ncon.set_item("intended_for", self.fqdn)
        ncon.set_item("tests", self.auto_tests)
        ncon.set_item("templates", self.auto_templates)
        ncon.to_json_file(auto_file_path, indent=4)
        self.logger.info(f"Host template for {self.fqdn} added at {auto_file_path}")

    def add_ping_intranet(self):
        d = PingDiscovery(self)
        d.discover()

    def add_linux_common(self):
        d = LinuxCommonDiscovery(self)
        d.discover()

    def add_snmp(self):
        d = SNMPDiscovery(self)
        d.discover()

    def add_sensors(self):
        d = SensorsDiscovery(self)
        d.discover()

    def add_cockpit(self):
        if self.can_ssh:
            r = Runner(f"systemctl is-enabled cockpit", userat=self.userat, timeout=5)
            if r.success:
                self.add_template("Cockpit")

    # noinspection HttpUrlsUsage
    def add_http(self):
        urls = [f"http://{self.fqdn}", f"https://{self.fqdn}"]
        if self.is_localhost:
            # don't test santa interface across instances
            # tends to pick up development testing and generate extra tests
            # which fail when development activity pauses or stops
            urls.append(f"http://{self.fqdn}:4242/")
        for url_ in urls:
            try:
                response: Response = get(url_, timeout=5)
                code = response.status_code
                ok = code in [200]
                self.logger.info(f"Response from {url_=} -> {code=} {ok=}")
                if ok:
                    self.add_test(
                        {
                            "test_type": "HTTPTest",
                            "url": url_
                        })
            except Exception as e:
                self.logger.warning(f"Exception while trying to get {url_=} -> {e}")

    def add_nfs(self):
        if self.can_ssh:
            r = Runner(f"exportfs -s", userat=self.userat, timeout=5)
            if r.success:
                share_list = [line.split()[0] for line in r.so_lines]
                if len(share_list) > 0:
                    self.add_test(
                        {
                            "test_type": "Shares_NFS",
                            "shares": share_list
                        })

    def add_smb(self):
        if self.can_ssh:
            smb_username = self.config.get_item("__SECRET__SMB_USER", secrets=True, default=None, allow_none=True)
            smb_password = self.config.get_item("__SECRET__SMB_PASS", secrets=True, default=None, allow_none=True)
            if smb_username and smb_password:
                r = Runner(f"smbclient -L  {self.fqdn} -U {smb_username} --password {smb_password}", timeout=5)
            else:
                r = Runner(f"smbclient -L  {self.fqdn}", timeout=5)
            if r.success:
                share_list = [line.strip().split()[0] for line in r.so_lines if "Disk" in line]
                if smb_username and smb_password:
                    self.add_test(
                        {
                            "test_type": "Shares_SMB",
                            "shares": share_list,
                            "smb_username": "{{__SECRET__SMB_USER}}",
                            "smb_password": "{{__SECRET__SMB_PASS}}",
                        })
                else:
                    self.add_test(
                        {
                            "test_type": "Shares_SMB",
                            "shares": share_list,
                        })

    def add_sestatus(self):
        if self.can_ssh:
            r = Runner(f"sestatus", userat=self.userat, timeout=5)
            if r.success:
                self.add_test({"test_type": "SE_Status"})

    # noinspection PyTestUnpassedFixture
    def add_smart(self):
        if self.can_ssh:
            r = Runner(f"smartctl --scan --json", userat=self.userat, timeout=8)
            #  "devices": [
            #     {
            #       "name": "/dev/sda",
            #       "info_name": "/dev/sda",
            #       "type": "scsi",
            #       "protocol": "SCSI"
            #     },
            #     {
            #       "name": "/dev/sdb",
            #       "info_name": "/dev/sdb",
            if r.success:
                txt = '\n'.join(r.so_lines)
                # self.logger.info(f"{txt}")
                con = Config(Config.text_to_dict(txt))
                if "devices" in con:
                    devs = con.get_item("devices")
                    for dev_ in devs:
                        dev_name = dev_.get("name")
                        by_id = self.get_dev_id(dev_name)
                        cmd = {
                            "dev": by_id,
                            "dev_raw": dev_name,
                            "test_type": "SmartCtl"
                        }
                        self.add_test(cmd)

    def add_apcaccess(self):
        if self.can_ssh:
            r = Runner("apcaccess -u", userat=self.userat, timeout=5, retries=1)
            if r.success:
                cmd = {
                    "test_type": "ApcAccess"
                }
                self.add_test(cmd)

    def add_df(self):
        if self.can_ssh:
            r = Runner(f"cat /etc/fstab", userat=self.userat, timeout=5)
            if r.success:
                # #
                # # /etc/fstab
                # # Created by anaconda on Thu Mar 14 21:16:25 2024
                # #
                # # Accessible filesystems, by reference, are maintained under '/dev/disk/'.
                # # See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info.
                # #
                # # After editing this file, run 'systemctl daemon-reload' to update systemd
                # # units generated from this file.
                # #
                # /dev/mapper/rhel_kylo-root /                       xfs     defaults        0 0
                # UUID=abf33b68-bf8c-4a55-8189-98d9ec34e699 /boot                   xfs     defaults        0 0
                # UUID=925A-976A          /boot/efi               vfat    umask=0077,shortname=winnt 0 2
                # /dev/mapper/rhel_kylo-home /home                   xfs     defaults        0 0
                # /dev/mapper/rhel_kylo-swap none                    swap    defaults        0 0
                for line in r.so_lines:
                    if line.startswith(("#", ";")):
                        continue
                    parts = line.split()
                    if len(parts) >= 2:
                        path = parts[1]
                        path.strip()
                        if path in ["none", "/proc", "swap"]:
                            continue
                        instance_name = path.replace("/", "_")
                        cmd = {
                            "test_type": "DiskFree",
                            "path": path,
                            "instance_name": instance_name
                        }
                        self.add_test(cmd)

    def add_time_machine(self):
        if not self.can_ssh:
            return
        r = Runner("zfs list -H -o mountpoint", userat=self.userat, timeout=10)
        if not r.success:
            return
        for line in r.so_lines:
            r2 = Runner(f"ls {line}/*bundle/com.apple.TimeMachine.MachineID.plist", userat=self.userat,
                        timeout=10)
            pth = Path(line)
            nam = Path(pth.name).name
            if r2.success:
                cmd = {
                    "test_type": "TimeMachine",
                    "path": line,
                    "instance_name": nam
                }
                self.add_test(cmd)

    # noinspection PyTestUnpassedFixture
    def add_zfs_stuff(self):
        if not self.can_ssh:
            return
        r = Runner("zpool list -H -o name", userat=self.userat, timeout=10)
        if not r.success:
            return
        cmd = {
            "test_type": "ZFS_Version",
            "period": 900
        }
        self.add_test(cmd)
        for pool_name in r.so_lines:
            cmd = {
                "test_type": "Zpool_Status",
                "instance_name": pool_name,
                "period": 300,
                "pool": pool_name
            }
            self.add_test(cmd)
            cmd = {
                "test_type": "Zpool_Free",
                "instance_name": pool_name,
                "period": 300,
                "pool": pool_name
            }
            self.add_test(cmd)
        zfs_volumes_processed = []
        r = Runner("cat /etc/pyznap/pyznap.conf", userat=self.userat, timeout=4)
        if r.success:
            data = Config(Config.text_to_dict('\n'.join(r.so_lines)))
            for vol_name in data.keys():
                sdata = data[vol_name]
                if sdata.get("snap", "no") == "yes":
                    cmd = {
                        "par_0": vol_name,
                        "test_type": "ZFS_Snapshots_Primary"
                    }
                    self.add_test(cmd)
                    zfs_volumes_processed.append(vol_name)
        r = Runner("zfs list -H -o name", userat=self.userat, timeout=10)
        zfs_volumes = r.so_lines
        for vol_name in zfs_volumes:
            # Looking for vols with no child vols
            matched = False
            for vol_name2 in zfs_volumes:
                if vol_name == vol_name2:
                    continue
                if vol_name2.startswith(vol_name):
                    matched = True
                    break
            if matched:
                continue
            if vol_name in zfs_volumes_processed:
                continue
            if not self.check_age_of_snapshots(vol_name):
                continue
            cmd = {
                "par_0": vol_name,
                "test_type": "ZFS_Snapshots_Copy"
            }
            self.add_test(cmd)
            zfs_volumes_processed.append(vol_name)

    def check_age_of_snapshots(self, vol) -> bool:
        zfs_commands = ["/sbin/zfs", "list", "-H", "-t",
                        "snapshot", "-r",
                        "-d1", "-o", "name,creation", "-S", "creation", vol]
        r = Runner(zfs_commands, userat=self.userat, timeout=15)
        lines = r.so_lines
        ret = r.ret
        if ret != 0:
            res_str = f"UNKNOWN - Command Error 0x{ret:04x} {vol}"
            self.logger.warning(res_str)
            return False
        else:
            minutes = 60
            crit_t = timedelta(0, minutes * 60)

            datetime_now = datetime.now()
            if lines:
                for line in lines:
                    parts = line.split('\t')
                    self.logger.info(parts)
                    # name = parts[0]
                    if len(parts) > 1:
                        dat_a = parts[1]
                        dt = datetime.strptime(dat_a, '%a %b %d %H:%M %Y')
                        age = datetime_now - dt
                        self.logger.info(f"Snapshot {vol} age {age} minutes")
                        return age <= crit_t
        return False


class MakeListsEmbedded:

    def __init__(self, santa_config: Config, np: NorthPole):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.np = np
        self.santa_config = santa_config

        self.candidate_hosts: list[HostCreator] = []

        self.group_path_dict: dict[str, Path] = dict()

        self.is_root = os.getuid() == 0

        # local_info = Info("localhost")
        # local_info.dump()

        # setup any program specific command line arguments
        # self.parser.add_argument('--dir', help="Dir to generate files into", dest='santa_config_dir',
        #                          default=str(assumed_dir))
        # self.parser.add_argument('--config', help="Configuration File", dest='config', default=None)
        # self.parser.add_argument('--threads', help="Number of threads in pool", dest='num_threads', type=int,
        #                          default=32)

        # create output dir if missing

        if not self.np.santa_discovery_config_dir.exists():
            self.np.create_discovery_dirs()

        self.logger.info(f"Santa_IW config output to {self.np.santa_discovery_config_dir}")

        self.logger.info(f"Santa_IW discovery input config is {self.np.user_discovery_file}")
        self.info = Info()
        self.localhost_config = self.info.to_config("localhost.")
        self.discovery_config = Config(self.np.user_discovery_file, self.localhost_config)

        self.worker_pool = ThreadPoolExecutor(max_workers=32)  # fixme config

        self.create_dirs()
        self.loop_over_scans()
        #

    def create_dirs(self) -> None:
        # create group subdirectories below HOST_NODES
        groups: dict[str, Any] = self.discovery_config.get_item("groups")
        for group, group_config in groups.items():
            # if the given group name contains a slash "HOSTS/RPI"
            # this will magically create nested groups
            # group_short is just the last part of this name
            group_short = group.split('/')[-1]
            path = self.np.santa_discovery_nodes_dir / group
            path.mkdir(parents=True, exist_ok=True)
            self.group_path_dict[group] = path
            # data in config should just reflect th last part of this name
            con = Config(dict({
                "short_name": group_short,
                "tests": [],
                "templates": []
            }), group_config)

            con.to_json_file(path / f'__{group_short}.json', indent=4)
            self.logger.info(f"Santa_IW group path {group} at {path}")

    def loop_over_scans(self):
        scan_defaults = self.discovery_config.get_item("scan_defaults")
        scans = self.discovery_config.get_item("scans")
        for scan in scans:
            scan_config = Config(scan, scan_defaults, self.discovery_config)
            self.perform_one_scan(scan_config)

        self.logger.info(f"Phase one, identify hosts")
        futures = [self.worker_pool.submit(candidate.identify) for candidate in self.candidate_hosts]
        for future in futures:
            future.result()
        self.logger.info(f"Phase two, process hosts")
        futures = [self.worker_pool.submit(candidate.process_host) for candidate in self.candidate_hosts if
                   candidate.can_ping]
        for future in futures:
            future.result()

    def perform_one_scan(self, scan_config: Config):
        first_ip = scan_config.get_item("first_ip")
        last_ip = scan_config.get_item("last_ip")
        if first_ip.lower() == "auto":
            local_info = Info("localhost")
            r = Runner("ip -oneline addr", timeout=5)
            for line in r.so_lines:
                if local_info.ip in line:
                    # 2: enp0s31f6    inet 10.0.4.32/24 brd 10.0.4.255 scope global dynamic noprefixroute enp0s31f6\       valid_lft 3076sec preferred_lft 3076sec
                    parts = line.split()
                    cidr_range = parts[3]
                    break
            else:
                self.logger.error(f"Could not find ip address {local_info.ip} in {r.so_lines}")
                exit(1)
            network = IPv4Network(cidr_range, strict=False)
            net_addr_start = network.network_address
            net_addr_end = network.broadcast_address
            int_net_addr_start = self.ipv4_to_int(net_addr_start) + 1
            int_net_addr_end = self.ipv4_to_int(net_addr_end) - 1
            # given huge range, limit to x.y.0.1 through x.y.4.254
            int_net_addr_end = min(int_net_addr_end, int_net_addr_start + (5 * 256) - 3)
            first_address = IPv4Address(int_net_addr_start)
            last_address = IPv4Address(int_net_addr_end)
            self.logger.info(f"Santa_IW auto will scan {first_address} -> {last_address}")
        else:
            first_address = IPv4Address(first_ip)
            last_address = IPv4Address(last_ip)
        self.logger.info(
            f"{first_address=} {first_address.packed=} {first_address.compressed=} {last_address.exploded=} {last_address.version=}")
        first_int = self.ipv4_to_int(first_address)
        last_int = self.ipv4_to_int(last_address)
        num = last_int - first_int
        self.logger.info(f"Scanning {num=} addresses {first_address=} {last_address=}")
        for int_addr in range(first_int, last_int + 1):
            ip = IPv4Address(int_addr)
            self.logger.info(f"Scanning {ip=} {int_addr=:x}")
            x = HostCreator(address=ip, config=scan_config, host_template_dir=self.np.santa_discovery_templates_dir,
                            group_paths=self.group_path_dict)
            self.candidate_hosts.append(x)

    # noinspection PyMethodMayBeStatic
    def ipv4_to_int(self, ipv4: IPv4Address) -> int:
        byts = ipv4.packed
        v: int = 0
        for byte in byts:
            v = v * 256 + byte
        return v


# noinspection DuplicatedCode
class Discovery(Subassembly):

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        self.plugin_type_map: dict[str, PluginType] = {}
        self.plugin_instance_map: dict[str, PluginBase] = {}
        self.plugin_names_not_found: set[str] = set()
        # failure within a test type does not imply factory failure
        self._propagate_child_stats_in_overall = False
        self.np = NorthPole()

    def start(self) -> None:
        # fixme add rotation later
        if self.np.santa_discovery_config_dir.is_dir():
            self.log_internal_status(Status.OK, message=f"Keeping Previous Network Discovery at {self.np.santa_discovery_config_dir}")
        else:
            et=ElapsedTime("discovery")
            self.log_internal_status(Status.MAINT,message="Performing network discovery")
            _ = MakeListsEmbedded(self.config(), self.np)
            et.stop()
            self.log_internal_status(Status.OK,message=f"Net discovery completed {et}")

    def report(self) -> str:
        out = super().report()
        out += "\n"
        return out
