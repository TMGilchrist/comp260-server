# Main game class. Contains gameloop

from Scripts import aiInputManager, npcAgent, inputManager, server, dungeon

from colorama import Fore, init



import socket
import time
import random
import threading
import sys
from queue import *


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, client=''):
        # Legacy
        self.gameIsRunning = ''

        self.server = ''
        self.dungeon = ''

        self.inputManager = ''
        self.aiInputManager = ''

        # Init colourama
        init()

        self.userLocalHost = False
        self.serverIP = "46.101.56.200"
        self.serverPort = 9100

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

        # Agent builder class
        self.aiBuilder = ''

    def setup(self, dungeonName):
        self.gameIsRunning = True

        # Setup network connection
        self.Connect()

        # Create a dungeon
        self.dungeon = dungeon.Dungeon(dungeonName)

        # Create inputManager
        self.inputManager = inputManager.InputManager(self.dungeon)
        self.aiInputManager = aiInputManager.AiInputManager(self.dungeon)

        # Setup rooms for the dungeon
        # self.dungeon.SetupDefaultRooms()
        self.dungeon.SetupCityRooms()

        # Create aiBuilder
        self.aiBuilder = npcAgent.AgentBuilder(self.dungeon)

        # Build and setup agents.
        self.aiBuilder.BuildAgents()
        self.aiBuilder.SetUpAgents()

        # Create processing threads for each agent in the game.
        self.CreateAgentThreads()

    def Connect(self):
        self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to bind to port
        try:
            # Use address specified in command line args
            if len(sys.argv) > 1:
                self.networkSocket.bind((sys.argv[1], 8222))

            elif self.userLocalHost is True:
                self.networkSocket.bind(("127.0.0.1", 8222))

            elif self.serverIP != '' and self.serverPort != '':
                print("Using serverIP")
                self.networkSocket.bind((self.serverIP, self.serverPort))

            # Use default localhost
            else:
                self.networkSocket.bind(("127.0.0.1", 8222))

        except socket.error:
            print("Cannot start server, another instance of the server may be running.")
            exit()

        self.networkSocket.listen(5)

        # Start the client accept thread.
        self.myAcceptThread = threading.Thread(target=self.AcceptThread, args=(self.networkSocket,))
        self.myAcceptThread.start()

    # Main game code
    def GameLoop(self):
        print("Server in gameloop")

        # Main server loop
        while self.gameIsRunning:
            self.lostClients = []

            self.clientsLock.acquire()

            while self.commandQueue.qsize() > 0:
                currentCommand = self.commandQueue.get()

                self.activeClient = currentCommand[0]
                self.activePlayer = self.dungeon.players[self.activeClient]

                # Process user command into output.
                serverOutput = self.inputManager.HandleInput(self.activeClient, self.activePlayer, currentCommand[1].decode("utf-8"))

                if serverOutput is None:
                    serverOutput = "An error has occurred that left serverOutput as NoneType."

                if serverOutput == "exit":
                    # self.gameIsRunning = False
                    print("This should disconnect the client but not affect the server.")

                else:
                    # Send server output. server.Output returns false if not connected.
                    print(Fore.GREEN + "Sending output to client" + Fore.RESET)
                    print(Fore.GREEN + serverOutput + Fore.RESET)
                    server.Server.OutputJson(currentCommand[0], serverOutput)

            # Remove lost clients from clients dictionary
            for client in self.lostClients:
                self.clients.pop(client)

            self.clientsLock.release()
            time.sleep(0.5)

    # Thread to accept clients connecting to the server.
    def AcceptThread(self, serverSocket):
        print(Fore.CYAN + "Accept thread running." + Fore.RESET)

        clientCount = 0

        while True:
            # Get new client
            newClient = serverSocket.accept()
            print("Added client!")

            # Update number of connected clients
            clientCount += 1

            # Add new client to dictionary
            self.clientsLock.acquire()
            self.clients[newClient[0]] = 0
            self.clientsLock.release()

            # Start a new recieve thread for the client
            newRecieveThread = threading.Thread(target=self.ReceiveThread, args=(newClient[0],))
            newRecieveThread.start()

            # Add a new player to the dungeon.
            self.dungeon.AddPlayer(newClient[0], "Player " + str(clientCount))

            # The player associated with the new client
            newPlayer = self.dungeon.players[newClient[0]]

            # Send player name to the client
            server.Server.OutputJson(newClient[0], "#name " + newPlayer.name + "\n")

            # Delay to prevent messages being appended to each other in the client receive queue. Could add delimiters.
            time.sleep(0.5)

            # For all other players in the game display who has joined the game..
            for playerClient in self.dungeon.players:
                if self.dungeon.players[playerClient] != newPlayer:
                    server.Server.OutputJson(playerClient, "<font color=magenta>" + newPlayer.name + " has joined the game! </font>")

            # Send roomName to the client. Not very nice being here.
            # Would be nice to do this at the beginning of the gameloop.
            # Added a space before #room to stop the # appending to the player name for some reason.
            server.Server.OutputJson(newClient[0], '#room ' + newPlayer.currentRoom)

            # Pre-game intro text
            intro = self.dungeon.description + self.inputManager.Look(newPlayer)

            server.Server.OutputJson(newClient[0], intro)

    # Thread to receive input from clients.
    def ReceiveThread(self, client):

        print(Fore.CYAN + "Receive thread running." + Fore.RESET)
        clientIsValid = True

        while clientIsValid == True:
            try:
                # Get data from client and store as a tuple.
                newCommand = (client, client.recv(4096))

                # Add to queue
                self.commandQueue.put(newCommand)

            except socket.error:
                print(Fore.RED + "Lost Client" + Fore.RESET)
                self.lostClients.append(client)
                clientIsValid = False

    # Thread that handles processing for each ai.

    def HandleAgentThread(self, agent):

        handleAgent = True

        while handleAgent is True:
            # Get possible options in the current room.
            self.aiInputManager.GetOptions(agent)

            # Make a choice and wait based on the choice made.
            time.sleep(self.aiInputManager.MakeChoice(agent))

            time.sleep(random.randint(1, 3))

    # Creates threads for each agent in the game so each one can process commands individually.
    def CreateAgentThreads(self):

        # For each agent in the dungeon, start a new thread.
        for agent in self.dungeon.agents:
            newAgentThread = threading.Thread(target=self.HandleAgentThread, args=(self.dungeon.agents[agent],))
            newAgentThread.start()











