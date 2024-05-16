import numpy as np
import matplotlib.pyplot as plt


"""Description

Here are 2 functions which help to simulate aerodynamics
Cx(a) - drag coeficent, which is function of attack angle
Cy(a) - lift coeficent, which is function of attack angle

"""
def Cy(x: float):
    Cy_table = np.array([-0.874, -0.770, -0.653, -0.530, -0.402, -0.276, -0.150, -0.023, 0.1, 0.221, 0.344, \
        0.464, 0.584, 0.7, 0.81, 0.9, 0.952, 0.965])

    alpha_table = np.linspace(-18, 16, 18) * np.pi / 180
    idx = np.searchsorted(alpha_table, x)

    try:
        x0 = alpha_table[idx - 1]
        x1 = alpha_table[idx]

        y0 = Cy_table[idx - 1]
        y1 = Cy_table[idx]

    except:
        idx = 17
        x0 = alpha_table[idx - 1]
        x1 = alpha_table[idx]

        y0 = Cy_table[idx - 1]
        y1 = Cy_table[idx]

    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)

def Cx(x: float) ->float:
    Cx_table = np.array([0.0821, 0.0592, 0.0445, 0.0318, 0.0220, 0.0155, 0.0113, 0.0086, 0.0082, 0.0103, 0.0154, \
        0.0203, 0.0332, 0.0460, 0.0615, 0.0758, 0.097, 0.119])

    alpha_table = np.linspace(-18, 16, 18) * np.pi / 180
    idx = np.searchsorted(alpha_table, x)

    try:
        x0 = alpha_table[idx - 1]
        x1 = alpha_table[idx]

        y0 = Cx_table[idx - 1]
        y1 = Cx_table[idx]

    except:
        idx = 17
        x0 = alpha_table[idx - 1]
        x1 = alpha_table[idx]

        y0 = Cx_table[idx - 1]
        y1 = Cx_table[idx]

    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)



if __name__ == '__main__':
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

    ax1.set_title('Cx(a)')
    ax1.set(xlabel='a', ylabel='Cx')
    x = np.linspace(-18, 16, 30) * np.pi / 180
    ax1.plot(x, Cx(x), marker='_')
    ax1.grid()

    ax2.set_title('Cy(a)')
    ax2.set(xlabel='a', ylabel='Cy')
    x = np.linspace(-18, 16, 30) * np.pi / 180
    ax2.plot(x, Cy(x), marker='_')
    ax2.grid()

    plt.show()