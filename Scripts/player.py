from Scripts import inputManager


class Player:

    def __init__(self):
        self.name = ''
        self.dungeon = ''
        self.currentRoom = ''
        self.inputManager = ''
        self.inventory = []

    def setup(self, name, currentDungeon):
        # Player's name. With multiple players this should be unique.
        self.name = name

        # The dungeon the player is currently in
        self.dungeon = currentDungeon

        # The room the player is currently in. Set to the start room when the player starts the game.
        self.currentRoom = self.dungeon.startRoom

        # InputManager to handle typing
        self.inputManager = inputManager.InputManager(self, self.dungeon)

    def checkInventory(self):

        print("\n------------------------ \n"
              "Inventory: " + str(len(self.inventory)) + " items \n")

        for item in self.inventory:
            print(" - " + item.name)

        print("------------------------ \n")
