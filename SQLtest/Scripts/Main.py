import sqlite3


dataBasePath = "testDB.sqlite3"
connection = sqlite3.connect(dataBasePath)
cursor = connection.cursor()



def main():
    print("Starting SQLite test")

    running = True

    studentsSQL = """
                  CREATE TABLE students(
                  id int PRIMARY KEY,
                  first_name text NOT NULL,
                  last_name text NOT NULL,
                  fav_colour text NOT NULL)
                  """

    # cursor.execute(studentsSQL)
    # connection.commit()


    print(cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"))
    print(cursor.fetchall())

    # print(cursor.fetchone()[0])

    #CreateStudent(("Ryan", "Clarke", "Purple"))

    while running:
        userInput = input(">>")

        if userInput == "exit":
            running = False

        else:
            print(cursor.execute(userInput))

# Insert into table
def CreateStudent(data):

    insertSQL = "INSERT INTO students(first_name, last_name, fav_colour) VALUES(?, ?, ?)"

    cursor.execute(insertSQL, data)
    connection.commit()


# Connect to a database or create a new one at the file path. Returns the connection.
def connectToDB(dataBasePath):
    connection = sqlite3.connect(dataBasePath)

    return connection


if __name__ == "__main__":
    main()


