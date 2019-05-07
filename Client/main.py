from Scripts import game, jsonIO, encryption
import socket
import time
import sys
import threading
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtCore import QCoreApplication

import bcrypt

# Get UI file and load as window.
qtCreatorFile = "Forms/ClientMain.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Load in login screen file.
modalDialogFile = "Forms/loginScreen.ui"
Ui_loginScreen, QtBaseClass = uic.loadUiType(modalDialogFile)


# Login screen modal dialog.
class LoginScreen(QtWidgets.QDialog, Ui_loginScreen):

    def __init__(self, game):
        QtWidgets.QDialog.__init__(self)
        Ui_loginScreen.__init__(self)
        self.setupUi(self)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.loginMessageText.setText("")

        self.game = game

        self.encryptionManager = encryption.EncryptionManager(self.game.networkSocket)  # self.game.networkSocket is apparently empty here??

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

    # Sends a login request to the sever with the user's username. The server will then respond with password verification.
    def Login(self):
        try:
            self.encryptionManager.serverSocket = self.game.networkSocket

            # Get user input and strip whitespace. Doing this until I can prevent the user from entering spaces in the edit box.
            username = self.usernameInput.text().replace(' ', '')
            password = self.passwordInput.text().replace(' ', '')

            self.encryptionManager.plaintextPassword = password
            self.encryptionManager.username = username

            jsonIO.JsonIO.Output(self.game.networkSocket, "##loginRequest " + username)

        except socket.error:
            print("No server found.")
            self.loginMessageText.setText("Could not connect to server!")

        except ValueError:
            print("No server found.")
            self.loginMessageText.setText("Could not connect to server!")

    # Sends a request for a new account.
    def NewAccount(self):
        try:
            # Get user input
            username = self.usernameInput.text().replace(' ', '')
            password = self.passwordInput.text().replace(' ', '')

            saltedHashedPassword = self.encryptionManager.SaltAndHashPassword(password)

            jsonIO.JsonIO.Output(self.game.networkSocket, "##newUser " + username + " " + saltedHashedPassword)

        except socket.error:
            print("No server found.")
            self.loginMessageText.setText("Could not connect to server!")

        except ValueError:
            print("No server found.")
            self.loginMessageText.setText("Could not connect to server!")

    # Called each timer interval
    def timerEvent(self):

        # Check for messages to display
        if self.game.loginMessageQueue.qsize() > 0:
            message = self.game.loginMessageQueue.get()

            splitInput = message.split(' ')
            command = splitInput[0]

            del splitInput[0]
            message = ' '.join(splitInput)

            print("Command: " + command)
            print("Message; " + message)

            # Check for successful login
            if command == '##LoginSuccess':
                print("Login should now proceed!")

                self.loginMessageText.setText("Login success!")
                self.game.loggedIn = True
                self.timer.stop()
                self.accept()

            # Pass the salt to the encryption manager to verify login.
            elif command == '##SaltForVerification':
                self.encryptionManager.VerifyPassword(message)

            elif command == '##NoUser':
                self.loginMessageText.setText("No user exists with that username.")

            elif command == '##WrongPass':
                self.loginMessageText.setText("Password is incorrect.")

            elif command == '##LoginConflict':
                self.loginMessageText.setText("This user is already registered as logged in.")

            elif command == '##NewUserSuccess':
                # Show new user message
                self.loginMessageText.setText("New user created!")

            elif command == '##NewUserConflict':
                self.loginMessageText.setText("An account with this username already exists.")

            else:
                print("Login screen message log fallthrough: " + command + ' ' + message)
                pass

    # Called when the login screen closes.
    def closeEvent(self, event):
        print("Dialog closing")
        self.timer.stop()
        #self.close()
        #self.reject()
        self.done(0)
        #app.quit()


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

        # If the player is in the main game and should receive game-related messages.
        self.inGame = False

        self.ShowLoginScreen()

        self.SetLabel(self.playerNameLabel, '')

        self.SetLabel(self.currentRoomLabel, '')

        """--------------------
              Listeners
        --------------------"""

        # When enter is pressed in input box.
        self.userInput.returnPressed.connect(self.UserInputSubmit)

        #app.aboutToQuit.connect(self.closeEvent)

    # Open the login screen as a modal dialog.
    def ShowLoginScreen(self):
        self.dialog = LoginScreen(self.game)

        # For Modal dialogs
        if self.dialog.exec_():
            print("Accepted")
            self.show()

        else:
            print("Not accepted")
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

        if self.game.loggedIn is True:
            print("Send logout")
            self.game.loggedIn = False
            jsonIO.JsonIO.Output(self.game.networkSocket, "##logout")

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

        # Using this to stop the client as app_exec() not returning properly when closing login dialog otherwise.
        # Not working
        app.quit()

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
    #window.show()

    # Event loop.
    sys.exit(app.exec_())





