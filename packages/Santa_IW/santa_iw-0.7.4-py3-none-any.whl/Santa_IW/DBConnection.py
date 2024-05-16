import logging
from pathlib import Path

from sqlalchemy import create_engine, Engine,text,CursorResult


class DBConnection:
    def __init__(self, file_name: str | Path, in_memory: bool = False):
        self.logger = logging.getLogger(self.__class__.__name__)
        if in_memory:
            self.file_name = ":memory:"
        else:
            self.file_name = Path(file_name).absolute()
        self.logger.info(f"Opening {self.file_name}")
        # self.connection = sqlite3.connect(self.file_name)
        self._engine = create_engine("sqlite:///" + str(self.file_name))

    def engine(self) -> Engine:
        return self._engine

    def close(self):
        self.logger.info("Calling close")
        self._engine.dispose(close=True)

    def all_tables(self) -> list[str]:
        with self.engine().connect() as cur:
            result:CursorResult= cur.execute(text("SELECT name FROM sqlite_master"))
            recs = [row for row in result]
            # self.logger.info(f"All tables: {recs}")
            a = [rec[0] for rec in recs]
            self.logger.info(f"All tables: {', '.join(a)}")
            return list(a)

    def has_table(self, table_name: str) -> bool:
        tables = self.all_tables()
        return table_name in tables
