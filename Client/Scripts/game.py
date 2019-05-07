from Scripts import inputManager, jsonIO
import socket
import time
import threading
import sys
import json

from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from queue import *
from colorama import Fore, init


class Game:

    def __init__(self, qtWindow=''):
        self.isConnected = False
        self.clientIsRunning = True

        self.userLocalHost = True
        self.serverIP = "46.101.56.200"
        self.serverPort = 9100

        self.networkSocket = ''
        self.currentReceiveThread = ''
        self.currentBackgroundThread = ''

        # If this user is logged in to the game.
        self.loggedIn = False

        # Init colourama
        init()

        self.qtWindow = qtWindow
        self.inputManager = inputManager.InputManager()

        # Queue of messages from the server
        self.messageQueue = Queue()

        # Queue of messages for the login screen only
        self.loginMessageQueue = Queue()

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
                    data = json.loads(payloadData) #.decode("utf-8"))

                    # Decrypt data
                    iv = b64decode(data["iv"])

                    cipherText = b64decode(data["message"])

                    # Convert key to bytes for use.
                    keyAsBytes = jsonIO.JsonIO.encryptionKey.encode('utf-8')
                    keyAsBytes = b64decode(keyAsBytes)

                    cipher = AES.new(keyAsBytes, AES.MODE_CBC, iv)

                    decryptedMessage = unpad(cipher.decrypt(cipherText), AES.block_size)
                    decryptedMessage = decryptedMessage.decode('utf-8')

                    print(Fore.YELLOW + "Time Sent: " + Fore.RESET + data["time"])
                    print(Fore.YELLOW + "Packet sequence: " + Fore.RESET + str(data["value"]))
                    print(Fore.YELLOW + "Packet message: " + Fore.RESET + decryptedMessage + "\n")

                    # Add login screen commands to the loginMessageQueue
                    if decryptedMessage[:2] == "##":
                        self.loginMessageQueue.put(decryptedMessage)

                    else:
                        # Add the message to to the messageQueue
                        self.messageQueue.put(decryptedMessage)

                elif packetID.decode("utf-8") == "Init":
                    # Store size of payload
                    payloadSize = int.from_bytes(serverSocket.recv(2), 'little')

                    print(Fore.YELLOW + "Payload size: " + Fore.RESET + str(payloadSize))

                    # Grab payload data.
                    payloadData = serverSocket.recv(payloadSize)

                    # Convert data to dictionary.
                    data = json.loads(payloadData.decode("utf-8"))
                    key = data["key"]

                    # Store key.
                    jsonIO.JsonIO.encryptionKey = key

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
                print(Fore.CYAN + "Background Thread: attempting to connect..." + Fore.RESET)
                self.messageQueue.put("<font color=Cyan>Attempting to connect to server...</font>")

                # Find server socket
                self.networkSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to server socket
                try:
                    if len(sys.argv) > 1:
                        self.networkSocket.connect((sys.argv[1], 8222))

                    elif self.userLocalHost is True:
                        self.networkSocket.connect(("127.0.0.1", 8222))

                    elif self.serverIP != '' and self.serverPort != '':
                        print("Using serverIP!")
                        self.networkSocket.connect((self.serverIP, self.serverPort))

                    else:
                        self.networkSocket.connect(("127.0.0.1", 8222))

                    self.isConnected = True
                    print(Fore.CYAN + "Background Thread: Connected to server." + Fore.RESET)
                    self.messageQueue.put("<font color=Cyan>Connected to server!</font>")

                except socket.error:
                    time.sleep(2.0)
                    print(Fore.RED + "Background Thread: Failed to connect to the server..." + Fore.RESET)
                    self.messageQueue.put("<font color=Red>Failed to connect to the server...</font>")
                    time.sleep(1.0)

                # Start the receive thread
                self.currentReceiveThread = threading.Thread(target=self.receiveThread, args=(self.networkSocket,))
                self.currentReceiveThread.start()

                # Sleep after connecting to keep the thread running.
                while self.isConnected is True:
                    time.sleep(1.0)

            except socket.error:
                print(Fore.RED + "No server connection found." + Fore.RESET)
                time.sleep(2.0)

