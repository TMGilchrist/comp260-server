from Scripts import room


# The Dungeon the player explores
class Dungeon:

    # Constructor
    def __init__(self, name, player):
        # The name of the dungeon
        self.name = name

        # The player
        self.player = player

        # The rooms of the dungeon.
        self.rooms = {}

        # A description of the dungeon that is shown at the start of the game.
        self.description = "----------------------------------------------------------\n" \
                           "You descend the worn steps into the cool dark of the Dungeon. \n" \
                           "What awaits you within?\n" \
                           "----------------------------------------------------------\n"

        # Set up pre-defined rooms
        self.defaultRooms = room.DefaultRooms()

        # The room the player will start in
        self.startRoom = ''

    # Setup the rooms of the dungeon. Default setup for testing.
    def SetupDefaultRooms(self):
        self.rooms["Entrance"] = self.defaultRooms.Entrance
        self.rooms["Antechamber"] = self.defaultRooms.Antechamber

        # Define which room the player should begin in
        self.startRoom = self.rooms["Entrance"].name

    # Move from a room in a direction
    def Move(self, currentRoom, direction):
        newRoomName = self.rooms[currentRoom].connections[direction]

        # Check connection is valid
        if newRoomName != "":
            print("\nYou walk " + direction + "\n" + self.rooms[newRoomName].entryDescription)
            return self.rooms[newRoomName].name

        # If connection invalid, stay in currentRoom
        else:
            print("\nThere is nowhere to go in this direction.")
            return currentRoom

