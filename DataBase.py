import sqlite3


class DataBase:
    def __init__(self, db):
        self.db = db
        try:
            self.connection = sqlite3.connect(self.db)
            print('connection with {} successful'.format(self.db))
            self.cursor = self.connection.cursor()
        except sqlite3.Error:
            print(sqlite3.Error)
        finally:
            self.connection.close()
            print('connection closed')

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db)
            self.cursor = self.connection.cursor()
            print('connection with {} successful'.format(self.db))
        except sqlite3.Error:
            print(sqlite3.Error)

    def close(self):
        self.connection.close()

    def executeQuery(self, query, val):
        self.cursor = self.connection.cursor()
        self.cursor.execute(query, val)
        self.connection.commit()

    def addScoreTable(self, name):
        sql = '''CREATE TABLE IF NOT EXISTS {} (id integer PRIMARY KEY, playerName text NOT NULL, score integer);'''.format(name)
        self.cursor.execute(sql)
        self.connection.commit()
        print('table {} added'.format(name))

    def addRow(self, name, row):
        sql = '''INSERT INTO {} (playerName, score) VALUES (?,?);'''.format(name)
        self.cursor.execute(sql, row)
        self.connection.commit()
        print('row added')

    def getTable(self, name):
        sql = '''SELECT * FROM {}'''.format(name)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def updateRow(self, tableName, playerName, newRow):
        sql = '''UPDATE {} SET playerName = ?, score = ? WHERE playerName = ?;'''.format(tableName)
        row = newRow + (playerName,)
        self.cursor.execute(sql, row)
        self.connection.commit()
        print('row updated')

    def getTop10(self, tableName):
        sql = '''SELECT * FROM {} ORDER BY score DESC LIMIT 10;'''.format(tableName)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def getRowsWhereNameIs(self, tableName, playerName):
        sql = '''SELECT * FROM {} WHERE playerName = ?'''.format(tableName)
        self.cursor.execute(sql, (playerName,))
        return self.cursor.fetchall()

