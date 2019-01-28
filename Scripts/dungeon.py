# The Dungeon the player explores
class Dungeon:

    # The name of the dungeon
    name = ''

    # Dictionary containing the rooms of the dungeon
    rooms = {}

    # The player in the dungeon
    player = ''

    # Constructor
    def __init__(self, player):
        self.player = player

