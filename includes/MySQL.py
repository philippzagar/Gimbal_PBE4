# Python 3 Implementation
# Error: Package pymysql is not found - nur einmal aufgetreten
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb as MySQL

class Database:

    host = 'localhost'
    user = 'root'
    password = 'raspberry'
    db = 'gimbal'

    def __init__(self):
        self.connection = MySQL.connect(self.host, self.user, self.password, self.db)
        self.cursor = self.connection.cursor()

    def insert(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except:
            self.connection.rollback()

    def query(self, query):
        cursor = self.connection.cursor( MySQL.cursors.DictCursor )
        cursor.execute(query)

        return cursor.fetchall()

    def __del__(self):
        self.connection.close()