from Scripts import inputManager
from Scripts import character
from colorama import Fore, Back, Style, init


class Player(character.Character):

    def __init__(self, name, health, currentDungeon='', client=''):
        super().__init__(name, health)

        self.dungeon = currentDungeon
        self.currentRoom = ''

        self.inventory = {}
        self.client = client

        # Init colorama
        init()

        self.Setup(self.dungeon)

    def Setup(self, currentDungeon):
        self.dungeon = currentDungeon

        # The room the player is currently in. Set to the start room when the player starts the game.
        self.currentRoom = self.dungeon.startRoom

    def CheckInventory(self):

        output = ("<br>------------------------<br> "
                  "<font color=Brown>Inventory: </font>" + str(len(self.inventory)) + " items <br>")

        for item in self.inventory:
            output += (" - " + item + "<br>")

        output += "<br>------------------------<br>"

        return output
