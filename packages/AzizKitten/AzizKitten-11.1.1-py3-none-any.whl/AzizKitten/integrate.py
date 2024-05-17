def integrate(integrand, a, b):
    if b == float('inf'):
        b = 999999999999999
    if b == float('-inf'):
        b = -999999999999999
    if a == float('inf'):
        a = 999999999999999
    if a == float('-inf'):
        a = -999999999999999
    segment_width = (b - a) / 60000
    result = 0.5 * (integrand(a) + integrand(b))
    for i in range(1,60000):
        x_i = a + i * segment_width
        result += integrand(x_i)
    result *= segment_width
    if result >= 1e10:
        return float('inf')
    elif result <= -1e10:
        return float('-inf')
    return result