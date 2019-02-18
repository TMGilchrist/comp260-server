from Scripts import game
import socket
import time
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "../Forms/testForm.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.PrintStuff)

    def PrintStuff(self):
        print("Clicking button")


# Entry point of program
def main():
    print("Entry point of SUD game.\n\n")

    #networkSocket = ClientSetup()

    newGame = game.Game()
    # newGame.setup()
    newGame.GameLoop()


def ClientSetup():
    # Setup network socket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False

    while connected != True:
        try:
            mySocket.connect(("127.0.0.1", 8222))
            print("Connected to server.")
            connected = True
        except socket.error:
            print("Could not connect to server")

    # Send some test data to the server
    testString = "Client connected."
    mySocket.send(testString.encode())

    return mySocket


if __name__ == "__main__":
    #main()
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()

    # Exit application
    sys.exit(app.exec_())





