import psycopg2

class Database:
    host = "127.0.0.1"
    user = "postgres"
    passwd = "password"
    db = "test_bd"
    port = '5432'

    def __init__(self):
        try:
            self.connection = psycopg2.connect( host = self.host,
                                                user = self.user,
                                            password = self.passwd,
                                              dbname = self.db,
                                                port = self.port)
            self.cursor = self.connection.cursor()
        except Exception:
            print("Fail to connect to the postgresql database")


    def query(self, query):
        cursor = self.cursor

        if isinstance(query, str):
            cursor.execute(query)
        else:
            print("The query provided is not correct.")
        return cursor.fetchall()

    def __del__(self):
        self.connection.close()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    db = Database()

    query = "select * FROM students"
    result = db.query(query)

    print(result)

    db.close_connection()