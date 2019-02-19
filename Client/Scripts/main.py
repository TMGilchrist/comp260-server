from Scripts import game
import socket
import time
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

# Get UI file and load as window.
qtCreatorFile = "../Forms/ClientMain.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


# PyQT application.
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, game):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.game = game

        # Setup timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

        # Send startup message
        self.textDisplayMain.append("Window init.")

        """--------------------
              Listeners
        --------------------"""

        # When enter is pressed in input box.
        self.userInput.returnPressed.connect(self.UserInputSubmit)

    # Test function to print stuff
    def PrintStuff(self):
        print("Clicking button")

    # Called when user sends input
    def UserInputSubmit(self):
        # Try to send input to server
        try:
            newInput = self.userInput.text().lower()
            print("User input submitted")
            self.game.networkSocket.send(newInput.encode())

        except socket.error:
            self.textDisplayMain.append("No server.")

        # Clear input box
        self.userInput.setText("")

    # Called each timer interval
    def timerEvent(self):
        # Check for messages to display
        if self.game.messageQueue.qsize() > 0:
            message = self.game.messageQueue.get()

            if message[0] == '#':
                self.ParseCommand(message)

            else:
                # print(message)
                self.textDisplayMain.append(message)

    # Parse server commands. This could call functions for specific command types - set data etc
    def ParseCommand(self, commandString):
        print("parsing command args")

        # Split string by spaces
        splitString = commandString.split(' ')

        # Get first substring which is the #command and remove from the main string
        command = splitString[0]
        del splitString[0]

        # Set the rest of the string to the value being set
        value = ' '.join(splitString)

        # Change labels to match new values
        if command == '#name':
            self.SetLabel(self.playerNameLabel, value)

        elif command == '#room':
            self.SetLabel(self.currentRoomLabel, value)

    # Updates a labels text
    def SetLabel(self, labelToSet, newValue):
        labelToSet.setText(newValue)

# Entry point of program
def main():
    print("Entry point of SUD game.\n\n")

    newGame = game.Game(window)


if __name__ == "__main__":
    # Create qtApplication
    app = QtWidgets.QApplication(sys.argv)

    newGame = game.Game()

    # Create and show qtWindow
    window = MyApp(newGame)
    window.show()

    #main()

    # Event loop
    sys.exit(app.exec_())





