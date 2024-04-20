import hashlib


users = [['brian', 'morel'],
         ['bmorel', 'mypass'],
         ['teacher', 'easy']]

with open("Login.txt", "w") as loginfile:
    for user in users:
        username = user[0]
        pw = hashlib.md5(user[1].encode()).hexdigest()
        loginfile.write(username + "," + pw + "\n")
    
    

