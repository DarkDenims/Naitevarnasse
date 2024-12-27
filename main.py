import pycrptyodome
import base64
import random
import json
import os

# let's start with something simple

# generete a random key
def createKey():
    return int(random.randint(1,1000))


# pass createKey vaulue into rawdata.json
def passKey(file='rawdata.json'):
    with open('rawdata.json', 'r') as f:
        data = json.load(f)

    data['key'] = createKey()
    #sanity check
    print(data)
    with open('rawdata.json', 'w') as f:
        json.dump(data, f, indent=4)

passKey()

