from Scripts import inputManager
import socket
import time


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, networkSocket):
        self.gameIsRunning = True
        self.currentInput = ''

        self.networkSocket = networkSocket
        self.inputManager = inputManager.InputManager()

    # Main game code
    def GameLoop(self):

        # Get intro output
        self.GetServerOutput()

        # Main server loop
        while self.gameIsRunning:
            self.currentInput = self.inputManager.GetInput("\nYou stand at the ready.")

            # Receive server output
            try:
                # Send input
                self.networkSocket.send(self.currentInput.encode())

                data = self.networkSocket.recv(4096)
                print(data.decode("utf-8"))

            except socket.error:
                print("Server lost.")
                self.Reconnect()


    def Reconnect(self):
        connected = False
        self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while not connected:
            try:
                print("Attempting to reconnect.")
                self.networkSocket.connect(("127.0.0.1", 8222))
                # self.GetServerOutput()
                connected = True

            except socket.error:
                print("Unable to connect.")
                time.sleep(1)

    def GetServerOutput(self):

        # Receive startup server output
        try:
            data = self.networkSocket.recv(4096)
            print(data.decode("utf-8"))

        except socket.error:
            print("Server lost.")









