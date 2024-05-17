def cbrt(x):
    from .cos import cos
    from .sin import sin
    from .constants import pi
    from .sqrt import sqrt
    from .atan import atan
    if type(x) is complex:
        a = x.real
        b = x.imag
        if a != 0:
            r = sqrt(a**2+b**2)
            theta = atan(b/a)
            low = 0.0
            high = max(1.0, r)
            epsilon = 0.00000000000001
            while True:
                mid = (low + high)/2
                mid_cubed = mid * mid * mid

                if abs(mid_cubed-r) < epsilon:
                    cubed_r = mid
                    break
                elif mid_cubed < r:
                    low = mid
                else:
                    high = mid
            sqrt1 = cubed_r * (cos((-pi-theta)/3)-sin((-pi-theta)/3)*1j)
            sqrt2 = cubed_r * (cos((pi-theta)/3)-sin((pi-theta)/3)*1j)
            sqrt3 = -cubed_r * (cos((theta)/3)+sin((theta)/3)*1j)
            if sqrt1.real > sqrt2.real and sqrt1.real > sqrt3.real:
                return sqrt1
            elif sqrt2.real > sqrt1.real and sqrt2.real > sqrt3.real:
                return sqrt2
            return sqrt3 
            
        if b >= 0:
            low = 0.0
            high = max(1.0, b)
        else:
            low = min(-1.0, b)
            high = 0.0
        
        epsilon = 0.00000000000001
    
        while True:
            mid = (low + high) / 2
            mid_cubed = mid * mid * mid

            if abs(mid_cubed - b) < epsilon:
                cubed_b = mid
                break
            elif mid_cubed < b:
                low = mid
            else:
                high = mid
        return cubed_b*-1j
    if x >= 0:
        low = 0.0
        high = max(1.0, x)
    else:
        low = min(-1.0, x)
        high = 0.0
    
    epsilon = 1e-10
    
    while True:
        mid = (low + high) / 2
        mid_cubed = mid * mid * mid

        if abs(mid_cubed - x) < epsilon:
            return mid
        elif mid_cubed < x:
            low = mid
        else:
            high = mid