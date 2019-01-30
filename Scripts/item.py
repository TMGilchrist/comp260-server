class Item:

    def __init__(self, name, pickupText, description):
        # The item's name
        self.name = name

        # A short description shown when the player picks up the item
        self.pickupText = pickupText

        # A verbose description of the item
        self.description = description


class Items:

    def __init__(self):
        self.sword = Item("Sword", "You pick up the old sword and stow it in your pack.", "A rusty shortsword.")
        self.shield = Item("Shield", "You retrieve the shield and sling it over your back.", "A cracked wooden shield.")

