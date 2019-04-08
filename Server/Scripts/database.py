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
        dungeonSQL = """
                     CREATE TABLE dungeonRooms(
                     id integer PRIMARY KEY,
                     RoomName text NOT NULL,
                     EntryDescription text DEFAULT "You enter an empty room.",
                     Description text DEFAULT "An empty room.",
                     North text DEFAULT "",
                     East text DEFAULT "",
                     South text DEFAULT "",
                     West text DEFAULT "")
                     """

        cursor = self.connection.cursor()
        cursor.execute(dungeonSQL)
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
        insertSQL = "INSERT INTO users(Name, CurrentRoom, User) VALUES(?, ?, ?)"

        self.cursor.execute(insertSQL, (name, currentRoom, user))
        self.connection.commit()

    """------------------
          Queries
    ------------------"""

    def QueryWithFilter(self, tableToQuery, fieldToQuery, filterField, filterValue):

        self.cursor.execute("SELECT " + fieldToQuery + " FROM " + tableToQuery + " WHERE " + filterField + "=?", (filterValue,))

        rows = self.cursor.fetchall()

        for index, row in enumerate(rows):
            rows[index] = row[0]
            #print(rows[index])

        return rows

    def Query(self, tableToQuery, fieldToQuery):

        self.cursor.execute("SELECT " + fieldToQuery + " FROM " + tableToQuery)

        rows = self.cursor.fetchall()

        for row in rows:
            row = row[0]
            #print(row)

        return rows




