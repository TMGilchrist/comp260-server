from Scripts import game
from Scripts import database


# Entry point of program
def main():
    print("Entry point of SUD game.\n\n")

    """sqlManger = database.sqlManager()
    sqlManger.ConnectToDB("../MUDdatabase.db")
    sqlManger.QueryTableByID("dungeonRooms", "name", "1")"""

    newGame = game.Game()
    newGame.setup("New Dungeon")
    newGame.GameLoop()


if __name__ == "__main__":
    main()

