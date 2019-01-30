from Scripts import item


# A room in the Dungeon
class Room:

    def __init__(self, name, entryDescription, description, items={}, itemPlacement={}, north="", east="", south="", west=""):
        # The room name, used to identify it when moving between rooms
        self.name = name

        # A short description shown when the player enters a room
        self.entryDescription = entryDescription

        # A verbose description given when the player uses the LOOK command
        self.description = description

        # A dictionary of connections with other rooms.
        # Connections are represented by the name of the connected room, stored as a string.
        self.connections = dict()

        # Assign connections. Void connections are represented by ""
        self.connections["north"] = north
        self.connections["east"] = east
        self.connections["south"] = south
        self.connections["west"] = west

        # A dictionary of any items in the room
        self.items = items

        self.itemPlacement = itemPlacement


# Pre-constructed rooms that can be added during testing.
class DefaultRooms:

    def __init__(self):
        # Get predefined items
        self.gameItems = item.Items()

        self.Entrance = Room("Entrance", "You return to the entrance of the dungeon.",
                             "You are in a bare stone room with a door to the south. "
                             "Old iron chains hang from the ceiling and clusters of mushrooms grow from cracks in the walls. \n"
                             "There is a small iron door to the South.",
                             items={"sword": self.gameItems.sword},
                             itemPlacement={"sword": "There is a sword leaning against one wall."},
                             south="Antechamber")

        self.Antechamber = Room("Antechamber", "You enter a large antechamber, statues line the walls.",
                                "You are in a large chamber with a vaulted ceiling supported by rows of pillars. There is a small iron door at the North end. "
                                "On the Southern wall, an impressive set of bronze-banded double doors stands shut.",
                                items={"shield": self.gameItems.shield},
                                itemPlacement={"shield": "There is a shield behind one of the statues."},
                                north="Entrance")


# Add further classes for the layouts of real dungeons.
