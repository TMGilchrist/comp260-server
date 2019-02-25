from Scripts import item
from Scripts import npc


# A room in the Dungeon
class Room:

    def __init__(self, name, entryDescription, description, items={}, itemPlacement={}, npcs={}, npcPlacement={}, north="", east="", south="", west=""):
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

        # Items in the room
        self.items = items

        # Descriptions of the placement of any items in the room
        self.itemPlacement = itemPlacement

        # Npcs in the room
        self.npcs = npcs

        # Descriptions of the placement of any npcs in the room
        self.npcPlacement = npcPlacement




# Pre-constructed rooms that can be added during testing.
class DefaultRooms:

    def __init__(self):
        # Get predefined items and characters
        self.gameItems = item.Items()
        self.npcs = npc.Npcs()

        self.Entrance = Room("Entrance", "You return to the entrance of the dungeon.",
                             "You are in a bare stone room with a door to the South and another to the East. "
                             "Old iron chains hang from the ceiling and clusters of mushrooms grow from cracks in the walls. \n"
                             "There is a small iron door to the South. \n"
                             "There is a wooden door to the east.",
                             items={"sword": self.gameItems.sword},
                             itemPlacement={"sword": "There is a sword leaning against one wall."},
                             east="Tavern",
                             south="Antechamber")

        self.Antechamber = Room("Antechamber", "You enter a large antechamber, statues line the walls.",
                                "You are in a large chamber with a vaulted ceiling supported by rows of pillars. There is a small iron door at the North end. "
                                "On the Southern wall, an impressive set of bronze-banded double doors stands shut.",
                                items={"shield": self.gameItems.shield},
                                itemPlacement={"shield": "There is a shield behind one of the statues."},
                                north="Entrance")

        self.Tavern = Room("Tavern", "You enter the tavern. The old barkeep looks up as the door swings shut behind you.",
                           "You are in a small tavern with a low roof. The room is lit by lanterns hanging from the ceiling and there are a handful of patrons sitting at the tables.",
                           npcs={"Barkeep": self.npcs.oldBarkeep, "Patron": self.npcs.barPatron},
                           npcPlacement={"Barkeep": "An old man stands behind the bar.", "Patron": "A drunk patron sits at a table nearby."},
                           west="Entrance")


# Add further classes for the layouts of real dungeons.
