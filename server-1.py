from cryptography.fernet import Fernet
import hashlib
import re
import socket
import sys

def encResponse(response, fernet):
    return fernet.encrypt(response.encode("UTF-8"))
    
def decMessage(message, fernet):
    return fernet.decrypt(message).decode("UTF-8")

def loginUser(clientSocket,fernet):
    resp = "\nPlease Enter Username ('exit' to disconnect):"
    clientSocket.send(encResponse(resp, fernet)[:1500])
    msg = clientSocket.recv(1500)
    username = decMessage(msg,fernet)
    if username.lower() == "exit":
        return 0

    resp = "Please Enter Password:"
    clientSocket.send(encResponse(resp,fernet)[:1500])
    msg = clientSocket.recv(1500)
    password = decMessage(msg,fernet)
    pw = hashlib.md5(password.encode()).hexdigest()
    
    valid = checkAccess(username, pw)
    if valid:
        newState = 2
    else:
        newState = 1
    
    return newState

def drawMenu(items, item_total, order_total):
    header = ['Item ID', 'Description', 'Price (EA)', '# on Order', 'Ext. Total']

    menu = '_____________________________________________________________________________'
    
    menu += f'\n| {header[0]:<7} | {header[1]:<20} | {header[2]:>11} | {header[3]:>10} | {header[4]:>13} |'
    menu += '\n-----------------------------------------------------------------------------'

    for item in items:
        menu += f'\n| {item[0]:<7} | {item[1]:<20} | ${item[2]:>10} | {item[3]:>10} | ${item[4]:>12.2f} |'

    menu += f'\n| 10      | Proceed to Pay       |             |            |               |'
    menu += f'\n| 99      | Exit                 | Totals      | {item_total:>10} | ${order_total:>12.2f} |'
    menu += '\n-----------------------------------------------------------------------------'
    menu += '\n Selection:'

    return menu

def drawReceipt(items, item_total, order_total):
    header = ['Item ID', 'Description', 'Price (EA)', '# on Order', 'Ext. Total']

    receipt = '_____________________________________________________________________________'
    
    receipt += f'\n| {header[0]:<7} | {header[1]:<20} | {header[2]:>11} | {header[3]:>10} | {header[4]:>13} |'
    receipt += '\n-----------------------------------------------------------------------------'

    for item in items:
        if item[4] > 0:
            receipt += f'\n| {item[0]:<7} | {item[1]:<20} | ${item[2]:>10} | {item[3]:>10} | ${item[4]:>12.2f} |'

    receipt += f'\n|         |                      | Totals      | {item_total:>10} | ${order_total:>12.2f} |'
    receipt += '\n-----------------------------------------------------------------------------'

    return receipt

def checkMenuResponse(message):
    try:
        int(message)
        return True
    except ValueError:
        return  False

def invalidResponse(clientSocket, fernet):
    response = f'Invalid Response, please send any key to return to Menu: '
    resp = response.encode("utf-8")
    clientSocket.send(encResponse(response,fernet)[:1500])
    msg = clientSocket.recv(1500)

def shoppingMenu(clientSocket, items, fernet):
    item_total = 0
    order_total = 0.00

    for item in items:
        item_total += item[3]
        order_total += item[3] * item[2]

    while True:
        menu = drawMenu(items, item_total, order_total)
        clientSocket.send(encResponse(menu, fernet)[:1500])
        msg = clientSocket.recv(1500)
        message = decMessage(msg, fernet)
        if checkMenuResponse(message):
            msgID = int(message)
            if msgID == 99:
                return 99
            elif msgID == 10:
                return 3
            elif 0 < msgID < 7:
                response = f'How many {items[msgID - 1][1]} would you like to order? '
                resp = response.encode("utf-8")
                clientSocket.send(encResponse(response, fernet)[:1500])
                msg = clientSocket.recv(1500)
                message = decMessage(msg,fernet)
                if checkMenuResponse(message):
                    qty = int(message)
                    if qty + items[msgID -1][3] < 0:
                        item_total -= items[msgID -1][3]
                        order_total -= items[msgID -1][3] * items[msgID -1][2]
                        items[msgID -1][3] = 0
                        items[msgID -1][4] = 0
                    else:
                        items[msgID -1][3] += qty
                        items[msgID -1][4] += qty * items[msgID -1][2]
                        item_total += qty
                        order_total += qty * items[msgID -1][2]
                else:
                    invalidResponse(clientSocket, fernet)
                    return 2
            else:
                invalidResponse(clientSocket, fernet)
                return 2
        else:
            invalidResponse(clientSocket, fernet)
            return 2
    return 2

