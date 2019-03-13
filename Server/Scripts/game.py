# Main game class. Contains gameloop

from Scripts import player
from Scripts import dungeon
from Scripts import server
from Scripts import inputManager
from Scripts import aiInputManager
from Scripts import npcAgent

from colorama import Fore, init

import socket
import time
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

        self.dungeon = ''

        self.inputManager = ''
        self.aiInputManager = ''

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

        # Test Agent
        self.testAgent = npcAgent.NpcAgent("TestAI", 1, "A test npc.", '')

    def setup(self, dungeonName):
        self.gameIsRunning = True

        self.Connect()

        # Create a dungeon
        self.dungeon = dungeon.Dungeon(dungeonName)

        # Create inputManager
        self.inputManager = inputManager.InputManager(self.dungeon)
        self.aiInputManager = aiInputManager.AiInputManager(self.dungeon)

        # Setup rooms for the dungeon
        # self.dungeon.SetupDefaultRooms()
        self.dungeon.SetupCityRooms()

        self.testAgent.currentRoom = "GreatPlaza"#self.dungeon.startRoom
        self.dungeon.agents["TestAgent"] = self.testAgent
        self.SetupAgentThreads()


    def Connect(self):
        self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to bind to port
        try:
            # Use address specified in command line args
            if len(sys.argv) > 1:
                self.networkSocket.bind((sys.argv[1], 8222))

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

        # Pre-game intro text
        # intro = self.dungeon.description + self.player.inputManager.Look(self.player)

        #server.Output(self.client, intro)

        # Main server loop
        while self.gameIsRunning:
            self.lostClients = []

            #self.HandleAgents()

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
                    server.Output(currentCommand[0], serverOutput)

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

            # The player associated with the new client
            newPlayer = self.dungeon.players[new_client[0]]

            # Send player name to the client
            server.Output(new_client[0], "#name " + newPlayer.name + "\n")

            # Delay to prevent messages being appended to each other in the client receive queue. Could add delimiters.
            time.sleep(0.5)

            # For all other players in the game display who has joined the game..
            for playerClient in self.dungeon.players:
                if self.dungeon.players[playerClient] != newPlayer:
                    server.Output(playerClient, "<font color=magenta>" + newPlayer.name + " has joined the game! </font>")

            # Send roomName to the client. Not very nice being here.
            # Would be nice to do this at the beginning of the gameloop.
            # Added a space before #room to stop the # appending to the player name for some reason.
            server.Output(new_client[0], '#room ' + newPlayer.currentRoom)

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

    def HandleAgents(self):
        # self.aiInputManager.HandleInput(self.testAgent, "go north")

        self.aiInputManager.GetOptions(self.testAgent)
        self.aiInputManager.MakeChoice(self.testAgent)
        self.testAgent.ClearOptions()

        pass

    def SetupAgentThreads(self):
        # For each agent in the dungeon, start a new thread.
        for agent in self.dungeon.agents:
            newAgentThread = threading.Thread(target=self.HandleAgentThread, args=(self.dungeon.agents[agent],))
            newAgentThread.start()

    # Thread that handles processing for each ai.
    def HandleAgentThread(self, agent):

        handleAgent = True

        while handleAgent is True:
            self.aiInputManager.GetOptions(agent)

            self.aiInputManager.MakeChoice(agent)
            time.sleep(2.0)

            self.testAgent.ClearOptions()











