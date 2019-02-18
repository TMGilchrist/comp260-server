from Scripts import room
from Scripts import server
from Scripts import player
from colorama import Fore, Back, Style, init
import threading

# The Dungeon the player explores
class Dungeon:

    # Constructor
    def __init__(self, name):
        # The name of the dungeon
        self.name = name

        # The player
        # self.player = player

        # The rooms of the dungeon.
        self.rooms = {}

        # Dictionary of players. {Client : Player}
        self.players = {}
        self.playersLock = threading.Lock()

        # Init colorama
        init()

        # A description of the dungeon that is shown at the start of the game.
        self.description = "----------------------------------------------------------\n" \
                           + Fore.RED + "You descend the worn steps into the cool dark of the Dungeon. \n" \
                           "What awaits you within?\n" + Fore.RESET + \
                           "----------------------------------------------------------\n"

        # Set up pre-defined rooms
        self.defaultRooms = room.DefaultRooms()

        # The room the player will start in
        self.startRoom = ''

    # Setup the rooms of the dungeon. Default setup for testing.
    def SetupDefaultRooms(self):
        self.rooms["Entrance"] = self.defaultRooms.Entrance
        self.rooms["Antechamber"] = self.defaultRooms.Antechamber
        self.rooms["Tavern"] = self.defaultRooms.Tavern

        # Define which room the player should begin in
        self.startRoom = self.rooms["Entrance"].name

    # Move from a room in a direction
    def Move(self, player, currentRoom, direction):
        newRoomName = self.rooms[currentRoom].connections[direction]

        # Check connection is valid
        if newRoomName != "":
            #server.Output(player.client, "\nYou walk " + direction + "\n" + self.rooms[newRoomName].entryDescription)
            return self.rooms[newRoomName].name

        # If connection invalid, stay in currentRoom
        else:
            #server.Output(player.client, "\nThere is nowhere to go in this direction.")
            return currentRoom

    def AddPlayer(self, client, playerName):
        self.playersLock.acquire()
        self.players[client] = player.Player(playerName, 10, self)
        self.playersLock.release()