def checkAccess(user, pw):
    with open("Login.txt", "r") as loginfile:
        valid = (user + "," + pw + "\n") in loginfile.readlines()
    
    if valid:
        return True
    else:
        return False

def checkCC(cc, expire, order_total):
    CCHOST = '127.0.0.1'
    CCPORT = 11022
    
    ccClean = re.sub('[^0-9]+', '', cc)
    ccValid = re.search('^[0-9]{16}$', ccClean)

    expireClean = re.sub('[^0-9\/]+', '', expire)
    expireValid = re.search('^[0-9][0-9]\/[0-9][0-9]$', expireClean)

    if ccValid and expireValid:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        addr = (CCHOST, CCPORT)

        ccKey = open("skey.key", "rb").read()
        ccFernet = Fernet(ccKey)

        ccComplete = ccClean + expireClean
        response = hashlib.md5(ccComplete.encode()).hexdigest()
        client.sendto(encResponse(response,ccFernet)[:1500], addr)

        message, addr = client.recvfrom(1500)
        if decMessage(message,ccFernet).lower() == 'valid':
            client.sendto(encResponse(str(order_total),ccFernet)[:1500], addr)
            message, addr = client.recvfrom(1500)
            if decMessage(message,ccFernet).lower() == 'success':
                return True
            else:
                return False
        else:
            return False
    else: 
        return False

def checkout(clientSocket, items, fernet):
    item_total = 0
    order_total = 0.00

    for item in items:
        item_total += item[3]
        order_total += item[3] * item[2]
 
    receipt = drawReceipt(items, item_total, order_total)
    response = receipt + '\n Everything correct (Y/N):'
    clientSocket.send(encResponse(response, fernet)[:1500])
    msg = clientSocket.recv(1500)
    message = decMessage(msg, fernet)
    if message.lower() != 'y':
        return 2
    
    response = 'Please Enter Credit Card Number (0000 0000 0000 0000):'
    clientSocket.send(encResponse(response, fernet)[:1500])
    msg = clientSocket.recv(1500)
    cc = decMessage(msg, fernet)
    
    response = 'Please Enter Expiration Date (MM/YY):'
    clientSocket.send(encResponse(response, fernet)[:1500])
    msg = clientSocket.recv(1500)
    expire = decMessage(msg, fernet)
    
    if checkCC(cc, expire, order_total) == False:
        invalidResponse(clientSocket, fernet)
        return 2
    
    response = receipt + '\n Thanks for your Order! - Type "99" to exit'
    clientSocket.send(encResponse(response, fernet)[:1500])
    return 99

def main():
    HOST = "127.0.0.1"
    PORT = 10022

    key = open("key.key", "rb").read()
    fernet = Fernet(key)

    items = [[1,'Hamburger', 4.99, 0, 0.00],
            [2,'Cheeseburger', 5.99, 0, 0.00],
            [3,'Hot Dog', 3.99, 0, 0.00],
            [4,'French Fries', 2.99, 0, 0.00],
            [5,'Pop / Soda', 1.99, 0, 0.00],
            [6,'Bottled Water', 1.99, 0, 0.00]]
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Listening on {HOST}:{PORT}")
    
    conn, addr = server.accept()
    print(f"Accepted connection from {addr[0]}:{addr[1]}")
    
    state = 1
        
    while True:
        match state:
            case 1:
                state = loginUser(conn,fernet)
            case 2:
                state = shoppingMenu(conn,items,fernet)
            case 3:
                state = checkout(conn,items,fernet)
            case _:
                conn.close()
                sys.exit()

if __name__=="__main__": 
    main() 




