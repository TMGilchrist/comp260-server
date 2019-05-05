import sqlite3


class sqlManager:

    def __init__(self):
        self.connection = ""
        self.cursor = ""

    # Connect to a database or create a new one at the file path. Returns the connection.
    def ConnectToDB(self, dataBasePath):
        connection = sqlite3.connect(dataBasePath)
        self.connection = connection
        self.cursor = connection.cursor()

        return connection

    """------------------
          Creation
    ------------------"""

    def CreateTables(self):
        roomsSQL = ""
        cursor = self.connection.cursor()
        cursor.execute(roomsSQL)

        playersSQL = "CREATE TABLE players(Name text not null UNIQUE PRIMARY KEY, CurrentRoom text, User text, foreign key(CurrentRoom) references rooms(Name), foreign key(User) references users(Username))"
        cursor = self.connection.cursor()
        cursor.execute(playersSQL)

        usersSQL = "CREATE TABLE users(Username text unique not null, Password text not null, LoggedIn bool default false, LastLoggedIn text, TimeLoggedIn Text)"
        cursor = self.connection.cursor()
        cursor.execute(usersSQL)

        self.connection.commit()

    """------------------
          Inserts
    ------------------"""

    def CreateRoom(self, name, entryDescription, description, north='', east='', south='', west=''):
        insertSQL = "INSERT INTO rooms(RoomName, EntryDescription, Description, North, East, South, West) VALUES(?, ?, ?, ?, ?, ?, ?)"

        self.cursor.execute(insertSQL, (name, entryDescription, description, north, east, south, west))
        self.connection.commit()

    def CreateUser(self, username, password):
        insertSQL = "INSERT INTO users(Username, Password) VALUES(?, ?)"

        self.cursor.execute(insertSQL, (username, password))
        self.connection.commit()

    def CreatePlayer(self, name, currentRoom, user):
        insertSQL = "INSERT INTO players(Name, CurrentRoom, User) VALUES(?, ?, ?)"

        self.cursor.execute(insertSQL, (name, currentRoom, user))
        self.connection.commit()

    """------------------
          Updates
    ------------------"""

    def Update(self, tableToUpdate, fieldToUpdate, newValue, filterField, filterValue):

        sql = ("UPDATE " + tableToUpdate + " SET " + fieldToUpdate + " =?" + " WHERE " + filterField + "=?")

        self.cursor.execute(sql, (newValue, filterValue,))
        self.connection.commit()

    """------------------
          Queries
    ------------------"""

    def QueryWithFilter(self, tableToQuery, fieldToQuery, filterField, filterValue):

        self.cursor.execute("SELECT " + fieldToQuery + " FROM " + tableToQuery + " WHERE " + filterField + "=?", (filterValue,))

        rows = self.cursor.fetchall()

        for index, row in enumerate(rows):
            rows[index] = row[0]
            print(rows[index])

        return rows

    def Query(self, tableToQuery, fieldToQuery):

        self.cursor.execute("SELECT " + fieldToQuery + " FROM " + tableToQuery)

        rows = self.cursor.fetchall()

        for row in rows:
            row = row[0]
            #print(row)

        return rows




