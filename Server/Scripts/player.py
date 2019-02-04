from Scripts import inputManager
from Scripts import character
from colorama import Fore, Back, Style, init


class Player(character.Character):

    def __init__(self, name, health, client):
        super().__init__(name, health)

        self.dungeon = ''
        self.currentRoom = ''
        self.inputManager = ''

        self.inventory = {}
        self.client = client

        # Init colorama
        init()

    def Setup(self, currentDungeon):
        self.dungeon = currentDungeon

        # The room the player is currently in. Set to the start room when the player starts the game.
        self.currentRoom = self.dungeon.startRoom

        # InputManager to handle typing
        self.inputManager = inputManager.InputManager(self, self.dungeon)

    def CheckInventory(self):

        output = ("\n------------------------ \n"
                  + Fore.BLUE + "Inventory: " + Fore.RESET + str(len(self.inventory)) + " items \n")

        for item in self.inventory:
            output += (" - " + item)

        output += ("\n------------------------" + Back.RESET)

        return output
