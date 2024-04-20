# echo-server.py

import socket
import sys

def loginUser(clientSocket):
    resp = "Please Enter Username:".encode("utf-8")
    clientSocket.send(resp)
    msg = clientSocket.recv(1024)
    username = msg.decode("utf-8")
    if username.lower() == "exit":
        clientSocket.close()
        return 0

    resp = "Please Enter Password:".encode("utf-8")
    clientSocket.send(resp)
    msg = clientSocket.recv(1024)
    password = msg.decode("utf-8")
    
    valid = checkAccess(username, password)
    if valid:
        newState = 2
    else:
        newState = 1
    
    return newState

def shoppingMenu(clientSocket):
    menu = []
    menu[0] = ['Item ID', 'Description', 'Price (EA)', '# on Order', 'Ext. Total']
    menu[1] = [1,'Hamburger', 4.99, 0, 0.00]
    

    return 2

def checkAccess(user, pw):
    return True

def main():
    HOST = "127.0.0.1"
    PORT = 10022
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Listening on {HOST}:{PORT}")
    
    conn, addr = server.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")
    
    response = f"Thank You for Connecting from {addr[0]}:{addr[1]}".encode("utf-8")
    conn.send(response)
    state = 1
        
    while True:
        match state:
            case 1:
                state = loginUser(conn)
            case 2:
                state = shoppingMenu(conn)
            case _:
                conn.close()
                sys.exit()

if __name__=="__main__": 
    main() 




