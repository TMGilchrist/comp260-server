from Scripts import character
from colorama import init


class Player(character.Character):

    def __init__(self, name, health, currentDungeon):
        super().__init__(name, health)

        self.dungeon = currentDungeon
        self.currentRoom = ''

        self.inventory = {}

        # Init colorama
        init()

        self.Setup()

    def Setup(self):

        # The room the player is currently in. Set to the start room when the player starts the game.
        self.currentRoom = self.dungeon.startRoom

    def CheckInventory(self):

        output = ("<br>------------------------<br> "
                  "<font color=Brown>Inventory: </font>" + str(len(self.inventory)) + " items <br>")

        for item in self.inventory:
            output += (" - " + item + "<br>")

        output += "<br>------------------------<br>"

        return output
