class InputManager:

    def __init__(self):
        print("Init inputManager")

    def GetInput(self):
        newInput = input("Enter a command: ")

        return newInput.lower()