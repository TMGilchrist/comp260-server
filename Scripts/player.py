from Scripts import inputManager


class Player:

    def __init__(self):
        self.name = ''
        self.dungeon = ''
        self.currentRoom = ''
        self.inputManager = ''

    def setup(self, name, currentDungeon):
        # Player's name. With multiple players this should be unique.
        self.name = name

        # The dungeon the player is currently in
        self.dungeon = currentDungeon

        # The room the player is currently in
        self.currentRoom = "Start"

        # InputManager to handle typing
        self.inputManager = inputManager.InputManager(self, self.dungeon)



