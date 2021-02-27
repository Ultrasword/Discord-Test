import json
from os import path, getcwd

cwd = getcwd()

def isBad(attackelement, defendelement):
    with open(path.join(cwd, "server\\types.json"),"r") as types:
        data = json.load(types)
        types.close()
    #find if good or bad against
    d = data[str(defendelement)]
    if attackelement in d["bad"]:
        return True
    else:
        return False

def isGood(attackelement, defendelement):
    with open(path.join(cwd, "server\\types.json"),"r") as types:
        data = json.load(types)
        types.close()
    #find if good or bad against
    d = data[str(defendelement)]
    if attackelement in d["good"]:
        return True
    else:
        return False