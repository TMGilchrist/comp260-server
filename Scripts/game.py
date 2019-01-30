# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon


"""
Game class that holds important information for a game including the dungeon and the player. 
"""
class Game:

    def __init__(self, dungeonName):
        self.gameIsRunning = True
        self.currentInput = ''

        # Create a player and dungeon
        self.player = player.Player()
        self.dungeon = dungeon.Dungeon(dungeonName, self.player)

        # Setup rooms for the dungeon
        self.dungeon.SetupDefaultRooms()

        # Do player setup including storing current dungeon
        self.player.setup('NewCharacter', self.dungeon)

    # Main game loop
    def GameLoop(self):
        print(self.dungeon.description)
        print("\n" + self.dungeon.rooms[self.player.currentRoom].description + "\n")

        while self.gameIsRunning:
            # currentInput = self.player.inputManager.GetInput()
            self.player.inputManager.HandleInput()

            """
            # Quit game
            if currentInput == "exit":
                self.gameIsRunning = False"""







