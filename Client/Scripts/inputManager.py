from colorama import Fore, Back, Style, init


class InputManager:

    def __init__(self):
        # If the player is in the inventory menu
        self.inventoryActive = False

        # Initialise colorama
        init()

    def GetInput(self, inputTitle=''):
        print(inputTitle)
        newInput = input(Fore.MAGENTA + "Enter a command: " + Fore.RESET)

        return newInput.lower()

