import socket
import json
import time
from colorama import Fore, init

class JsonIO:
    seqID = 0
    packetID = "MudM"

    init()

    @classmethod
    def Output(cls, serverSocket, output):
        # Send data to client
        try:
            dataDict = {"time": time.ctime(), "message": output, "value": cls.seqID}

            jsonPacket = json.dumps(dataDict)

            header = len(jsonPacket).to_bytes(2, byteorder='little')

            serverSocket.send(cls.packetID.encode())
            serverSocket.send(header)
            serverSocket.send(jsonPacket.encode())

            # print("Sent: " + str(dataDict["value"]))
            cls.seqID += 1

            return True

        except socket.error:
            print(Fore.RED + "Unable to send to client." + Fore.RESET)
            print("Attempted output: " + output)
            return False


