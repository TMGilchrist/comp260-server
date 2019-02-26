from Scripts import npc


class NpcAgent(npc.Npc):

    def __init__(self, name, health, description, home):
        super().__init__(name, health, description)

        # A room in the dungeon where the agent will return to.
        self.home = home
        self.currentRoom = ''

    def Move(self):
        print("")