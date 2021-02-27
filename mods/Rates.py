ranks = ["Clay","Bronze","Silver","Iron","Gold"]

def convert(rank: str):
    pos = ranks.index(rank)
    return pos + 1

def getRank(rank: int):
    return ranks[rank-1]
    