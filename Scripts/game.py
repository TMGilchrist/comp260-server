# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon


"""
Game class that holds important information for a game including the dungeon and the player. 
"""
class Game:

    def __init__(self):
        self.gameIsRunning = ''
        self.currentInput = ''
        self.player = ''
        self.dungeon = ''

    def setup(self, dungeonName):
        self.gameIsRunning = True
        self.currentInput = ''

        # Create a player and dungeon
        self.player = player.Player("NewCharacter", 10)
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

        # Main game loop
        while self.gameIsRunning:

            # Handles player input. Also exits if the player inputs "exit". Might be a slightly bad way of doing this?
            if self.player.inputManager.HandleInput() == "exit":
                self.gameIsRunning = False








