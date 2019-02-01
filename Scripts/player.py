from Scripts import inputManager
from Scripts import character


class Player(character.Character):

    def __init__(self, name, health):
        super().__init__(name, health)

        self.dungeon = ''
        self.currentRoom = ''
        self.inputManager = ''

        self.inventory = {}

    def Setup(self, currentDungeon):
        self.dungeon = currentDungeon

        # The room the player is currently in. Set to the start room when the player starts the game.
        self.currentRoom = self.dungeon.startRoom

        # InputManager to handle typing
        self.inputManager = inputManager.InputManager(self, self.dungeon)

    def CheckInventory(self):

        print("\n------------------------ \n"
              "Inventory: " + str(len(self.inventory)) + " items \n")

        for item in self.inventory:
            print(" - " + item)

        print("------------------------")
