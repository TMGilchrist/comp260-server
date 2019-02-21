from Scripts import inputManager
import socket
import time
import threading

from queue import *
from colorama import Fore, init


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, qtWindow=''):
        self.gameIsRunning = True
        self.isConnected = False

        self.currentInput = ''

        self.networkSocket = ''
        self.currentReceiveThread = ''
        self.currentBackgroundThread = ''

        # Init colourama
        init()

        self.qtWindow = qtWindow
        self.inputManager = inputManager.InputManager()

        # Queue of messages from the server
        self.messageQueue = Queue()

        # Connect to the server

    def Connect(self):
        # While client not connected to a server
        while self.isConnected == False:

            self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server
            try:
                self.networkSocket.connect(("127.0.0.1", 8222))
                self.isConnected = True
                print("Initial server connect successful.")

                self.currentReceiveThread = threading.Thread(target=self.receiveThread, args=(self.networkSocket,))
                self.currentReceiveThread.start()

            except socket.error:
                self.isConnected = False
                print(Fore.RED + "Could not connect to server." + Fore.RESET)

            if self.isConnected == True:
                try:
                    confirmationData = "Connected to the server"
                    # self.networkSocket.send(confirmationData.encode())

                except socket.error:
                    self.isConnected = False
                    self.networkSocket = None

            if self.isConnected == False:
                print(Fore.RED + "No server" + Fore.RESET)
                time.sleep(1.0)

    # Main game code
    def GameLoop(self):
        print("Client gameloop entered.")

        # Get intro output
        #self.GetServerOutput()

        # Main server loop
        while self.gameIsRunning:

            # While client not connected to a server
            while self.isConnected == False:
                print(Fore.RED + "Not connected." + Fore.RESET)

                # Check if socket is null
                if self.networkSocket is None:
                    self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to server
                try:
                    self.networkSocket.connect(("127.0.0.1", 8222))
                    self.isConnected = True
                    print("Server connect successful.")

                except socket.error:
                    self.isConnected = False
                    print(Fore.RED + "Could not connect to server." + Fore.RESET)

                if self.isConnected == True:
                    try:
                        confirmationData = "Client: Client connected to the server"
                        # self.networkSocket.send(confirmationData.encode())

                    except socket.error:
                        self.isConnected = False
                        self.networkSocket = None

                if self.isConnected == False:
                    print(Fore.RED + "No server" + Fore.RESET)
                    time.sleep(1.0)

            while self.isConnected == True:

                # Get user input
                self.currentInput = self.inputManager.GetInput("\nYou stand at the ready.")

                try:
                    # Send input
                    self.networkSocket.send(self.currentInput.encode())
                    time.sleep(0.5)

                    # Receive response
                    while self.messageQueue.qsize() > 0:
                        # print(self.messageQueue.get())
                        self.qtWindow.textDisplayMain.append(self.messageQueue.get())

                except socket.error:
                    print(Fore.RED + "Server lost." + Fore.RESET)
                    self.isConnected = False
                    self.networkSocket = None

    def receiveThread(self, serverSocket):
        print(Fore.CYAN + "Receive thread running." + Fore.RESET)

        while self.isConnected is True:
            try:
                message = serverSocket.recv(4096).decode("utf-8")
                self.messageQueue.put(message)

            except socket.error:
                self.isConnected = False
                self.messageQueue.put("<font color=Red>Server lost.</font>")
                print(Fore.RED + "Server lost." + Fore.RESET)

    def BackgroundThread(self):
        print(Fore.CYAN + "Background thread running." + Fore.RESET)
        self.isConnected = False

        while self.isConnected is False:
            try:
                print(Fore.CYAN + "Background Thread: attempting to connect." + Fore.RESET)
                self.messageQueue.put("<font color=Cyan>Attempting to connect to server.</font>")

                # Find server socket
                self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to server socket
                try:
                    self.networkSocket.connect(("127.0.0.1", 8222))
                    self.isConnected = True
                    print(Fore.CYAN + "Background Thread: Connected to server." + Fore.RESET)
                    self.messageQueue.put("<font color=Cyan>Connected to server.</font>")

                except socket.error:
                    print(Fore.RED + "Background Thread: Failed to connect to the server." + Fore.RESET)
                    self.messageQueue.put("<font color=Red>Failed to connect to the server.</font>")

                # Start the receive thread
                self.currentReceiveThread = threading.Thread(target=self.receiveThread, args=(self.networkSocket,))
                self.currentReceiveThread.start()

                # Sleep after connecting to keep the thread running.
                while self.isConnected is True:
                    time.sleep(1.0)

            except socket.error:
                print(Fore.RED + "No server connection found." + Fore.RESET)
                time.sleep(2.0)

