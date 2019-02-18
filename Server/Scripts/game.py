# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon
from Scripts import server

from colorama import Fore, init

import socket
import time
import threading
from queue import *


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

        # Queue of commands to be processed
        self.commandQueue = Queue()

    def setup(self, dungeonName):
        self.gameIsRunning = True
        self.currentInput = ''

        self.Connect()

        # Create a player and dungeon
        self.dungeon = dungeon.Dungeon(dungeonName, self.player)
        self.player = player.Player("NewCharacter", 10, self.dungeon, self.client)


        # Setup rooms for the dungeon
        self.dungeon.SetupDefaultRooms()

        # Do player setup including storing current dungeon
        self.player.Setup(self.dungeon)

    def Connect(self):
        self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.networkSocket.bind(("127.0.0.1", 8222))
        self.networkSocket.listen(5)

        self.myAcceptThread = threading.Thread(target=self.AcceptThread, args=(self.networkSocket,))
        self.myAcceptThread.start()

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
                # Start a new recieve thread for each client
                newRecieveThread = threading.Thread(target=self.ReceiveThread, args=(client,))
                newRecieveThread.start()

            while self.commandQueue.qsize() > 0:
                currentCommand = self.commandQueue.get()

                # Update player client -> used in Dungeon.Move
                #self.player.client = currentCommand[0]
                #print("Current client: " + str(self.player.client))

                # Process input and create output
                serverOutput = self.dungeon.players[currentCommand[0]].inputManager.HandleInput(currentCommand[1].decode("utf-8"))

                if serverOutput == "exit":
                    # self.gameIsRunning = False
                    print("This should disconnect the client but not affect the server.")

                else:
                    # Send server output. server.Output returns false if not connected.
                    print(Fore.GREEN + "Sending output to client" + Fore.RESET)
                    print(Fore.GREEN + serverOutput + Fore.RESET)
                    self.isConnected = server.Output(currentCommand[0], serverOutput)


            # Remove lost clients from clients dictionary
            for client in self.lostClients:
                self.clients.pop(client)

            self.clientsLock.release()
            time.sleep(0.5)


    # Thread function
    def AcceptThread(self, serverSocket):
        clientCount = 0

        while True:
            # Get new client
            new_client = serverSocket.accept()
            print("Added client!") # <-- at this point a new player should also be created to map to the client.

            # Update number of connected clients
            clientCount += 1

            # Add new client to dictionary
            self.clientsLock.acquire()
            self.clients[new_client[0]] = 0
            self.clientsLock.release()

            # Add a new player to the dungeon.
            self.dungeon.AddPlayer(new_client[0], "Player " + str(clientCount))

    def ReceiveThread(self, client):
        while self.gameIsRunning:
            try:
                # Get data from client and store as a tuple.
                newCommand = (client, client.recv(4096))

                #Add to queue
                self.commandQueue.put(newCommand)

            except socket.error:
                print(Fore.RED + "Lost Client" + Fore.RESET)
                # self.lostClients.append(client)
                time.sleep(5.0)












