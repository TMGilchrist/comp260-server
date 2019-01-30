from Scripts import room


# The Dungeon the player explores
class Dungeon:

    # Constructor
    def __init__(self, name, player):
        self.name = name
        self.player = player
        self.rooms = {}

    # Setup the rooms of the dungeon. Default setup for testing.
    def SetupDefaultRooms(self):
        self.rooms["Start"] = room.Room("Start", "You are in a bare room with a door in front of you.", south="Antechamber")
        self.rooms["Antechamber"] = room.Room("Antechamber", "You are in a large chamber with a vaulted ceiling.", north="Start")

    # Move from a room in a direction
    def Move(self, currentRoom, direction):

        newRoomName = self.rooms[currentRoom].connections[direction]
        return self.rooms[newRoomName].name

