from Scripts import inputManager


class Player:

    def __init__(self, name):
        self.name = name
        self.currentRoom = "Start"

        # InputManager to handle typing
        self.inputManager = inputManager.InputManager()



