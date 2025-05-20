import contextlib
import mysql.connector as mc


class DatabaseExecutor:

    @staticmethod
    def exec_query(query, param=(), retrieve_id=False, fetchone=False, dictionary=False):
        print(query, param)
        with contextlib.closing(db.cursor(dictionary=dictionary)) as cur:
            cur.execute(query, param)
            if fetchone:
                data = cur.fetchone()
            else:
                data = cur.fetchall()
            if retrieve_id:
                data = cur.lastrowid
        db.commit()
        return data


db = mc.connect(user='tusur', password='ImXAaJRqvrI8r3r', host='127.0.0.1', port='3306', database='medicine')
