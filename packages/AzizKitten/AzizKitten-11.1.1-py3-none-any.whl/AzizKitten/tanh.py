def tanh(x):
    from .sinh import sinh
    from .cosh import cosh
    return sinh(x)/cosh(x)