import socket
import json
import time
from colorama import Fore, init

from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class JsonIO:
    seqID = 0
    packetID = "MudM"

    encryptionKey = ''

    init()

    @classmethod
    def Output(cls, serverSocket, output):

        keyAsBytes = cls.encryptionKey.encode('utf-8')
        keyAsBytes = b64decode(keyAsBytes)

        # Generate AES cipher with key.
        cipher = AES.new(keyAsBytes, AES.MODE_CBC)

        # Encrypt message as bytes using cipher.
        cipherTextRaw = cipher.encrypt(pad(output.encode('utf-8'), AES.block_size))

        # Get initialisation vector.
        iv = b64encode(cipher.iv).decode('utf-8')

        cipherText = b64encode(cipherTextRaw).decode('utf-8')

        # Send data to client
        try:
            dataDict = {"time": time.ctime(), "iv": iv, "message": cipherText, "value": cls.seqID}

            jsonPacket = json.dumps(dataDict)

            header = len(jsonPacket).to_bytes(2, byteorder='little')

            serverSocket.send(cls.packetID.encode())
            serverSocket.send(header)

            serverSocket.send(jsonPacket.encode())

            cls.seqID += 1

            return True

        except socket.error:
            print(Fore.RED + "Unable to send to client." + Fore.RESET)
            print("Attempted output: " + output)
            return False


