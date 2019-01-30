# A room in the Dungeon
class Room:

    def __init__(self, name, description, north="", east="", south="", west=""):
        self.name = name
        self.description = description
        self.connections = dict()

        # Assign connections. Void connections are represented by ""
        self.connections["north"] = north
        self.connections["east"] = east
        self.connections["south"] = south
        self.connections["west"] = west








