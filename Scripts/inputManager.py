class InputManager:

    def __init__(self, player, dungeon):
        # Store the player that has instantiated an inputManager
        self.player = player

        # The current dungeon
        self.dungeon = dungeon

        # Help text, should include commands and useful info.
        self.helpText = "\n------------------------------------------------------------------\n" \
                        "Help: Displays this help message. \n" \
                        "Go <direction>: Move to the room in this direction. \n" \
                        "<direction>: Directions are North, East, South and West. \n" \
                        "Look: Look at the room around you. \n" \
                        "Examine <object> (WIP): Attempt to examine and object, item or feature in more detail. \n" \
                        "Take <object>: Attempt to take an object or item and add it to your inventory. \n" \
                        "Inventory: Displays your inventory \n" \
                        "------------------------------------------------------------------\n"

    def GetInput(self):
        newInput = input("Enter a command: ")

        return newInput.lower()

    def HandleInput(self):
        userInput = self.GetInput()

        # Split string into individual words
        splitInput = userInput.split(' ')
        command = splitInput[0]

        if command == "exit":
            return "exit"

        elif command == "help":
            print(self.helpText)

        # Check for GO command.
        elif command == "go":
            if "north" in userInput:
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "north")

            elif "east" in userInput:
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "east")

            elif "south" in userInput:
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "south")

            elif "west" in userInput:
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "west")

        elif command == "look":
            print("\n" + self.dungeon.rooms[self.player.currentRoom].description)

        elif command == "take":
            # Compare the dictionary keys of items in the room with the input the player has entered, storing matches in a new set.
            matchSet = set(splitInput).intersection(self.dungeon.rooms[self.player.currentRoom].items.keys())

            # Convert set of matching keys to a list
            matches = list(matchSet)

            # If at least one match found (set is not empty)
            if bool(matches):
                # Add first item that matches to the inventory
                self.player.inventory.append(self.dungeon.rooms[self.player.currentRoom].items[matches[0]])
            else:
                print("Unable to take item.")

        elif command == "inventory":
            self.player.checkInventory()

        else:
            print("No such command - Use 'help' to display a list of commands.")




