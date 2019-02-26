from colorama import Fore, Back, Style, init
import socket
from Scripts import server
# from PyQt5 import QtGui

class InputManager:

    def __init__(self, dungeon):

        # The current dungeon
        self.dungeon = dungeon

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

        # Help text, should include commands and useful info.
        self.helpTextHTML = "<br>------------------------------------------------------------------<br>" \
                            "<font color='Blue'>General Commands</font><br>" \
                            "~~~~~~~~~~~~~~~~ <br>" \
                            "<font color='Green'>Help: </font> Displays this help message. <br>" \
                            "<font color='Green'>Go <direction>: </font> Move to the room in this direction. <br>" \
                            "<font color='Green'>Direction: </font> Directions are North, East, South and West. <br>" \
                            "<font color='Green'>Look: </font> Look at the room around you. <br>" \
                            "<font color='Green'>Take <object>: </font>Attempt to take an object or item and add it to your inventory. <br>" \
                            "<font color='Green'>Say: </font>Speak out loud. Other players in the same room will be able to hear you. <br>" \
                            "<font color='Blue'><br>Inventory Menu</font><br>" \
                            "~~~~~~~~~~~~~~~~ <br>" \
                            "<font color='Green'>Inventory: </font> Displays your inventory <br>" \
                            "<font color='Green'>Examine <object>: </font> Attempt to examine an object in your inventory in more detail. <br>" \
                            "------------------------------------------------------------------<br>"

        # If the player is in the inventory menu
        self.inventoryActive = False

        self.userInput = ''
        self.splitInput = ''
        self.command = ''

        # Possible movement directions in the dungeon.
        self.directions = ["north", "south", "east", "west"]

        # Initialise colorama
        init()

    def GetInput(self, player, inputTitle=''):
        print(inputTitle)
        newInput = input(Fore.MAGENTA + "Enter a command: " + Fore.RESET)

        return newInput.lower()

    def HandleInput(self, player, userInput):
        print(Fore.BLUE + "Handle Input: " + userInput + Fore.RESET)

        # Split string into individual words
        splitInput = userInput.split(' ')
        command = splitInput[0]

        if command[0] == '#':
            return self.parseServerCommand(player, command, splitInput)

        if command == "help":
            return self.helpTextHTML

        if self.inventoryActive is True:
            return self.InventoryMenu(player, command, splitInput)

        if command == "exit":
            return "exit"

        # Check for GO command.
        elif command == "go":
            return self.Move(player, splitInput)

        elif command == "look":
            return self.Look(player)

        elif command == "take":
            return self.TakeItem(player, splitInput)

        elif command == "drop":
            return self.DropItem(player, splitInput)

        elif command == "say":
            return self.Say(player, splitInput)

        elif command == "inventory":
            self.inventoryActive = True
            return player.CheckInventory()

        else:
            return "No such command - Use 'help' to display a list of commands."

    def InventoryMenu(self, player, command, splitInput):

            if command == "back":
                self.inventoryActive = False
                return "\nYou  have left your inventory."

            elif command == "examine":
                # Compare the dictionary keys of items in the room with the input the player has entered, storing matches in a new set.
                matchSet = set(splitInput).intersection(player.inventory.keys())

                # Convert set of matching keys to a list
                matches = list(matchSet)

                if bool(matches):
                    return player.inventory[matches[0]].description

                else:
                    return "Unable to find item."

            elif command == "help":
                return self.helpText

            else:
                return "No such command. You are currently in the Inventory Menu - Use 'help' to display a list of commands."

    def TakeItem(self, player, userInput):
        # Compare the dictionary keys of items in the room with the input the player has entered, storing matches in a new set.
        matchSet = set(userInput).intersection(self.dungeon.rooms[player.currentRoom].items.keys())

        # Convert set of matching keys to a list
        matches = list(matchSet)

        # If at least one match found (set is not empty)
        if bool(matches):
            output = self.dungeon.rooms[player.currentRoom].items[matches[0]].pickupText

            # Add first item that matches to the inventory
            player.inventory[self.dungeon.rooms[player.currentRoom].items[matches[0]].name] = self.dungeon.rooms[player.currentRoom].items[matches[0]]

            # Remove item from the room
            del(self.dungeon.rooms[player.currentRoom].items[matches[0]])

            return output

        else:
            return "Unable to take item."

    def DropItem(self, player, splitInput):

        itemName = splitInput[1]

        # Get item from inventory
        if player.inventory[itemName] is not None:
            itemToDrop = player.inventory[itemName]

        del player.inventory[itemName]

        # Add item to room
        self.dungeon.rooms[player.currentRoom].items[itemToDrop.name] = itemToDrop

        return "You drop " + itemToDrop.description

    def Look(self, player):
        # Print room description
        output = "\n" + self.dungeon.rooms[player.currentRoom].description

        # Check for items
        for item in self.dungeon.rooms[player.currentRoom].items:
            output = output + ("\n" + self.dungeon.rooms[player.currentRoom].itemPlacement[item])

        # Check for npcs
        for npc in self.dungeon.rooms[player.currentRoom].npcs:
            output = output + ("\n" + self.dungeon.rooms[player.currentRoom].npcPlacement[npc])

        # Check for other players
        for playerClient in self.dungeon.players:
            if (self.dungeon.players[playerClient].currentRoom == player.currentRoom) and (self.dungeon.players[playerClient] != player):
                output = output + ("\n" + self.dungeon.players[playerClient].name + " is standing nearby.")

        return output

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
                self.messagePlayers(player, player.name + " leaves the room.", True)

                player.currentRoom = newRoom

                self.messagePlayers(player, player.name + " enters the room.", True)

                return "\n" + moveDirection[0] + "\n" + self.dungeon.rooms[player.currentRoom].entryDescription

        return "Please enter a valid direction."

    def Say(self, player, userInput, roomChat=True):
        # Remove the 'say' command from the input.
        del userInput[0]
        message = ' '.join(userInput)

        # Check if the message should be sent to all players in the dungeon, or just players in the current room.
        if roomChat is True:
            self.messagePlayers(player, player.name + " says: '" + message + "'", True)

        else:
            self.messagePlayers(player, player.name + " says: '" + message + "'", False)

        # Return the message to be displayed to the speaker.
        return "You say: '" + message + "'"

    # Outputs a message to other players. If sameRoomOnly is set to true, the message is only sent to players
    # in the same room as the player sending the message.
    def messagePlayers(self, player, message, sameRoomOnly=True):
        # For all other players in the game (excluding the speaker) display the message.
        for playerClient in self.dungeon.players:
            if self.dungeon.players[playerClient] != player:

                # If the message should only be hear by players in the same room
                if sameRoomOnly is True:
                    if self.dungeon.players[playerClient].currentRoom == player.currentRoom:
                        server.Output(playerClient, message)
                else:
                    server.Output(playerClient, message)

    # Parse specific commands to call server functions.
    def parseServerCommand(self, player, command, splitInput):

        # Remove the command from the input
        del splitInput[0]
        value = ' '.join(splitInput)

        # Change player name
        if command == '#name':
            self.messagePlayers(player, "<font color=magenta>" + player.name + " has changed their name to " + value.capitalize() + ".</font>", False)
            player.name = value.capitalize()
            #server.Output("#name " + player.name) broken!!!! needs player client.!
            return "Name changed to " + player.name



