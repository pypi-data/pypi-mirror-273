class DriveUnit:
    """ This class made to sim saome dynamics of drive unit,
    for non-instant resonse
    """
    def __init__(self, dt):
        self.a = 0.0
        self.k = 9
        self.dt = dt

    def __call__(self, s):
        """ Determine dynamics of drive unit

        a' = k * (target - a)
        """
        self.a += self.k * (s - self.a) * self.dt
        return self.a

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import numpy as np

    dt = 0.05
    t = np.linspace(0, 20, 201)
    s = np.ones_like(t)

    du = DriveUnit(dt=dt)

    resp = []

    for x in s:
        resp.append(du(x))

    plt.plot(t, s, label='target')
    plt.scatter(t, np.array(resp), label='response of drive_unit', marker='.', color='orange')

    plt.legend()
    plt.show()
