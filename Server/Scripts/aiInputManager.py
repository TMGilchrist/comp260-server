from colorama import Fore, Back, Style, init
from Scripts import server


class AiInputManager:

    def __init__(self, dungeon):

        # The current dungeon
        self.dungeon = dungeon

        self.userInput = ''
        self.splitInput = ''
        self.command = ''

        # Possible movement directions in the dungeon.
        self.directions = ["north", "south", "east", "west"]

        # Initialise colorama
        init()

    def HandleInput(self, player, userInput):
        print(Fore.BLUE + "Handle Input: " + userInput + Fore.RESET)

        # Split string into individual words
        splitInput = userInput.split(' ')
        command = splitInput[0]

        # Check for GO command.
        if command == "go":
            return self.Move(player, splitInput)

        else:
            return "No such command - Use 'help' to display a list of commands."

    def Move(self, player, splitInput):
        # List comprehension to get matches between possible movement directions and input commands.
        moveDirection = [direction for direction in splitInput if direction in self.directions]

        if len(moveDirection) > 0:
            # Use the first direction command found and move the player.
            newRoom = self.dungeon.Move(player.currentRoom, moveDirection[0])

            # Check if the player has actually changed rooms.
            if player.currentRoom == newRoom:
                return "\nThere is nowhere to go in this direction."

            else:
                #self.messagePlayers(player, player.name + " leaves the room.", True)

                player.currentRoom = newRoom

                #self.messagePlayers(player, player.name + " enters the room.", True)

                return "\n" + moveDirection[0] + "\n" + self.dungeon.rooms[player.currentRoom].entryDescription

        return "Please enter a valid direction."