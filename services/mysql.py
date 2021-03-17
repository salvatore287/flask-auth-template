import pymysql as mysql
#from os import environ
#import mysql.connector as mysql    # (add to requirements.txt)

class DBTypeError(TypeError):
    # raised when there's a database type error (currently supports 'str', 'float', 'int', 'None' and 'bool', datetime.datetime() and time.time() soon to come)
    pass

class Database:
    db = None
    dbc = None
    autocommit = True
    autoreconnect = True
    def __init__(self, host, user, pwd, data, port=3306, autocommit=True, autoreconnect=True):
        try:
            self.db = mysql.connect(host=host, user=user, password=pwd, database=data, port=port)
            self.dbc = self.db.cursor()
            self.autocommit = autocommit
            self.db.ping(reconnect=autoreconnect)
        except:
            return None
    """
    def execute(self, query):
        self.dbc.execute(query)
        try:
            res = self.dbc.fetchall()
            if self.autocommit:
                self.db.commit()
            return res
        except Exception as e:
            return None
    """
    def close(self):
        if self.db is not None:
            self.db.close()
    def insertUser(self, table, fields):
        if not isinstance(table, str):
            raise DBTypeError("'table' param must be type of 'str'.")
        if not isinstance(fields, dict):
            raise DBTypeError("'fields' param must be type of 'dict', ie. Dict['field'] = value")
        length = len(fields)
        if length == 0:
            raise DBTypeError("'fields' parameter must not be empty.")
        table = _escape(table)
        query = f"INSERT INTO {table} ("
        i = 0
        querypt1 = ''
        querypt2 = ''
        for key in fields:
            i += 1
            key = _escape(key)
            if not isinstance(key, str):
                raise DBTypeError("A 'fields' key must be type of 'str' only.")
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
                raise DBTypeError("A 'fields' value must be type of 'int', 'float', 'bool', 'str' or 'None' only.")
            if i != length:
                querypt1 += ","
                querypt2 += ","
        try:
            query += querypt1 + ") VALUES (" + querypt2 + f")"
            self.dbc.execute(query)
            return True
        except:
            return False
    def updateUser(self, table, fields, user):
        if not isinstance(table, str):
            raise DBTypeError("'table' param must be type of 'str'.")
        if not isinstance(fields, dict):
            raise DBTypeError("'fields' param must be type of 'dict', ie. Dict['field'] = value")
        if not isinstance(user, str):
            raise DBTypeError("'user' param must be type of 'str'.")
        length = len(fields)
        user = _escape(user)
        table = _escape(table)
        if length == 0:
            raise DBTypeError("'fields' parameter must not be empty.")
        query = f"UPDATE {table} SET "
        i = 0
        for key in fields:
            i += 1
            key = _escape(key)
            if not isinstance(key, str):
                raise DBTypeError("A 'fields' key must be type of 'str' only.")
            if isinstance(fields[key], str):
                fields[key] = _escape(fields[key])
                query += f"{key} = '{fields[key]}'"
            elif isinstance(fields[key], int) or isinstance(fields[key], float) or isinstance(fields[key], bool):
                query += f"{key} = {fields[key]}"
            elif fields[key] is None:
                query =+ f"{key} = NULL"
            else:
                raise DBTypeError("A 'fields' value must be type of 'int', 'float', 'bool', 'str' or 'None' only.")
            if i != length:
                query += ","
        user = _escape(user)
        query += f" WHERE name = '{user}'"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            return self.dbc.rowcount
        except:
            return -1
    def deleteUser(self, table, user):
        if not isinstance(table, str):
            raise DBTypeError("'table' param must be type of 'str'.")
        if not isinstance(user, str):
            raise DBTypeError("'user' param must be type of 'str'.")
        user = _escape(user)
        table = _escape(table)
        query = f"DELETE FROM {table} WHERE name = '{user}'"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            return self.dbc.rowcount
        except:
            return -1
    def getUserData(self, table, user):
        if not isinstance(table, str):
            raise DBTypeError("'table' param must be type of 'str'.")
        if not isinstance(user, str):
            raise DBTypeError("'user' param must be type of 'str'.")
        user = _escape(user)
        table = _escape(table)
        query = f"SELECT * FROM {table} WHERE name = '{user}'"
        try:
            self.dbc.execute(query)
            if self.autocommit:
                self.db.commit()
            x = list(self.dbc.fetchall())
            for i in range(len(x)):
                x[i] = list(x[i])
            return x
        except:
            return None

def _escape(text):
    return text.replace("'", "''")

if __name__ == "__main__":
    # *kasnije, ide citanje iz ENV varijable ovog dela ---> odg: svakako je privremeno, za testiranje
    """
    envget = environ.get
    HOST = envget("HOST")
    PORT = envget("PORT")
    USER = envget("USER")
    PASS = envget("PASS")
    DATA = envget("DATA")
    """
    USER = ""
    HOST = ""
    PASS = ""
    DATA = ""
    db = Database(HOST, USER, PASS, DATA, autocommit=True, autoreconnect=True)
    #x = db.execute("SELECT number,number2 FROM users WHERE name = 'test'")
    x = db.getUserData("users", "test8")
    print(f"Select: {x}")
    x = db.insertUser("users", {"name":"test8","pwd":"x","salt":"y","token":"z","number":310,"number2":3.13421})
    print(f"Insert: {x}") # successful insert?
    x = db.getUserData("users", "test8")
    print(f"Select: {x}")
    x = db.updateUser("users", {"number": 72, "number2": 127.4}, "test8")
    print(f"Update: {x}") # affected rows by using UPDATE
    x = db.getUserData("users", "test8")
    print(f"Select: {x}")
    x = db.deleteUser("users", "test8")
    print(f"Delete: {x}") # affected rows by using DELETE
    x = db.getUserData("users", "test8")
    print(f"Select: {x}")
    db.close()
