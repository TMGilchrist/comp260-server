from colorama import Fore, Back, Style, init
import socket
from Scripts import server
from PyQt5 import QtGui

class InputManager:

    def __init__(self, player, dungeon):
        # Store the player that has instantiated an inputManager
        self.player = player

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
                            "<font color='Green'><direction>: </font> Directions are North, East, South and West. <br>" \
                            "<font color='Green'>Look: </font> Look at the room around you. <br>" \
                            "<font color='Green'>Take <object>: </font>Attempt to take an object or item and add it to your inventory. <br>" \
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

        # Initialise colorama
        init()

    def GetInput(self, inputTitle=''):
        print(inputTitle)
        newInput = input(Fore.MAGENTA + "Enter a command: " + Fore.RESET)

        return newInput.lower()

    def HandleInput(self, userInput):
        print(Fore.BLUE + "Handle Input: " + userInput + Fore.RESET)

        # Split string into individual words
        splitInput = userInput.split(' ')
        command = splitInput[0]

        if command == "exit":
            return "exit"

        elif command == "help":
            return self.helpTextHTML

        # Check for GO command.
        elif command == "go":
            return self.Move(userInput)

        elif command == "look":
            return self.Look()

        elif command == "take":
            return self.TakeItem(splitInput)

        elif command == "say":
            return self.Say(splitInput)

        elif command == "inventory":
            self.inventoryActive = True
            return self.player.CheckInventory()
            # self.InventoryMenu()

        else:
            return "No such command - Use 'help' to display a list of commands."

    def InventoryMenu(self):
        self.inventoryActive = True

        # Keep menu open while the user is in the inventory
        while self.inventoryActive:

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
            output = self.dungeon.rooms[self.player.currentRoom].items[matches[0]].pickupText

            # Add first item that matches to the inventory
            # self.player.inventory.append(self.dungeon.rooms[self.player.currentRoom].items[matches[0]])
            self.player.inventory[self.dungeon.rooms[self.player.currentRoom].items[matches[0]].name] = self.dungeon.rooms[self.player.currentRoom].items[matches[0]]

            # Remove item from the room
            del(self.dungeon.rooms[self.player.currentRoom].items[matches[0]])

            return output

        else:
            return "Unable to take item."

    def Look(self):
        # Print room description
        # print("\n" + self.dungeon.rooms[self.player.currentRoom].description)
        output = "\n" + self.dungeon.rooms[self.player.currentRoom].description

        # Check for items
        for item in self.dungeon.rooms[self.player.currentRoom].items:
            output = output + ("\n" + self.dungeon.rooms[self.player.currentRoom].itemPlacement[item])

        # Check for npcs
        for npc in self.dungeon.rooms[self.player.currentRoom].npcs:
            output = output + ("\n" + self.dungeon.rooms[self.player.currentRoom].npcPlacement[npc])

        return output

    def Move(self, userInput):
        if "north" in userInput:
            self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "north")

        elif "east" in userInput:
            self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "east")

        elif "south" in userInput:
            self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "south")

        elif "west" in userInput:
            self.player.currentRoom = self.dungeon.Move(self.player.currentRoom, "west")

        # Return empty string to satisfy serverOutput in gameloop.
        # Output here is done in dungeon.Move function.
        return ''

    def Say(self, userInput):
        del userInput[0]
        return self.player.name + " says '" + ' '.join(userInput) + "'"
