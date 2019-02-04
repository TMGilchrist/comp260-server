# Main game class. Contains gameloop

from Scripts import player
from Scripts import inputManager
# from Scripts import dungeon
# from Scripts import server
import socket


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, networkSocket):
        self.gameIsRunning = True
        self.currentInput = ''
        # self.player = ''
        # self.dungeon = ''

        self.networkSocket = networkSocket
        self.inputManager = inputManager.InputManager()

    def setup(self, dungeonName):
        """self.gameIsRunning = True
        self.currentInput = ''

        # Create a player and dungeon
        self.player = player.Player("NewCharacter", 10, self.client)
        self.dungeon = dungeon.Dungeon(dungeonName, self.player)

        # Setup rooms for the dungeon
        self.dungeon.SetupDefaultRooms()

        # Do player setup including storing current dungeon
        self.player.Setup(self.dungeon)"""

    # Main game code
    def GameLoop(self):

        # Receive data
        try:
            data = self.networkSocket.recv(4096)
            print(data.decode("utf-8"))

            data = self.networkSocket.recv(4096)
            print(data.decode("utf-8"))

        except socket.error:
            print("Server lost.")

        # Main server loop
        while self.gameIsRunning:
            self.currentInput = self.inputManager.GetInput("\nYou stand at the ready.")

            # Send input
            self.networkSocket.send(self.currentInput.encode())

            # Receive data
            try:
                data = self.networkSocket.recv(4096)
                print(data.decode("utf-8"))

            except socket.error:
                print("Server lost.")











