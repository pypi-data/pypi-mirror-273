def factorial(x):
    from .exp import exp
    from .integrate import integrate
    if type(x) is not complex:
        if int(x) == x:
            if x < 0:
                raise ValueError("Factorial of a negative integer is undefined.")
            else:
                ans = 1
                for i in range(1,x+1):
                    ans *= i
                return ans
    else:
        def integrand(t):
            return t**x * exp(-t)
        return integrate(integrand, 0, 100)
