from Scripts import game
import socket
import time


# Entry point of program
def main():
    print("Entry point of SUD game.\n\n")

    #networkSocket = ClientSetup()

    newGame = game.Game()
    # newGame.setup()
    newGame.GameLoop()


def ClientSetup():
    # Setup network socket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False

    while connected != True:
        try:
            mySocket.connect(("127.0.0.1", 8222))
            print("Connected to server.")
            connected = True
        except socket.error:
            print("Could not connect to server")

    # Send some test data to the server
    testString = "Client connected."
    mySocket.send(testString.encode())

    return mySocket


if __name__ == "__main__":
    main()

