from colorama import Fore, Back, Style, init


class InputManager:

    def __init__(self):
        # Help text, should include commands and useful info.
        self.helpText = "\n------------------------------------------------------------------\n" \
                        + Fore.BLUE + "General Commands \n" \
                        "~~~~~~~~~~~~~~~~ \n" \
                        + Fore.GREEN + "Help: " + Fore.RESET + "Displays this help message. \n" \
                        + Fore.GREEN + "Go <direction>: " + Fore.RESET + "Move to the room in this direction. \n" \
                        + Fore.GREEN + "<direction>: " + Fore.RESET + "Directions are North, East, South and West. \n" \
                        + Fore.GREEN + "Look: " + Fore.RESET + "Look at the room around you. \n" \
                        + Fore.GREEN + "Take <object>: " + Fore.RESET + "Attempt to take an object or item and add it to your inventory. \n" \
                        + Fore.BLUE + "\nInventory Menu \n" \
                        "~~~~~~~~~~~~~~~~ \n" \
                        + Fore.GREEN + "Inventory: " + Fore.RESET + "Displays your inventory \n" \
                        + Fore.GREEN + "Examine <object>: " + Fore.RESET + "Attempt to examine an object in your inventory in more detail. \n" \
                        "------------------------------------------------------------------\n"

        # If the player is in the inventory menu
        self.inventoryActive = False


        # Initialise colorama
        init()

    def GetInput(self, inputTitle=''):
        print(inputTitle)
        newInput = input(Fore.MAGENTA + "Enter a command: " + Fore.RESET)

        return newInput.lower()

