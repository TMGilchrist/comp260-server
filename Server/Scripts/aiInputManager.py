from colorama import Fore, Back, Style, init
from Scripts import server
import random
import time


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
        print(Fore.BLUE + "Handle AI Input: " + userInput + Fore.RESET)

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
                self.MessagePlayers(player, "<font color=red>" + player.name + " leaves the room, heading " + moveDirection[0] + ". </font>", True)

                player.currentRoom = newRoom

                self.MessagePlayers(player, "<font color=orange>" + player.name + " enters the room from the " + moveDirection[0] + ". </font>", True)

                return "\n" + moveDirection[0] + "\n" + self.dungeon.rooms[player.currentRoom].entryDescription

        return "Please enter a valid direction."

    # Check the current room for connections and add valid paths as options for the agent to take.
    def GetOptions(self, player):
        # Clear any current options.
        player.options.clear()

        print("Possible commands from this room.")

        for connection in self.dungeon.rooms[player.currentRoom].connections:
            if self.dungeon.rooms[player.currentRoom].connections[connection] != "":
                player.options.append(connection)

        player.options.append("wait")
        print(player.options)

    def MakeChoice(self, player):
        print("AI making choice.")

        # Get a random index for the options list
        randomIndex = random.randint(0, len(player.options) - 1)
        optionChoice = player.options[randomIndex]

        print("Choice: " + optionChoice)

        # Wait in room.
        if optionChoice == "wait":
            print("Waiting in room")
            print(Fore.CYAN + "AI current room: " + player.currentRoom + "\n" + Fore.RESET)

            timeToWait = 4
            return timeToWait

        # Move to new room.
        else:
            print("Moving " + optionChoice)
            self.Move(player, ["go", optionChoice])
            print(Fore.CYAN + "AI current room: " + player.currentRoom + "\n" + Fore.RESET)
            timeToWait = 1
            return timeToWait

    # Outputs a message to other players. If sameRoomOnly is set to true, the message is only sent to players
    # in the same room as the player sending the message.
    def MessagePlayers(self, player, message, sameRoomOnly=True):
        # For all other players in the game (excluding the speaker) display the message.
        for playerClient in self.dungeon.players:
            if self.dungeon.players[playerClient] != player:

                # If the message should only be hear by players in the same room
                if sameRoomOnly is True:
                    if self.dungeon.players[playerClient].currentRoom == player.currentRoom:
                        server.Output(playerClient, message)
                else:
                    server.Output(playerClient, message)
