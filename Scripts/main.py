from Scripts import game


# Entry point of program
def main():
    print("Entry point of SUD game.")

    newGame = game.Game("NewDungeon")
    newGame.GameLoop()


if __name__ == "__main__":
    main()

