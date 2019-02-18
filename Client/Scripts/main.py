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
        self.timer.start(500)

        self.textDisplayMain.append("Window init.")
        self.testButton.clicked.connect(self.PrintStuff)

        # When enter is pressed in input box.
        self.userInput.returnPressed.connect(self.UserInputSubmit)

    def PrintStuff(self):
        print("Clicking button")

    def UserInputSubmit(self):
        input = self.userInput.text().lower()

        print("User input submitted")

        self.game.networkSocket.send(input.encode())

        self.userInput.setText("")



    def timerEvent(self):
        print("Timer event")

        # self.textDisplayMain.append("Timer event")
        if self.game.messageQueue.qsize() > 0:
            #print(self.game.messageQueue.get())
            self.textDisplayMain.append(self.game.messageQueue.get())

        # fooVar = self.game.messageQueue.get()

    """def keyPressEvent(self, event):
        print("keypress event")

        if event.key() == QtCore.Qt.Key_Return:
            self.textDisplayMain.append("Input")"""

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





