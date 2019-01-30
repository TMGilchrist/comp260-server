class Item:

    def __init__(self, name, description):
        self.name = name
        self.description = description


class Items:

    def __init__(self):
        self.sword = Item("Sword", "A rusty shortsword.")
        self.shield = Item("Shield", "A cracked wooden shield.")

