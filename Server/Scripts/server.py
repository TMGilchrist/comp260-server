import socket


def Output(client, output):
    # Send a test string
    try:
        client[0].send(output.encode())

    except socket.error:
        print("Client lost")

def ServerSetup():
    # Setup network socket
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.bind(("127.0.0.1", 8222))

    # Listen for a client
    mySocket.listen(5)
    client = mySocket.accept()

    # Receive some test data from the client
    data = client[0].recv(4096)
    print(data.decode("utf-8"))

    return client

def Reconnect():
    connected = False

    while not connected:
        ServerSetup()


