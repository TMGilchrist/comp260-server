from Scripts import game
import socket
import time
import sys
import threading
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

            # Check for hash commands.
            if message[0] == '#':
                self.ParseCommand(message)

            else:
                self.textDisplayMain.append(message)

    # Parse server commands. This could call functions for specific command types - set data etc
    def ParseCommand(self, commandString):
        print("Parsing command args")
        print("Command string = " + commandString)

        # Split string by spaces
        splitString = commandString.split(' ')

        # Get first substring which is the #command and remove from the main string
        command = splitString[0]
        del splitString[0]

        # Set the rest of the string to the value being set
        value = ' '.join(splitString)
        print("Value = " + value)

        # Change labels to match new values
        if command == '#name':
            self.SetLabel(self.playerNameLabel, value)

        elif command == '#room':
            self.SetLabel(self.currentRoomLabel, value)

    # Updates a labels text
    def SetLabel(self, labelToSet, newValue):
        labelToSet.setText(newValue)

    # Called when the user closes the application window.
    def closeEvent(self, event):

        self.game.networkSocket.close()
        self.game.networkSocket = None

        self.game.isConnected = False
        self.game.clientIsRunning = False

        if self.game.currentBackgroundThread is not None:
            self.game.currentBackgroundThread.join()

        if self.game.currentReceiveThread is not None:
            self.game.currentReceiveThread.join()


if __name__ == "__main__":
    # Create qtApplication.
    app = QtWidgets.QApplication(sys.argv)

    # Create new game.
    newGame = game.Game()

    # Start background thread for the game. This handles connection to the server.
    newGame.currentBackgroundThread = threading.Thread(target=newGame.BackgroundThread)
    newGame.currentBackgroundThread.start()

    # Create and show qtWindow.
    window = MyApp(newGame)
    window.show()

    # Event loop.
    sys.exit(app.exec_())





