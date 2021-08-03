import psycopg2
# database connection


class Database(object):

    def __init__(self, database, user, password, host):
        self.connection = psycopg2.connect(database=database, user=user,
                                           password=password,
                                           host=host, port=5432, application_name="Python memvbot test")
        self.cur = self.connection.cursor()

    def commit(self, query):
        self.cur.execute(query)
        self.connection.commit()

    def one(self, query):
        print(query)
        self.cur.execute(query)
        return self.cur.fetchone()

    def many(self, query, size):
        print(query, size)
        self.cur.execute(query)
        return self.cur.fetchmany(size)

    def all(self, query):
        print(query)
        self.cur.execute(query)
        return self.cur.fetchall()

# TODO: добавить логи выполненных коммитов и запросов