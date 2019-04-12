from Scripts import game, jsonIO
import socket
import time
import sys
import threading
from PyQt5 import QtCore, QtGui, uic, QtWidgets

# Get UI file and load as window.
qtCreatorFile = "../Forms/ClientMain.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Load in login screen file.
modalDialogFile = "../Forms/loginScreen.ui"
Ui_loginScreen, QtBaseClass = uic.loadUiType(modalDialogFile)


# Login screen modal dialog.
class LoginScreen(QtWidgets.QDialog, Ui_loginScreen):

    def __init__(self, game):
        QtWidgets.QDialog.__init__(self)
        Ui_loginScreen.__init__(self)
        self.setupUi(self)

        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        #self.setWindowFlag(QtCore.Qt.Dialog)

        self.game = game

        # Setup timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

        """--------------------
              Listeners
        --------------------"""

        # On login button press
        self.loginButton.clicked.connect(self.Login)

        self.newAccountButton.clicked.connect(self.NewAccount)

    def Login(self):
        # Get user input and strip whitespace. Doing this until I can prevent the user from entering spaces in the edit box.
        username = self.usernameInput.text().replace(' ', '')
        password = self.passwordInput.text().replace(' ', '')

        jsonIO.JsonIO.Output(self.game.networkSocket, "#login " + username + " " + password)

    def NewAccount(self):
        # Get user input
        username = self.usernameInput.text().replace(' ', '')
        password = self.passwordInput.text().replace(' ', '')

        jsonIO.JsonIO.Output(self.game.networkSocket, "#newUser " + username + " " + password)

        # self.close()

    # Called each timer interval
    def timerEvent(self):
        # Check for messages to display
        if self.game.messageQueue.qsize() > 0:
            message = self.game.messageQueue.get()

            # Check for successful login
            if message == '#LoginSuccess':
                self.timer.stop()
                self.accept()

    def closeEvent(self, event):
        print("Dialog closing")
        self.timer.stop()
        #self.reject()


# PyQT application.
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, game):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.game = game
        self.dialog = ''

        # Setup timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(100)

        self.ShowLoginScreen()

        """--------------------
              Listeners
        --------------------"""

        # When enter is pressed in input box.
        self.userInput.returnPressed.connect(self.UserInputSubmit)

    # Open the login screen as a modal dialog.
    def ShowLoginScreen(self):
        self.dialog = LoginScreen(self.game)

        # For Modal dialogs
        if self.dialog.exec_():
            print("Accepted")

        else:
            print("not accepted")
            self.close()

    # Test function to print stuff
    def PrintStuff(self):
        print("Clicking button")

    # Called when user sends input
    def UserInputSubmit(self):
        # Try to send input to server
        try:
            newInput = self.userInput.text().lower()
            print("User input submitted")

            jsonIO.JsonIO.Output(self.game.networkSocket, newInput)

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
        print("Parsing command string.")
        print("Command string = " + commandString)

        # Split string by spaces
        splitString = commandString.split(' ')

        # Get first substring which is the #command and remove from the main string
        command = splitString[0]
        del splitString[0]

        # Set the rest of the string to the value being set
        value = ' '.join(splitString)
        print("Value = " + value + "\n")

        # Change labels to match new values
        if command == '#name':
            self.SetLabel(self.playerNameLabel, value)

        elif command == '#room':
            self.SetLabel(self.currentRoomLabel, value)

        elif command == '#exit':
            self.close()

    # Updates a labels text
    def SetLabel(self, labelToSet, newValue):
        labelToSet.setText(newValue)

    # Called when the user closes the application window.
    def closeEvent(self, event):

        print("Client closing")

        self.game.networkSocket.close()
        self.game.networkSocket = None

        self.game.isConnected = False
        self.game.clientIsRunning = False

        if self.game.currentBackgroundThread is not None:
            self.game.currentBackgroundThread.join()
            print("joining background thread")

        if self.game.currentReceiveThread is not None:
            self.game.currentReceiveThread.join()
            print("joining receive thread")

        print("client closed.")


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





