def ln(x):
    from .integrate import integrate
    from .constants import pi
    from .atan import atan
    from .sqrt import sqrt
    def integrand(t):
        return 1/t
    if type(x) is complex:
        r = sqrt((x.real)**2+(x.imag)**2)
        theta = atan(x.imag/x.real)
        return integrate(integrand, 1, r) + theta*1j
    else:
        if x < 0:
            return integrate(integrand, 1, -x) + pi*1j
        elif x == 0:
            return None
        return integrate(integrand, 1, x)