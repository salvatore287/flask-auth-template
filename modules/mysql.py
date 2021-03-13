import pymysql as mysql
#import mysql.connector as mysql

USER = "web"
HOST = "localhost"
PASS = "webwebweb"
DATA = "flaskweb"

class Database:
    db = None
    dbc = None
    def __init__(self, host, user, pwd, data):
        self.db = mysql.connect(host=host, user=user, password=pwd, database=data)
        self.dbc = self.db.cursor()
    def execute(self, query):
        self.dbc.execute(query)
        res = self.dbc.fetchall()
        return res


if __name__ == '__main__':
    db = Database(HOST, USER, PASS, DATA)
    x = db.execute("SELECT NOW() as time")
    print(x[0])
     