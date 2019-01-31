class InputManager:

    def __init__(self, player, dungeon):
        # Store the player that has instantiated an inputManager
        self.player = player

        # The current dungeon
        self.dungeon = dungeon

        # Help text, should include commands and useful info.
        self.helpText = "\n------------------------------------------------------------------\n" \
                        "General Commands \n" \
                        "~~~~~~~~~~~~~~~~ \n" \
                        "Help: Displays this help message. \n" \
                        "Go <direction>: Move to the room in this direction. \n" \
                        "<direction>: Directions are North, East, South and West. \n" \
                        "Look: Look at the room around you. \n" \
                        "Take <object>: Attempt to take an object or item and add it to your inventory. \n" \
                        "\nInventory Menu \n" \
                        "~~~~~~~~~~~~~~~~ \n" \
                        "Inventory: Displays your inventory \n" \
                        "Examine <object>: Attempt to examine an object in your inventory in more detail. \n" \
                        "------------------------------------------------------------------\n"

        # If the player is in the inventory menu
        self.inventoryActive = False

        self.userInput = ''
        self.splitInput = ''
        self.command = ''

    def GetInput(self, inputTitle=''):
        print(inputTitle)
        newInput = input("Enter a command: ")

        return newInput.lower()

    def HandleInput(self):
        userInput = self.GetInput("\nYou stand at the ready.")

        # Split string into individual words
        splitInput = userInput.split(' ')
        command = splitInput[0]

        if command == "exit":
            return "exit"

        elif command == "help":
            print(self.helpText)

        # Check for GO command.
        elif command == "go":
            self.Move(userInput)

        elif command == "look":
            self.Look()

        elif command == "take":
            self.TakeItem(splitInput)

        elif command == "inventory":
            self.player.CheckInventory()
            self.InventoryMenu()

        else:
            print("No such command - Use 'help' to display a list of commands.")

    def InventoryMenu(self):
        self.inventoryActive = True

        # Keep menu open while the user is in the inventory
        while self.inventoryActive:

            # print("\nYou are in your inventory.")

            userInput = self.GetInput("\nYou are in your inventory.")

            # Split string into individual words
            splitInput = userInput.split(' ')
            command = splitInput[0]

            if command == "back":
                self.inventoryActive = False
                print("\nYou  have left your inventory.")

            elif command == "examine":
                # Compare the dictionary keys of items in the room with the input the player has entered, storing matches in a new set.
                matchSet = set(splitInput).intersection(self.player.inventory.keys())

                # Convert set of matching keys to a list
                matches = list(matchSet)

                if bool(matches):
                    print(self.player.inventory[matches[0]].description)

                else:
                    print("Unable to find item.")

            elif command == "help":
                print(self.helpText)

            else:
                print("No such command. You are currently in the Inventory Menu - Use 'help' to display a list of commands.")

    def TakeItem(self, userInput):
        # Compare the dictionary keys of items in the room with the input the player has entered, storing matches in a new set.
        matchSet = set(userInput).intersection(self.dungeon.rooms[self.player.currentRoom].items.keys())

        # Convert set of matching keys to a list
        matches = list(matchSet)

        # If at least one match found (set is not empty)
        if bool(matches):
            print(self.dungeon.rooms[self.player.currentRoom].items[matches[0]].pickupText)

            # Add first item that matches to the inventory
            # self.player.inventory.append(self.dungeon.rooms[self.player.currentRoom].items[matches[0]])
            self.player.inventory[self.dungeon.rooms[self.player.currentRoom].items[matches[0]].name] = self.dungeon.rooms[self.player.currentRoom].items[matches[0]]

            # Remove item from the room
            del(self.dungeon.rooms[self.player.currentRoom].items[matches[0]])

        else:
            print("Unable to take item.")

    def Look(self):
        print("\n" + self.dungeon.rooms[self.player.currentRoom].description)

        for item in self.dungeon.rooms[self.player.currentRoom].items:
            print(self.dungeon.rooms[self.player.currentRoom].itemPlacement[item])

    def Move(self, userInput):
        if "north" in userInput:
            self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "north")

        elif "east" in userInput:
            self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "east")

        elif "south" in userInput:
            self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "south")

        elif "west" in userInput:
            self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "west")

