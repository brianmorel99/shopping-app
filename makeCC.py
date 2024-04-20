import hashlib

with open("cc.txt", "w") as ccFile:
    creditcards = [['0000000000000000', '12/25'],
                   ['1234567890123456', '78/90'],
                   ['1111111111111111', '11/11']
                   ]
    for cc in creditcards:
        ccComplete = cc[0] + cc[1]
        print(ccComplete)
        ccHash = hashlib.md5(ccComplete.encode()).hexdigest()
        print(ccHash)
        ccFile.write(ccHash + '\n')
