# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon


"""
Game class that holds important information for a game including the dungeon and the player. 
"""
class Game:

    def __init__(self, dungeonName):
        self.player = player.Player('NewCharacter')
        self.gameIsRunning = True
        self.currentInput = ''
        self.dungeon = dungeon.Dungeon(dungeonName, self.player)
        self.dungeon.SetupDefaultRooms()

    # Main game loop
    def GameLoop(self):
        while self.gameIsRunning:
            currentInput = self.player.inputManager.GetInput()

            # Quit game
            if currentInput == "exit":
                self.gameIsRunning = False

            # Check for southern movement
            if currentInput == "south":
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "south")





