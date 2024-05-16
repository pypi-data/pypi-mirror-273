from dataclasses import dataclass
from io import BytesIO
from threading import Thread
from time import sleep, time
from typing import Optional, NamedTuple

import pandas as pd
from libsrg.Config import Config
from libsrg.ElapsedTime import ElapsedTime
from libsrg.Statistics.ADStatsBase import ADStatsBase
from libsrg.Statistics.AnalogStatsBase import AnalogStatsBase, AStatsRecord
from libsrg.Statistics.AnalogStatsSlidingWindow import AnalogStatsSlidingWindow
from libsrg.Statistics.DiscreteStatsBase import DiscreteStatsBase, DStatsRecord
from pandas import DataFrame
from sqlalchemy import Engine, Connection, text, CursorResult

from Santa_IW.DBConnection import DBConnection
from Santa_IW.Status import Status
from Santa_IW.Subassembly import Subassembly


@dataclass
class StatusRecord:
    name: str
    time: float
    value: str


class DataRecording(Subassembly):
    """
    Data Recording subassembly

    """

    def __init__(self, instance_config: Config, short_name: str, parent: Subassembly):
        super().__init__(instance_config=instance_config, parent=parent,
                         short_name=short_name)  # super defines self.logger
        self.sep = self.config().get_item("tree_name_separator")
        self.db_filename = self.config().get_item("data_recording_db")
        self.db_thread: Optional[Thread] = None
        self._connection: Optional[DBConnection] = None
        self.db_pending: list[str] = []
        self.db_per_sec = AnalogStatsSlidingWindow(self.prefix_name("Mean db writes/s"), window=3600)
        self.data_recording_interval_sec = self.config().get_item("data_recording_interval_sec")
        self.data_recording_keep_days = float(self.config().get_item("data_recording_keep_days"))
        self.statistics_dict: [str, ADStatsBase] = {}

    def get_dbconnection(self) -> DBConnection:
        if self._connection is None:
            try:
                self._connection = DBConnection(self.db_filename)
                self.create_tables()
            except Exception as e:
                self.logger.error(f"Failed to connect to database: {e}", exc_info=True, stack_info=True)
                raise e
        return self._connection

    def get_db_engine(self) -> Engine:
        return self.get_dbconnection().engine()

    def get_db_connect(self) -> Connection:
        return self.get_dbconnection().engine().connect()

    def start(self) -> None:
        self.set_annotation("Setting up Data Recording...")
        self.log_internal_status(Status.OK, "Started", assess=True)

        Subassembly.register_global_status_observer(self.observe_subsystem_status)
        DiscreteStatsBase.register_class_callback(self.observe_discrete_stats)
        AnalogStatsBase.register_class_callback(self.observe_analog_stats)

        self.set_annotation("Done")
        self.log_internal_status(Status.OK, "Done", assess=True)
        # self.logger.info("Finished")

    # noinspection PyUnusedLocal
    def observe_subsystem_status(self, child: Subassembly, status: Status, attention: bool, assess=True) -> None:
        msg = f"Observing {child.short_name()} {status=} {attention=}"
        now = time()
        cmd = f"INSERT INTO ssamples VALUES ({child.name()!r},{now},{status.name!r})"
        self.db_pending.append(cmd)
        self.set_annotation(msg)

    def observe_discrete_stats(self, record: DStatsRecord):
        msg = f"Observing DS {record}"
        self.name_prefix_check(record.name)
        self.set_annotation(msg)
        cmd = f"INSERT INTO dsamples VALUES ({record.name!r},{record.count},{record.time},{record.value!r})"
        self.db_pending.append(cmd)

    def observe_analog_stats(self, record: AStatsRecord):
        msg = f"Observing AS {record}"
        self.name_prefix_check(record.name)
        self.set_annotation(msg)
        cmd = f"INSERT INTO asamples VALUES ({record.name!r},{record.count},{record.time},{record.value})"
        self.db_pending.append(cmd)

    def name_prefix_check(self, name):
        if self.sep not in name:
            self.log_internal_status(Status.WARNING, f"No name prefix for {name}", assess=True)

    def create_tables(self):
        tables = self.get_dbconnection().all_tables()
        self.logger.info(f"Existing tables: {', '.join(tables)}")
        if not self.get_dbconnection().has_table("asamples"):
            self.logger.info("Creating asamples table")
            with self.get_db_connect() as cur:
                cur.execute(text("""CREATE TABLE asamples (
                    name text,
                     count integer,
                     time float,
                     value float
                     )        """))
                cur.commit()

        if not self.get_dbconnection().has_table("dsamples"):
            self.logger.info("Creating dsamples table")
            with self.get_db_connect() as cur:
                cur.execute(text("""CREATE TABLE dsamples (
                    name text,
                     count integer,
                     time float,
                     value text
                     )        """))
                cur.commit()

        if not self.get_dbconnection().has_table("ssamples"):
            self.logger.info("Creating ssamples table")
            with self.get_db_connect() as cur:
                cur.execute(text("""CREATE TABLE ssamples (
                    name text,
                     time float,
                     status text
                     )        """))
                cur.commit()

    def shutdown_instance(self):
        super().shutdown_instance()

    def spawn(self):
        if self.db_thread:
            self.logger.error("Database thread already running")
        else:
            self.db_thread = Thread(target=self.run_in_db_thread, daemon=True, name="DataRecording DB Thread")
            self.db_thread.start()

    def run_in_db_thread(self):
        threshold = self.config().get_item("data_recording_purge_interval")
        purge_timer = ElapsedTime("purge_timer")
        interval_timer = ElapsedTime("actual_interval")
        purge_timer.start()
        while self.subsystem_is_enabled():
            len0 = len(self.db_pending)
            # time since last sample (prevent divide by zero on first pass)
            delta_t = max(interval_timer.current(), 0.1)
            interval_timer.start()
            self.db_per_sec.sample(len0 / delta_t)
            if purge_timer.current() >= threshold:
                purge_timer.start()
                self.logger.info(f"Purge database")
                retention_threshold = time() - self.sc.day * self.data_recording_keep_days
                self.db_pending.append(f"DELETE FROM asamples WHERE time<{retention_threshold}")
                self.db_pending.append(f"DELETE FROM dsamples WHERE time<{retention_threshold}")
                self.db_pending.append(f"DELETE FROM ssamples WHERE time<{retention_threshold}")
            if len0 > 0:
                self.logger.info(f"{len0} database actions to process")
                with self.get_db_connect() as cur:
                    while len(self.db_pending) > 0:
                        cmd = self.db_pending.pop(0)
                        # self.logger.info(f"Processing {cmd}")
                        # noinspection PyUnusedLocal
                        curresult: CursorResult = cur.execute(text(cmd))
                        # self.logger.info(f"Processing {cmd} {curresult.rowcount=} {curresult!r}")
                    cur.commit()

            sleep(self.data_recording_interval_sec)

        self._connection.close()

    def get_astat_image(self, sensor: str):
        cmd = f"SELECT time,value FROM asamples WHERE name='{sensor}'"
        df: DataFrame = pd.read_sql_query(cmd, self.get_db_engine())
        if df.empty:
            self.logger.error(f"No data available for sensor {sensor}")
            return "/dev/null"
        df['DateTime'] = pd.to_datetime(df['time'], unit='s')
        fig = df.plot(y='value', x='DateTime').get_figure()
        img = BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        return img

    def get_sensor_stats(self, outer_name, inner_name) -> ADStatsBase:
        name = self.prefix_name(f"{outer_name}_{inner_name}")
        if name in self.statistics_dict:
            stat = self.statistics_dict[name]
        else:
            stat = AnalogStatsSlidingWindow(name=name, window=100)
            self.statistics_dict[name] = stat
        return stat

    def update_named_tuple(self, tup: NamedTuple, tup_name):
        # noinspection PyProtectedMember
        for key, val in tup._asdict().items():
            stat = self.get_sensor_stats(tup_name, key)
            stat.sample(val)
