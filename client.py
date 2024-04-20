# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 10022  # The port used by the server

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

while True:
    message = client.recv(1024)
    print(message.decode("utf-8"))

    response = input(": ")
    if response == "":
        response = ' '
    client.send(response.encode("utf-8")[:1024])

    if response == "99":
        client.close()
        break
