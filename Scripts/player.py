from Scripts import inputManager


class Player:
    name = ''
    currentRoom = ''

    # InputManager to handle typing
    inputManager = inputManager.InputManager()

    def __init__(self, name):
        self.name = name


