from Scripts import game
import socket


# Entry point of program
def main():
    print("Entry point of SUD game.\n\n")

    #client = ServerSetup()

    newGame = game.Game()
    newGame.setup("New Dungeon")
    newGame.GameLoop()


def ServerSetup():
    # Setup network socket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind(("127.0.0.1", 8222))

    # Listen for a client
    mySocket.listen(5)
    client = mySocket.accept()

    # Receive some test data from the client
    data = client[0].recv(4096)
    print(data.decode("utf-8"))

    return client


if __name__ == "__main__":
    main()

