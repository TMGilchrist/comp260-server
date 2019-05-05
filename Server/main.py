from Scripts import game


# Entry point of program
def main():

    print("Entry point of SUD game.\n\n")

    newGame = game.Game()
    newGame.setup("New Dungeon")
    newGame.GameLoop()


if __name__ == "__main__":
    main()

