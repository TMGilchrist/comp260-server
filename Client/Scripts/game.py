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

    def __init__(self, networkSocket=''):
        self.gameIsRunning = True
        self.isConnected = False

        self.currentInput = ''

        self.networkSocket = networkSocket
        self.myReceiveThread = ''

        # Init colourama
        init()

        self.inputManager = inputManager.InputManager()

        # Queue of messages from the server
        self.messageQueue = Queue()

        # Connect to the server
        self.Connect()

    def Connect(self):
        # While client not connected to a server
        while self.isConnected == False:

            self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect to server
            try:
                self.networkSocket.connect(("127.0.0.1", 8222))
                self.isConnected = True
                print("Initial server connect successful.")

                self.myReceiveThread = threading.Thread(target=self.receiveThread, args=(self.networkSocket,))
                self.myReceiveThread.start()

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

                if(self.isConnected == True):
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
                    time.sleep(0.25)

                    # Receive response
                    while self.messageQueue.qsize() > 0:
                        print(self.messageQueue.get())

                except socket.error:
                    print(Fore.RED + "Server lost." + Fore.RESET)
                    self.isConnected = False
                    self.networkSocket = None

    def Reconnect(self):
        connected = False
        self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while not connected:
            try:
                print("Attempting to reconnect.")
                self.networkSocket.connect(("127.0.0.1", 8222))
                # self.GetServerOutput()
                connected = True

            except socket.error:
                print(Fore.RED + "Unable to connect." + Fore.RESET)
                time.sleep(1)

    def GetServerOutput(self):

        # Receive startup server output
        try:
            data = self.networkSocket.recv(4096)
            print(data.decode("utf-8"))

        except socket.error:
            print(Fore.RED + "Server lost." + Fore.RESET)

    def receiveThread(self, serverSocket):
        while self.gameIsRunning:
            if self.isConnected:
                try:
                    message = serverSocket.recv(4096).decode("utf-8")
                    self.messageQueue.put(message)

                except socket.error:
                    self.isConnected = False
                    print(Fore.RED + "Lost server" + Fore.RESET)

            else:
                print(Fore.RED + "No server" + Fore.RESET)
                time.sleep(5.0)







