import pymysql as mysql
#import mysql.connector as mysql

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
    def update(self, table, fields, user):
        if not isinstance(table, str):
            raise TypeError("'table' param should be type of 'str'.")
        if not isinstance(fields, dict):
            raise TypeError("'fields' param should be type of 'dict', ie. Dict['field'] = value")
        if not isinstance(user, str):
            raise TypeError("'user' param should be type of 'str'.")
        length = len(fields)
        if length == 0:
            raise Exception("'fields' parameter must not be empty.")
        query = f"UPDATE {table} SET "
        i = 0
        for key in fields:
            i += 1
            key = _escape(key)
            if not isinstance(key, str):
                raise TypeError("A 'fields' key must be type of 'str' only.")
            if isinstance(fields[key], str):
                fields[key] = _escape(fields[key])
                query += f"{key} = '{fields[key]}'"
            elif isinstance(fields[key], int) or isinstance(fields[key], float) or isinstance(fields[key], bool):
                query += f"{key} = {fields[key]}"
            else:
                raise TypeError("A 'fields' value must be type of 'int', 'float', 'bool' or 'str' only.")
            if i != length:
                query += ","
        self.dbc.execute(query)

def _escape(text):
    return text.replace("'", "''")

if __name__ == "__main__":
    USER = "web"
    HOST = "localhost"
    PASS = "webwebweb"
    DATA = "flaskweb"
    db = Database(HOST, USER, PASS, DATA)
    x = db.execute("SELECT number,number2 FROM users WHERE name = 'test'")
    print(x[0])
    db.update("users", {"number": 10, "number2": 27.3}, "test")
    x = db.execute("SELECT number,number2 FROM users")
    print(x[0])
    """output:
    (3, 5.0) before updating
    (10, 27.3) after updating
    """
