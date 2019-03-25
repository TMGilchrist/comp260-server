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

    def CreateTables(self):
        dungeonSQL = """
                     CREATE TABLE dungeonRooms(
                     id int PRIMARY KEY,
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

    def CreateRoom(self, name, entryDescription, description, connections):
        insertSQL = "INSERT INTO dungeonRooms(name, entryDescription, description, connections) VALUES(?, ?, ?, ?)"

        self.cursor.execute(insertSQL, (name, entryDescription, description, connections))
        self.connection.commit()

    def QueryTableByID(self, tableName, fieldToFind, ID):

        self.cursor.execute("SELECT " + fieldToFind + " FROM " + tableName + " WHERE ID = " + ID)

        result = self.cursor.fetchone()[0]
        print("Result of query is " + result)



