import socket
import json
import time


class Server:

    seqID = 0
    packetID = "MudM"

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
    def OutputJson(cls, client, output):
        # Send data to client
        try:
            dataDict = {"time": time.ctime(), "message": output, "value": cls.seqID}

            jsonPacket = json.dumps(dataDict)

            header = len(jsonPacket).to_bytes(2, byteorder='little')

            client.send(cls.packetID.encode())
            client.send(header)
            client.send(jsonPacket.encode())

            print("Sent: " + str(dataDict["value"]))
            cls.seqID += 1

            return True

        except socket.error:
            print("Client lost")
            return False


