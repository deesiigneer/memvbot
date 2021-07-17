import sqlite3
# database connection


class Database(object):

    def __init__(self, db_url):
        self.connection = sqlite3.connect(db_url)
        self.cur = self.connection.cursor()

    def commit(self, query):
        self.cur.execute(query)
        self.connection.commit()

    def one(self, query):
        return self.cur.execute(query).fetchone()

    def many(self, query, size):
        return self.cur.execute(query).fetchmany(size)

    def all(self, query):
        return self.cur.execute(query).fetchall()


sql = Database('database/without_name_bot.db')

# TODO: добавить логи выполненных коммитов и запросов