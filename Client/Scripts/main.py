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

        self.testButton.clicked.connect(self.PrintStuff)

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
            displayText = self.game.messageQueue.get()
            print(displayText)
            self.textDisplayMain.append(displayText)


# Entry point of program
def main():
    print("Entry point of SUD game.\n\n")

    newGame = game.Game(window)
    #newGame.GameLoop()


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





