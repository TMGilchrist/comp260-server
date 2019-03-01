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

        # The rooms of the dungeon.
        self.rooms = {}

        # Dictionary of players. {Client : Player}
        self.players = {}
        self.playersLock = threading.Lock()

        # Dictionary of ai agents
        self.agents = {}

        # Init colorama
        init()

        # A description of the dungeon that is shown at the start of the game.
        self.description = "----------------------------------------------------------\n" \
                           + Fore.RED + "You descend the worn steps into the cool dark of the Dungeon. \n" \
                           "What awaits you within?\n" + Fore.RESET + \
                           "----------------------------------------------------------\n"

        # Set up pre-defined rooms
        self.defaultRooms = room.DefaultRooms()
        self.cityRooms = room.DesertCity()

        # The room the player will start in
        self.startRoom = ''

    # Setup the rooms of the dungeon. Default setup for testing.
    def SetupDefaultRooms(self):
        self.rooms["Entrance"] = self.defaultRooms.Entrance
        self.rooms["Antechamber"] = self.defaultRooms.Antechamber
        self.rooms["Tavern"] = self.defaultRooms.Tavern

        # Define which room the player should begin in
        self.startRoom = self.rooms["Entrance"].name

    def SetupCityRooms(self):
        self.rooms["SouthGate"] = self.cityRooms.SouthGate
        self.rooms["SouthGateApproach"] = self.cityRooms.SouthGateApproach
        self.rooms["SouthRoad"] = self.cityRooms.SouthRoad
        self.rooms["GreatPlaza"] = self.cityRooms.GreatPlaza
        self.rooms["Market"] = self.cityRooms.Market
        self.rooms["TempleWay"] = self.cityRooms.TempleWay
        self.rooms["TempleSteps"] = self.cityRooms.TempleSteps
        self.rooms["Temple"] = self.cityRooms.Temple
        self.rooms["PalaceWay"] = self.cityRooms.PalaceWay

        self.startRoom = self.rooms["SouthGateApproach"].name

    # Move from a room in a direction
    def Move(self, currentRoom, direction):
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
