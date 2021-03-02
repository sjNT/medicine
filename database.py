import contextlib
import mysql.connector as mc


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


db = mc.connect(user='tusur', password='ImXAaJRqvrI8r3r', host='109.123.144.99', port='3306', database='medicine')
