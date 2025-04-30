import matplotlib.pyplot as plt
import numpy as np


def discontinuous(x: float) -> float:
    if x == -1:
        raise ValueError(f'Number {x} is out of range')
    elif -10 <= x <= -2:
        return -(x**2)
    elif -2 < x <= 9:
        return (1 - x) / (1 + x)
    elif 10 < x <= 35:
        return abs(x - 12)
    else:
        raise ValueError(f'Number {x} is out of range')

def main():
    x_vals = np.linspace(-20, 45, 400)
    y_vals = []

    for x in x_vals:
        try:
            y = discontinuous(x)
            y_vals.append(y)
        except ValueError:
            y_vals.append(np.nan)

    plt.plot(x_vals, y_vals, label="Discontinuous Function")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Plot of The Function")
    plt.grid(True)
    plt.legend()
    plt.savefig("plot.png")


if __name__ == '__main__':
    main()
