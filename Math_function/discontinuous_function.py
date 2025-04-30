# TODO make a plot
# TODO number 10 is not handled

def discontinuous(x: float) -> float:
    if x == -1:
        raise ValueError(f'Number {x} is out of range')
    elif -10 <= x <= -2:
        return -(x**2)
    elif -2 < x <= 9:
        return (1 - x) / (1 + x)
    elif 10 < x <= 35:
        return abs(x - 12)
