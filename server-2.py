from cryptography.fernet import Fernet
import hashlib
import re
import socket

def encResponse(response, fernet):
    return fernet.encrypt(response.encode("UTF-8"))
    
def decMessage(message, fernet):
    return fernet.decrypt(message).decode("UTF-8")

def main():
    HOST = "127.0.0.1"
    PORT = 11022

    key = open("skey.key", "rb").read()
    fernet = Fernet(key)

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    print(f"Listening on {HOST}:{PORT}")
    
    while True:
        msg, addr = server.recvfrom(1500)
        ccComplete = decMessage(msg,fernet)

        with open("cc.txt", "r") as ccFile:
            valid = (ccComplete + "\n") in ccFile.readlines()
    
        if valid:
            resp = "Valid"
            server.sendto(encResponse(resp, fernet)[:1500], addr)
            msg, addr = server.recvfrom(1500)
            total = decMessage(msg,fernet)
            resp = "Success"
            server.sendto(encResponse(resp, fernet)[:1500],addr)
            
        else:
            resp = "Invalid"
            server.sendto(encResponse(resp, fernet)[:1500], addr)

if __name__=="__main__": 
    main() 




