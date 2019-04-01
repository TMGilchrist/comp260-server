from Scripts import inputManager
import socket
import time
import threading
import sys
import json

from queue import *
from colorama import Fore, init


"""
Game class that holds important information for a game including the dungeon and the player. 
"""


class Game:

    def __init__(self, qtWindow=''):
        self.isConnected = False
        self.clientIsRunning = True

        self.networkSocket = ''
        self.currentReceiveThread = ''
        self.currentBackgroundThread = ''

        # Init colourama
        init()

        self.qtWindow = qtWindow
        self.inputManager = inputManager.InputManager()

        # Queue of messages from the server
        self.messageQueue = Queue()

    # Thread that handles receiving messages from the server and adding them to the message queue.
    def receiveThread(self, serverSocket):
        print(Fore.CYAN + "Receive thread running. \n" + Fore.RESET)

        # Receive packets
        while self.isConnected is True:
            try:
                # Get 4-character packet ID
                packetID = serverSocket.recv(4)

                print(Fore.YELLOW + "Packet Received." + Fore.RESET)
                print(Fore.YELLOW + "PacketID = " + Fore.RESET + packetID.decode("utf-8"))

                # Check if packet ID is correct.
                if packetID.decode("utf-8") == "MudM":
                    # Store size of payload
                    payloadSize = int.from_bytes(serverSocket.recv(2), 'little')

                    print(Fore.YELLOW + "Payload size: " + Fore.RESET + str(payloadSize))

                    # Grab payload data.
                    payloadData = serverSocket.recv(payloadSize)

                    # Convert data to dictionary.
                    data = json.loads(payloadData)

                    print(Fore.YELLOW + "Time Sent: " + Fore.RESET + data["time"])
                    print(Fore.YELLOW + "Packet sequence: " + Fore.RESET + str(data["value"]))
                    print(Fore.YELLOW + "Packet message: " + Fore.RESET + data["message"] + "\n")

                    # Add the message to to the messageQueue
                    self.messageQueue.put(data["message"])

            except socket.error:
                self.isConnected = False
                self.messageQueue.put("<font color=Red>Server lost.</font>")
                print(Fore.RED + "Server lost." + Fore.RESET)

    # Background thread that handles connection to the server.
    def BackgroundThread(self):
        print(Fore.CYAN + "Background thread running." + Fore.RESET)
        self.isConnected = False

        # When not connected, attempt to connect.
        while (self.isConnected is False) and (self.clientIsRunning is True):
            try:
                print(Fore.CYAN + "Background Thread: attempting to connect." + Fore.RESET)
                self.messageQueue.put("<font color=Cyan>Attempting to connect to server.</font>")

                # Find server socket
                self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to server socket
                try:
                    if len(sys.argv) > 1:
                        self.networkSocket.connect((sys.argv[1], 8222))

                    else:
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

