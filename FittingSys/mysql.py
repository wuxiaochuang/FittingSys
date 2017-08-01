import MySQLdb


class mysql(object):
    def __init__(self):
        self.db_connect = MySQLdb.connect(
            host="localhost",
            port=3306,
            user="root",
            passwd="123456",
            db="recommend_db",
            charset="utf8"
        )
        self.db_cursor = self.db_connect.cursor()

    def db_create(self,table_name):
        self.db_cursor.execute(table_name)

    def db_insert(self,t_insert):
        self.db_cursor.execute(t_insert)
        self.db_connect.commit()

    def db_alter(self,t_alter):
        self.db_cursor.execute(t_alter)

    def db_select(self,t_select):
        self.db_cursor.execute(t_select)
        values = list(self.db_cursor.fetchall())
        return values

    def db_drop(self,drop_name):
        self.db_cursor.execute(drop_name)

    def db_show(self,show_name):
        self.db_cursor.execute(show_name)

    def db_update(self,update_name):
        self.db_cursor.execute(update_name)
        self.db_connect.commit()

    def db_close(self):
        self.db_cursor.close()
        self.db_connect.commit()
        self.db_connect.close()
