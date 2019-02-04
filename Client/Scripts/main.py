from Scripts import game
import socket
import time


# Entry point of program
def main():
    print("Entry point of SUD game.\n\n")

    networkSocket = ClientSetup()

    newGame = game.Game(networkSocket)
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
    testString = "this is a test from the python client"
    mySocket.send(testString.encode())

    """
    # Send/Receive data to/from server
    while True:
        # Receive data
        try:
            data = mySocket.recv(4096)
            print(data.decode("utf-8"))
        except socket.error:
            print("Server lost.")
            time.sleep(1.0)
    """

    return mySocket


if __name__ == "__main__":
    main()

