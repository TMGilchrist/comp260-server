# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon
from Scripts import server
import socket


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, client):
        self.gameIsRunning = ''
        self.currentInput = ''
        self.player = ''
        self.dungeon = ''

        self.client = client

    def setup(self, dungeonName):
        self.gameIsRunning = True
        self.currentInput = ''

        # Create a player and dungeon
        self.player = player.Player("NewCharacter", 10, self.client)
        self.dungeon = dungeon.Dungeon(dungeonName, self.player)

        # Setup rooms for the dungeon
        self.dungeon.SetupDefaultRooms()

        # Do player setup including storing current dungeon
        self.player.Setup(self.dungeon)

    # Main game code
    def GameLoop(self):
        # Pre-game intro text
        print(self.dungeon.description)
        # print("\n" + self.dungeon.rooms[self.player.currentRoom].description + "\n")

        self.player.inputManager.Look()

        # Main server loop
        while self.gameIsRunning:

            # Get client user input
            try:
                data = self.client[0].recv(4096)
                print(data.decode("utf-8"))

            except socket.error:
                print("Unable to access client")

            # Process the user input
            # if self.player.inputManager.HandleInput(data.decode("utf-8")) == "exit":
                # self.gameIsRunning = False

            serverOutput = self.player.inputManager.HandleInput(data.decode("utf-8"))

            if serverOutput == "exit":
                self.gameIsRunning = False

            else:
                server.Output(self.client, serverOutput)









