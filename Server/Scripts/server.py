import socket


def Output(client, output):
    # Send a test string
    try:
        client[0].send(output.encode())

    except socket.error:
        print("Client lost")




