from Scripts import character


class Npc(character.Character):

    def __init__(self, name, health, description):
        super().__init__(name, health)

        # A description of this npc
        self.description = description


class Npcs:

    def __init__(self):
        self.oldBarkeep = Npc("Morven Tito", 2, "A small, rather nervous looking old man wearing a pair of spectacles.")
        self.barPatron = Npc("Traveus", 1, "A grubby peasant deep in his cups.")

