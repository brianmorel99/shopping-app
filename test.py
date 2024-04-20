import re

test = ['12/24',
        '01/ab',
        'a0/1v',
        '1224']

for t in test:
    t2 = re.sub('[^0-9\/]+', '', t)
    print(t2)
    t3 = re.search('^[0-9][0-9]\/[0-9][0-9]$', t2)
    if t3:
        print(t3)


