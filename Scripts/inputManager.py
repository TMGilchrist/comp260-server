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
                        "<directon>: Directions are North, East, South and West. \n" \
                        "------------------------------------------------------------------\n"

    def GetInput(self):
        newInput = input("Enter a command: ")

        return newInput.lower()

    def HandleInput(self):
        userInput = self.GetInput()

        # Split string into individual words
        splitInput = userInput.split(' ')
        command = splitInput[0]

        if command == "help":
            print(self.helpText)

        # How to pass this back to game?
        if command == "exit":
            return "exit"

        # Check for GO command.
        if command == "go":
            if "north" in userInput:
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "north")

            elif "east" in userInput:
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "east")

            elif "south" in userInput:
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "south")

            elif "west" in userInput:
                self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "west")

        if command == "look":
            print("\n" + self.dungeon.rooms[self.player.currentRoom].description)




