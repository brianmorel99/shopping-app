# echo-server.py

import socket
import sys

def loginUser(clientSocket):
    resp = "\nPlease Enter Username:".encode("utf-8")
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

def drawMenu(items, item_total, order_total):
    header = ['Item ID', 'Description', 'Price (EA)', '# on Order', 'Ext. Total']

    menu = f'\n| {header[0]:<7} | {header[1]:<20} | {header[2]:>10} | {header[3]:>10} | {header[4]:>12} |'

    for item in items:
        menu += f'\n| {item[0]:<7} | {item[1]:<20} | {item[2]:>10} | {item[3]:>10} | {item[4]:>12} |'

    menu += f'\n| (10) Proceed to Pay | (99) Exit | Total Items {item_total} | Order Total ${order_total} |'
    menu += '\n Selection:'

    return menu

def checkMenuResponse(message):
    if message.isdigit():
        return True
    else:
        return False

def invalidResponse(clientSocket):
    response = f'Invalid Response, please send any key to return to Menu: '
    resp = response.encode("utf-8")
    clientSocket.send(resp)
    msg = clientSocket.recv(1024)

def shoppingMenu(clientSocket):
    items = []
    item_total = 0
    order_total = 0.00

    items = [[1,'Hamburger', 4.99, 0, 0.00],
            [2,'Cheeseburger', 5.99, 0, 0.00],
            [3,'Hot Dog', 3.99, 0, 0.00],
            [4,'French Fries', 2.99, 0, 0.00],
            [5,'Pop / Soda', 1.99, 0, 0.00],
            [6,'Bottled Water', 1.99, 0, 0.00]]

    while True:
        menu = drawMenu(items, item_total, order_total)
        resp = menu.encode("utf-8")
        clientSocket.send(resp)
        msg = clientSocket.recv(1024)
        message = msg.decode("utf-8")
        if checkMenuResponse(message):
            msgID = int(message)
            if msgID == 99:
                return 99
            elif msgID == 10:
                return 10
            elif 0 < msgID < 7:
                response = f'How many {items[msgID - 1][1]} would you like to order? '
                resp = response.encode("utf-8")
                clientSocket.send(resp)
                msg = clientSocket.recv(1024)
                message = msg.decode("utf-8")
                if checkMenuResponse(message):
                    items[msgID -1][3] += int(message)
                    items[msgID -1][4] += int(message) * items[msgID -1][2]
                    item_total += int(message)
                    order_total += int(message) * items[msgID -1][2]
                else:
                    invalidResponse(clientSocket)
                    return 2
            else:
                invalidResponse(clientSocket)
                return 2
        else:
            invalidResponse(clientSocket)
            return 2
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




