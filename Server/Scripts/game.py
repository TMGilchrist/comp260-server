# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon
from Scripts import server
from Scripts import inputManager

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
        self.dungeon = ''

        self.inputManager = ''

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

        # Player/Client active during input/output handling
        self.activeClient = ''
        self.activePlayer = ''

    def setup(self, dungeonName):
        self.gameIsRunning = True
        self.currentInput = ''

        self.Connect()

        # Create a dungeon
        self.dungeon = dungeon.Dungeon(dungeonName)

        # Create inputManager
        self.inputManager = inputManager.InputManager(self.dungeon)

        # Setup rooms for the dungeon
        self.dungeon.SetupDefaultRooms()

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
        # intro = self.dungeon.description + self.player.inputManager.Look(self.player)

        #server.Output(self.client, intro)

        # Main server loop
        while self.gameIsRunning:
            self.lostClients = []

            self.clientsLock.acquire()

            while self.commandQueue.qsize() > 0:
                currentCommand = self.commandQueue.get()

                self.activeClient = currentCommand[0]
                self.activePlayer = self.dungeon.players[self.activeClient]

                serverOutput = self.inputManager.HandleInput(self.activePlayer, currentCommand[1].decode("utf-8"))
                server.Output(self.activeClient, '#room ' + self.activePlayer.currentRoom)

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
        print(Fore.CYAN + "Accept thread running." + Fore.RESET)

        clientCount = 0

        while True:
            # Get new client
            new_client = serverSocket.accept()
            print("Added client!")

            # Update number of connected clients
            clientCount += 1

            # Add new client to dictionary
            self.clientsLock.acquire()
            self.clients[new_client[0]] = 0
            self.clientsLock.release()

            # Start a new recieve thread for the client
            newRecieveThread = threading.Thread(target=self.ReceiveThread, args=(new_client[0],))
            newRecieveThread.start()

            # Add a new player to the dungeon.
            self.dungeon.AddPlayer(new_client[0], "Player " + str(clientCount))

            # Send player name to the client
            server.Output(new_client[0], "#name Player " + str(clientCount))

            # Delay to prevent messages being appended to each other in the client receive queue? I think?
            time.sleep(0.001)

            # Send roomName to the client. Not very nice being here.
            # Would be nice to do this at the beginning of the gameloop.
            server.Output(new_client[0], '#room ' + self.dungeon.players[new_client[0]].currentRoom)

    def ReceiveThread(self, client):

        print(Fore.CYAN + "Receive thread running." + Fore.RESET)
        clientIsValid = True

        while clientIsValid == True:
            try:
                # Get data from client and store as a tuple.
                newCommand = (client, client.recv(4096))

                #Add to queue
                self.commandQueue.put(newCommand)

            except socket.error:
                print(Fore.RED + "Lost Client" + Fore.RESET)
                self.lostClients.append(client)
                clientIsValid = False












