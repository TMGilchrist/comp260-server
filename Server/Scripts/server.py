import socket


def Output(client, output):
    # Send a string to the client.
    try:
        client.send(output.encode())
        return True

    except socket.error:
        print("Client lost")
        return False
