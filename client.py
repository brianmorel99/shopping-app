# echo-client.py

from cryptography.fernet import Fernet
import socket

def encResponse(response, fernet):
    return fernet.encrypt(response.encode("UTF-8"))
    
def decMessage(message, fernet):
    msg = fernet.decrypt(message)
    return msg.decode("UTF-8")

def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 10022  # The port used by the server

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, PORT))

    key = open("key.key", "rb").read()
    fernet = Fernet(key)


    while True:
        message = client.recv(1500)
        print(decMessage(message,fernet))

        response = input(": ")
        if response == "":
            response = ' '
        client.send(encResponse(response,fernet)[:1500])

        if response == "99" or response == "exit":
            client.close()
            break

if __name__=="__main__": 
    main() 
