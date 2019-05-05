from Scripts import item, npc


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


class DesertCity:

    def __init__(self):
        # Get predefined items and characters
        self.gameItems = item.Items()
        self.npcs = npc.Npcs()

        self.Template = Room("Name",
                             "Entry Desc",
                             "Desc",
                             )

        self.SouthGate = Room("SouthGate",
                              "You enter the courtyard inside the South Gate.",
                              "The towering bronze doors of the South Gate stand half open, and a steady stream of merchants and travellers wind their way through. "
                              "\nThrough the gates to the <font color=Gold>South</font>, you can see the windswept desert. \nTo the <font color=Gold>NorthM/font, a road leads into the city.",
                              items={"shield": self.gameItems.shield},
                              itemPlacement={"shield": "One of the guards has left their shield leaning against a wall."},
                              north="SouthRoad",
                              south="SouthGateApproach")

        self.SouthGateApproach = Room("SouthGateApproach",
                                      "Sand bites your face as you leave the shelter of the city walls and face the open desert.",
                                      "The sands of the desert stretch away to the south. <font color=Gold>North</font>, city walls stretch across the dunes. Behind them you can see sunlight gleaming off bronze-topped towers.",
                                      north="SouthGate")

        self.SouthRoad = Room("SouthRoad",
                              "You walk along a wide, paved road lined with tall sandstone buildings.",
                              "Merchants lead mules up the road towards the heart of the city, while busy citizens push past you. The tall buildings jostling for space on either side of the road shade you from the hot sun. "
                              "\nTo the <font color=Gold>South</font>, you can see the towers of the South Gate. \n<font color=Gold>Northwards</font>, the road continues towards the heart of the city.",
                              north="GreatPlaza",
                              south="SouthGate")

        self.GreatPlaza = Room("GreatPlaza",
                               "The street opens into a great plaza.",
                               "You are standing in a large square at the heart of the city. Buildings rise around you and people mill back and forth, shouting in a myriad of strange languages. In the center of the plaza is a large monument dedicated to some ancient king. "
                               "\nTo the <font color=Gold>North</font>, an empty road leads towards a huge building in the distance. \nWide streets run <font color=Gold>West</font> and <font color=Gold>South</font> out of the plaza. "
                               "\nTo the East is an archway into a covered market.",
                               north="TempleWay",
                               south="SouthRoad",
                               east="Market",
                               west="PalaceWay")

        self.Market = Room("Market",
                           "You enter a covered market.",
                           "The market is cool and dark beneath silk awnings that rustle softly. The air is thick with the smell of spices, sweat and coin. "
                           "\nTo the <font color=Gold>West</font> is an archway to the plaza beyond.",
                           items={"sword": self.gameItems.sword},
                           itemPlacement={"sword": "There is a sword lying on a blacksmith's market stall. A sign next to it reads: 'Free sample'"},
                           npcs={"spiceMerchant": self.npcs.spiceMerchant},
                           npcPlacement={"spiceMerchant": "There is a spice merchant crying his wares nearby."},
                           west="GreatPlaza")

        self.TempleWay = Room("TempleWay",
                              "You walk onto a dusty road that is almost deserted.",
                              "The road is almost completely deserted, with only a few people occasionally passing by. The tall buildings give way to gardens lining the street. "
                              "\nTo the North, a huge set of stone steps, paved with bronze, lead upwards towards a huge building. "
                              "\nTo the South, you can see the wide expanse of the Great Plaza.",
                              south="GreatPlaza",
                              north="TempleSteps")

        self.TempleSteps = Room("TempleSteps",
                                "You begin to walk the bronze steps.",
                                "Weathered bronze statues line the steps. Beyond them, the city is spread out below the steps. "
                                "\nTo the South, the steps end, joining an empty street. "
                                "\nTo the North, the steps end before a large building.",
                                items={"old coin": self.gameItems.oldCoin},
                                itemPlacement={"old coin": "There is an old coin lying on one of the steps."},
                                south="TempleWay",
                                north="Temple")

        self.Temple = Room("Temple",
                           "You stand before the temple doors.",
                           "The bronze doors of the temple are locked.",
                           south="TempleSteps")

        self.PalaceWay = Room("PalaceWay",
                              "You walk onto a well kept road heading West towards the domes of a large palace",
                              "The road ends abruptly in a barrier with a sign in front of it. The sign reads: 'No entry, still under construction.'",
                              east="GreatPlaza")

# Add further classes for the layouts of real dungeons.
