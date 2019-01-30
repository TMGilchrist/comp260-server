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
                           "You descend the worn steps into the cool dark of the Dungeon. \nWhat awaits you within?\n" \
                           "----------------------------------------------------------\n"

    # Setup the rooms of the dungeon. Default setup for testing.
    def SetupDefaultRooms(self):
        self.rooms["Start"] = room.Room("Start", "You are in a bare room with a door in front of you.\n", south="Antechamber")
        self.rooms["Antechamber"] = room.Room("Antechamber", "You are in a large chamber with a vaulted ceiling.\n", north="Start")

    # Move from a room in a direction
    def Move(self, currentRoom, direction):
        newRoomName = self.rooms[currentRoom].connections[direction]

        # Check connection is valid
        if newRoomName != "":
            print("\nYou walk " + direction + "\n")
            return self.rooms[newRoomName].name

        # If connection invalid, stay in currentRoom
        else:
            print("\nThere is nowhere to go in this direction. \n")
            return currentRoom

