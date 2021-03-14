import pymysql as mysql
from os import environ
#import mysql.connector    # (add to requirements.txt)

class DBTypeError(TypeError):
    # raised when there's a database type error (currently supports 'str', 'float', 'int', 'None' and 'bool', datetime.datetime() and time.time() soon to come)
    pass

class Database:
    db = None
    dbc = None
    autocommit = True
    def __init__(self, host, user, pwd, data, autocommit=True):
        self.db = mysql.connect(host=host, user=user, password=pwd, database=data)
        self.dbc = self.db.cursor()
        self.autocommit = autocommit
    def execute(self, query):
        self.dbc.execute(query)
        try:
            res = self.dbc.fetchall()
            if self.autocommit:
                self.db.commit()
            return res
        except Exception as e:
            return None
    def close(self):
        self.db.close()
    def insertUser(self, table, fields):
        if not isinstance(table, str):
            raise TypeError("'table' param must be type of 'str'.")
        if not isinstance(fields, dict):
            raise TypeError("'fields' param must be type of 'dict', ie. Dict['field'] = value")
        length = len(fields)
        if length == 0:
            raise DBTypeError("'fields' parameter must not be empty.")
        query = f"INSERT INTO {table} ("
        i = 0
        querypt1 = ''
        querypt2 = ''
        for key in fields:
            i += 1
            key = _escape(key)
            if not isinstance(key, str):
                raise TypeError("A 'fields' key must be type of 'str' only.")
            if isinstance(fields[key], str):
                fields[key] = _escape(fields[key])
                querypt1 += f"{key}"
                querypt2 += f"'{fields[key]}'"
            elif isinstance(fields[key], int) or isinstance(fields[key], float) or isinstance(fields[key], bool):
                querypt1 += f"{key}"
                querypt2 += f"{fields[key]}"
            elif fields[key] is None:
                querypt1 += f"{key}"
                querypt2 += f"NULL"
            else:
                raise TypeError("A 'fields' value must be type of 'int', 'float', 'bool', 'str' or 'None' only.")
            if i != length:
                querypt1 += ","
                querypt2 += ","
        try:
            query += querypt1 + ") VALUES (" + querypt2 + f")"
            self.dbc.execute(query)
            return (0, "Pass")
        except Exception as e:
            return e
    def updateUser(self, table, fields, user):
        if not isinstance(table, str):
            raise TypeError("'table' param must be type of 'str'.")
        if not isinstance(fields, dict):
            raise TypeError("'fields' param must be type of 'dict', ie. Dict['field'] = value")
        if not isinstance(user, str):
            raise TypeError("'user' param must be type of 'str'.")
        length = len(fields)
        if length == 0:
            raise DBTypeError("'fields' parameter must not be empty.")
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
            elif fields[key] is None:
                query =+ f"{key} = NULL"
            else:
                raise TypeError("A 'fields' value must be type of 'int', 'float', 'bool', 'str' or 'None' only.")
            if i != length:
                query += ","
        user = _escape(user)
        query += f" WHERE name = '{user}'"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            return (0, "Pass")
        except Exception as e:
            return e
    def deleteUser(self, table, user):
        if not isinstance(table, str):
            raise TypeError("'table' param must be type of 'str'.")
        if not isinstance(user, str):
            raise TypeError("'user' param must be type of 'str'.")
        query = f"DELETE FROM {table} WHERE name = '{user}'"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            return (0, "Pass")
        except Exception as e:
            return e
    def getUserData(self, table, user):
        if not isinstance(table, str):
            raise TypeError("'table' param must be type of 'str'.")
        if not isinstance(user, str):
            raise TypeError("'user' param must be type of 'str'.")
        query = f"SELECT * FROM {table} WHERE name = '{user}'"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            return ((0, "Pass"), self.dbc.fetchall())
        except Exception as e:
            return (e, None)

def _escape(text):
    return text.replace("'", "''")

if __name__ == "__main__":
    # *kasnije, ide citanje iz ENV varijable ovog dela ---> odg: svakako je privremeno, za testiranje
    """
    envget = environ.get
    HOST = envget("HOST")
    USER = envget("USER")
    PASS = envget("PASS")
    DATA = envget("DATA")
    """
    USER = "web"
    HOST = "localhost"
    PASS = "webwebweb"
    DATA = "flaskweb"
    db = Database(HOST, USER, PASS, DATA)
    #x = db.execute("SELECT number,number2 FROM users WHERE name = 'test'")
    x = db.getUserData("users", "test")
    print(x) # error?
    x = db.update("users", {"number": 77, "number2": 127.4}, "test")
    print(x) 
    #x = db.execute("SELECT number,number2 FROM users")
    x = db.getUserData("users", "test")
    print(x) # error? & output
    x = db.insert("users", {"name":"test8","pwd":"x","salt":"y","token":"z","number":310,"number2":3.13421})
    print(x) # error?
    x = db.getUserData("users", "test8")
    print(x) # error? & output
    db.close() # close the connection
