from Scripts import game
import socket
import time


# Entry point of program
def main():
    print("Entry point of SUD game.\n\n")

    client = ServerSetup()

    newGame = game.Game(client)
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

    # ?
    seqID = 0

    # Send and receive data to/from client
    """
    while True:
        # Send a test string
        try:
            testString = str(seqID) + ":" + time.ctime()
            client[0].send(testString.encode())
        except socket.error:
            print("Client lost")

        seqID += 1
        time.sleep(0.5)
    """

    return client


if __name__ == "__main__":
    main()

