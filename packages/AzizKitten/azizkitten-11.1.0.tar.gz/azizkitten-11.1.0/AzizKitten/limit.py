def limit(func, approaching, side=""):
    k = 1e16
    if approaching == float('inf'):
        approaching = 99999999999
    if approaching == float('-inf'):
        approaching = -99999999999
    if side == "":
        while True:
            try:
                result1 = func(approaching+1/k)
                result2 = func(approaching-1/k)
                break
            except:
                k = k // 10
        if result1 == result2:
            if result1 >= 1e10:
                return float('inf')
            elif result1 <= -1e10:
                return float('-inf')
            return result1
        else:
            raise NameError("Limit doesn't exist")
    elif side == "+":
        while True:
            try:
                result = func(approaching+1/k)
                break
            except:
                k = k // 10
        if result >= 1e10:
            return float("inf")
        elif result <= -1e10:
            return float("-inf")
        return result
    elif side == "-":
        while True:
            try:
                result = func(approaching-1/k)
                break
            except:
                k = k // 10
        if result >= 1e10:
            return float("inf")
        elif result <= -1e10:
            return float("-inf")
        return result
    else:
        raise ValueError("The input for 'side' must be a string type containing only '+' or '-' or nothing.")