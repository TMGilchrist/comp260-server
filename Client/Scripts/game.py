from Scripts import inputManager
import socket
import time


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, networkSocket=''):
        self.gameIsRunning = True
        self.isConnected = False

        self.currentInput = ''

        self.networkSocket = networkSocket
        self.inputManager = inputManager.InputManager()

        self.Connect()

    def Connect(self):
        # While client not connected to a server
        while self.isConnected == False:

            self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server
            try:
                self.networkSocket.connect(("127.0.0.1", 8222))
                self.isConnected = True
                print("Server connect successful.")

            except socket.error:
                self.isConnected = False
                print("Could not connect to server.")

            if(self.isConnected == True):
                try:
                    confirmationData = "Client: Client connected to the server"
                    self.networkSocket.send(confirmationData.encode())

                except socket.error:
                    self.isConnected = False
                    self.networkSocket = None

            if self.isConnected == False:
                print("No server")
                time.sleep(1.0)

    # Main game code
    def GameLoop(self):
        print("Client gameloop entered.")

        # Get intro output
        #self.GetServerOutput()

        # Main server loop
        while self.gameIsRunning:

            # While client not connected to a server
            while self.isConnected == False:
                # Check if socket is null
                if self.networkSocket is None:
                    self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to server
                try:
                    self.networkSocket.connect(("127.0.0.1", 8222))
                    self.isConnected = True
                    print("Server connect successful.")

                except socket.error:
                    self.isConnected = False
                    print("Could not connect to server.")

                if(self.isConnected == True):
                    try:
                        confirmationData = "Client: Client connected to the server"
                        self.networkSocket.send(confirmationData.encode())

                    except socket.error:
                        self.isConnected = False
                        self.networkSocket = None

                if self.isConnected == False:
                    print("No server")
                    time.sleep(1.0)

            while self.isConnected == True:

                # Get user input
                self.currentInput = self.inputManager.GetInput("\nYou stand at the ready.")

                # Receive server output
                try:
                    # Send input
                    self.networkSocket.send(self.currentInput.encode())

                    # Receive response
                    data = self.networkSocket.recv(4096)
                    print(data.decode("utf-8"))

                except socket.error:
                    print("Server lost.")
                    #self.Reconnect()
                    self.isConnected = False
                    self.networkSocket = None

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









