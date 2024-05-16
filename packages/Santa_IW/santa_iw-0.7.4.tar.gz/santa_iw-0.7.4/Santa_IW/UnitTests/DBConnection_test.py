import math
import os
import unittest
from pathlib import Path

from Santa_IW.DBConnection import DBConnection

dbpath = Path("/tmp/test_SQLite.db")


class MyTestCase(unittest.TestCase):
    # noinspection PyUnreachableCode
    def test_SQLite_clean(self):
        if dbpath.exists():
            os.remove(dbpath)
        db = DBConnection(dbpath)
        self.assertIsNotNone(db)
        return  # FIXME #169
        with db as cur:
            res = cur.execute("SELECT name FROM sqlite_master")
            a = res.fetchone()
            print(a)
            self.assertIsNone(a)

            cur.execute("""CREATE TABLE asamples (
                name text,
                 count integer,
                 time float,
                 value float
                 )        """)
            tables = db.all_tables()
            print(tables)
            self.assertEqual(('asamples',), tables)  # add assertion here
        db.close()

    # noinspection PyUnreachableCode
    def test_repopen(self):
        if dbpath.exists():
            os.remove(dbpath)
        db = DBConnection(dbpath)
        self.assertIsNotNone(db)
        return  # FIXME #169
        with db as cur:
            cur.execute("""CREATE TABLE asamples (
                name text,
                 count integer,
                 time float,
                 value float
                 )        """)
            cur.execute(f"INSERT INTO asamples VALUES ('samplename1',42,{now},{math.pi})")
            cur.execute(f"INSERT INTO asamples VALUES ('samplename2',42,{now},{math.pi / 2})")
        db.close()

        db2 = DBConnection(dbpath)
        with db2 as cur:
            tables = db2.all_tables()
            print(tables)
            self.assertEqual(('asamples',), tables)  # add assertion here
            cur.execute("SELECT * FROM asamples")
            recs = cur.fetchall()
            print(recs)
            self.assertEqual(2, len(recs))
            self.assertEqual(('samplename1', 42, now, math.pi), recs[0])
            self.assertEqual(('samplename2', 42, now, math.pi / 2), recs[1])

            self.assertEqual(True, db2.has_table('asamples'))
            self.assertEqual(False, db2.has_table('dsamples'))
        db2.close()


if __name__ == '__main__':
    unittest.main()
