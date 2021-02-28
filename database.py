import sqlite3
from const import proj_path
import contextlib


class DatabaseExecutor:

    @staticmethod
    def exec_query(query, param=None, retrieve_id=False, fetchone=False):
        print(query, param)
        if param:
            query = query % param
        with contextlib.closing(db.cursor()) as cur:
            cur.execute(query)
            if fetchone:
                data = cur.fetchone()
            else:
                data = cur.fetchall()
            if retrieve_id:
                data = cur.lastrowid
        db.commit()
        return data


db = sqlite3.connect(proj_path / 'medicine.sqlite')
