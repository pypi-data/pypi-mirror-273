def sqrt(x):
    if type(x) is not complex:
        if x <= 0:
            return (-x)**.5*1j
    return x**.5