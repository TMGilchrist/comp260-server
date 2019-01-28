# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon


class Game:
    player = player.Player('NewCharacter')

    gameIsRunning = True

    currentInput = ''

    dungeon = dungeon.Dungeon(player)

    # Main game loop
    while gameIsRunning == True:
        currentInput = player.inputManager.GetInput()

        # Quit game
        if currentInput == "exit":
            gameIsRunning = False





