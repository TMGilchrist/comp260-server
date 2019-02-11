# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon
from Scripts import server

from colorama import Fore, init

import socket
import time
import threading


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, client=''):
        self.gameIsRunning = ''
        self.isConnected = ''

        self.currentInput = ''
        self.player = ''
        self.dungeon = ''

        # Init colourama
        init()

        self.networkSocket = ''
        self.myAcceptThread = ''
        self.client = client

        # Dictionary of clients
        self.clients = {}

        # List of lost clients
        self.lostClients = []

        # Data lock for clients
        self.clientsLock = threading.Lock()


    def setup(self, dungeonName):
        self.gameIsRunning = True
        self.currentInput = ''

        self.Connect()

        # Create a player and dungeon
        self.player = player.Player("NewCharacter", 10, self.client)
        self.dungeon = dungeon.Dungeon(dungeonName, self.player)

        # Setup rooms for the dungeon
        self.dungeon.SetupDefaultRooms()

        # Do player setup including storing current dungeon
        self.player.Setup(self.dungeon)

    def Connect(self):
        self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.networkSocket.bind(("127.0.0.1", 8222))
        self.networkSocket.listen(5)

        self.myAcceptThread = threading.Thread(target=self.acceptThread, args=(self.networkSocket,))
        self.myAcceptThread.start()

        #self.client = self.networkSocket.accept()

        # Receive some test data from the client
        #data = self.client[0].recv(4096)
        #print(data.decode("utf-8"))

        #self.isConnected = True

    # Main game code
    def GameLoop(self):
        print("Server in gameloop")

        # Pre-game intro text
        intro = self.dungeon.description + self.player.inputManager.Look()

        #server.Output(self.client, intro)

        # Main server loop
        while self.gameIsRunning:
            self.lostClients = []

            self.clientsLock.acquire()

            # Iterate over clients
            for client in self.clients:
                try:
                    #testString = str(self.clients[client]) + ":" + time.ctime()
                    self.clients[client] += 1
                    #client.send(testString.encode())
                    #print("Sending: " + testString)

                    print("Process client input")
                    print(self.clients[client])

                    self.player.client = client

                    data = client.recv(4096)
                    print(Fore.GREEN + "Client: " + data.decode("utf-8") + Fore.RESET)

                    serverOutput = self.player.inputManager.HandleInput(data.decode("utf-8"))

                    if serverOutput == "exit":
                        self.gameIsRunning = False

                    else:
                        # Send server output. server.Output returns false if not connected.
                        self.isConnected = server.Output(client, serverOutput)

                except socket.error:
                    # Record client as lost
                    self.lostClients.append(client)
                    print("Lost client!")

            # Remove lost clients from clients dictionary
            for client in self.lostClients:
                self.clients.pop(client)

            self.clientsLock.release()
            time.sleep(0.5)

        """
            # Check for client and try to connect if not found
            if self.isConnected == False:
                print("Waiting for client")
                self.client = self.networkSocket.accept()
                self.player.client = self.client

                # Attempt to get input from client
                try:
                    self.isConnected = True
                    print("Client found")

                    data = self.client[0].recv(4096)
                    print(data.decode("utf-8"))

                except socket.error:
                    print("Unable to access client")
                    self.isConnected = False

            # While connected, process client data and output if possible
            while self.isConnected == True:
                try:
                    print("Process client input")

                    data = self.client[0].recv(4096)
                    print(data.decode("utf-8"))

                    serverOutput = self.player.inputManager.HandleInput(data.decode("utf-8"))

                    if serverOutput == "exit":
                        self.gameIsRunning = False

                    else:
                        # Send server output. server.Output returns false if not connected.
                        self.isConnected = server.Output(self.client, serverOutput)

                except socket.error:
                    print("Unable to access client")
                    self.isConnected = False
            """

    # Thread function
    def acceptThread(self, serverSocket):
        while True:
            # Get new client
            new_client = serverSocket.accept()
            print("Added client!")

            # Add new client to dictionary
            self.clientsLock.acquire()
            self.clients[new_client[0]] = 0
            self.clientsLock.release()









