# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon
from Scripts import server
import socket


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, client=''):
        self.gameIsRunning = ''
        self.isConnected = ''

        self.currentInput = ''
        self.player = ''
        self.dungeon = ''

        self.networkSocket = ''
        self.client = client

    def setup(self, dungeonName):
        self.gameIsRunning = True
        self.currentInput = ''

        self.Connect()

        # Create a player and dungeon
        self.player = player.Player("NewCharacter", 10, self.client)
        self.dungeon = dungeon.Dungeon(dungeonName, self.player)

        # Setup rooms for the dungeon
        self.dungeon.SetupDefaultRooms()

        # Do player setup including storing current dungeon
        self.player.Setup(self.dungeon)

    def Connect(self):
        self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.networkSocket.bind(("127.0.0.1", 8222))
        self.networkSocket.listen(5)
        self.client = self.networkSocket.accept()

        # Receive some test data from the client
        data = self.client[0].recv(4096)
        print(data.decode("utf-8"))

    # Main game code
    def GameLoop(self):
        print("Server in gameloop")

        # Pre-game intro text
        intro = self.dungeon.description + self.player.inputManager.Look()
        server.Output(self.client, intro)

        # Main server loop
        while self.gameIsRunning:

            # Check for client and try to connect if not found
            if self.isConnected == False:
                print("Waiting for client")
                self.client = self.networkSocket.accept()

            # Attempt to get input from client
            try:
                self.isConnected = True
                print("Client found")

                data = self.client[0].recv(4096)
                print(data.decode("utf-8"))

            except socket.error:
                print("Unable to access client")
                self.isConnected = False

            # While connected, process client data and output if possible
            while self.isConnected == True:
                try:
                    data = self.client[0].recv(4096)
                    print(data.decode("utf-8"))

                    serverOutput = self.player.inputManager.HandleInput(data.decode("utf-8"))

                    if serverOutput == "exit":
                        self.gameIsRunning = False

                    else:
                        # Send server output. server.Output returns false if not connected.
                        self.isConnected = server.Output(self.client, serverOutput)

                except socket.error:
                    print("Unable to access client")
                    self.isConnected = False











