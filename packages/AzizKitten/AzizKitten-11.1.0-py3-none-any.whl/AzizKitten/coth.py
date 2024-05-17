def coth(x):
    from .sinh import sinh
    from .cosh import cosh
    return cosh(x)/sinh(x)