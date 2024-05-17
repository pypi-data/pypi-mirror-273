def floor(x):
    if type(x) is int:
        return int(x)
    if x >= 0:
        return int(x)
    else:
        return int(x)-1