import socket
import json
import time
from colorama import Fore, init

from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from Crypto.Random import get_random_bytes


class Server:

    seqID = 0
    standardPacketID = "MudM"
    setupPacketID = "Init"

    init()

    # Encryption key. This should be moved to main so it can be used to decrypt incoming messages!
    encryptionKey = ''

    @staticmethod
    def Output(client, output):
        # Send a string to the client.
        try:
            client.send(output.encode())
            return True

        except socket.error:
            print("Client lost")
            return False

    @classmethod
    def OutputJson(cls, client, output, packetID=standardPacketID):
        # Send data to client

        # Generate AES cipher with key.
        cipher = AES.new(cls.encryptionKey, AES.MODE_CBC)

        # Encrypt message as bytes using cipher.
        cipherTextRaw = cipher.encrypt(pad(output.encode('utf-8'), AES.block_size))

        # Get initialisation vector.
        iv = b64encode(cipher.iv).decode('utf-8')
        cipherText = b64encode(cipherTextRaw).decode('utf-8')

        try:
            dataDict = {"time": time.ctime(), "iv": iv, "message": cipherText, "value": cls.seqID}

            jsonPacket = json.dumps(dataDict)

            header = len(jsonPacket).to_bytes(2, byteorder='little')

            client.send(packetID.encode())
            client.send(header)
            client.send(jsonPacket.encode())

            cls.seqID += 1

            return True

        except socket.error:
            print(Fore.RED + "Unable to send to client." + Fore.RESET)
            print("Attempted output: " + output)
            return False

    @classmethod
    def SetupMessage(cls, client):
        key = b64encode(cls.encryptionKey).decode('utf-8')

        try:
            dataDict = {"time": time.ctime(), "key": key, "value": cls.seqID}

            jsonPacket = json.dumps(dataDict)

            header = len(jsonPacket).to_bytes(2, byteorder='little')

            client.send(cls.setupPacketID.encode())
            client.send(header)
            client.send(jsonPacket.encode())

            cls.seqID += 1

            return True

        except socket.error:
            print(Fore.RED + "Unable to send setup info to client." + Fore.RESET)
            return False

    def ReceiveJson(cls, client, verbose=False):
        pass


    """
    @classmethod
    def OutputJson(cls, client, output):
        # Send data to client
        try:
            dataDict = {"time": time.ctime(), "message": output, "value": cls.seqID}

            jsonPacket = json.dumps(dataDict)

            header = len(jsonPacket).to_bytes(2, byteorder='little')

            client.send(cls.packetID.encode())
            client.send(header)
            client.send(jsonPacket.encode())

            # print("Sent: " + str(dataDict["value"]))
            cls.seqID += 1

            return True

        except socket.error:
            print(Fore.RED + "Unable to send to client." + Fore.RESET)
            print("Attempted output: " + output)
            return False
        """

