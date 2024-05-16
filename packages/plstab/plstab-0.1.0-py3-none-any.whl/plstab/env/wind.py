import numpy as np
from enum import Enum, auto
from scipy.signal import lti

# constants
# ---- 
S_W = 1.5
S_U = 1.5

L_W = 533
L_U = 533
# ----


class Filter:
    """
    Create filtered noise
    """

    def __init__(self, tf, dt, update_period=30):
        """

        Args:
            tf: transfer function of noise filter
            dt: period of integrtation
            update_period: filter recompute gust each "update_period"

        """
        self.tf = tf
        self.counter = 0
        self.update_p = update_period
        self.dt=dt

    def sample(self, airspeed):

        """ Return noise passed through linear filter 

        Args:
            airspeed: current value of AirSpeed

        Returns:
            single current value of noise passed through linear filter
        """

        if self.counter % (self.update_p+1) == 0: # update each x step
            self.counter = 0
            self.fil = lti(*self.tf(airspeed))
            input = np.random.randn(self.update_p+1)
            time = np.linspace(0, self.dt*self.update_p, self.update_p+1)
            self.output = self.fil.output(input, time)[1][:]
            

        out = self.output[self.counter]
        self.counter += 1
        return out

class WindMode(Enum):
    """
    Available modes of wind
    """

    off = auto()
    no_gust = auto()
    simple = auto()
    dryden = auto

class Wind:
    """
    Create wind model;

    There are 4 modes of wind:
        1. off - no wind
        2. constant wind - do not add gust
        3. simple - gust is a white noise
        4. drygen - wind + gust(according to dryden turbulence model; p.s. look -> https://en.wikipedia.org/wiki/Dryden_Wind_Turbulence_Model)
    """

    def __init__(self, timestep=None, mode: int = 0, magnitude=15):
        """
        Args: 
            timestep: period of itegration
            mode: 1 of 4 wind models
        """
        
        wind_map = {  
            0: WindMode.off,
            1: WindMode.no_gust,
            2: WindMode.simple,
            3: WindMode.dryden
        }
        self.mode = wind_map[mode] # want or do not to simulate wind
        if self.mode != WindMode.off:
            magnitude = magnitude + np.random.randn() # get values of constant window speed which can be written as:
            angle = (180 - np.random.uniform(5, 10)) * np.pi / 180 # v_wind = V + N(mu_gust, sigma_gust)

            self.wx = 0.1 * np.random.randn() + magnitude * np.cos(angle)
            self.wy = 0.1 * np.random.randn() + magnitude * np.sin(angle)
        else:
            self.wx = 0.0
            self.wy = 0.0
        
        if self.mode == WindMode.dryden:

            H_u = lambda Va: [[S_U * np.sqrt(2 * Va / L_U)], [1, Va / L_U]] # u-axis noise transfer function
            H_w = lambda Va: [[Va / (np.sqrt(3) * L_W)], [Va / L_W, Va / L_W], S_W * np.sqrt(3 * Va / L_W)] # w-axis noise transfer function

            self.gx = Filter(H_u, dt=timestep, update_period=30)
            self.gy = Filter(H_w, dt=timestep, update_period=30)

    
    def __call__(self, airspeed=None, rot_mat=None):
        """ Make vector of wind for only timestep

        Args: 
            airspeed: for dryden's model tf 
            rot_mat: to transit gust vector to ground system of coordinates

        Returns:
            np-array with 2 components: x and y component of wind speed 
        """
        match self.mode:
            case WindMode.off: # without wind
                wx = self.wx
                wy = self.wy
            case WindMode.no_gust: # constant wind
                wx = self.wx
                wy = self.wy
            case WindMode.simple: # naive gust model
                gx, gy = self.simple_gust()
                wx = self.wx + gx
                wy = self.wy + gy
            case WindMode.dryden: # dryden turbulence 
                v_g = rot_mat @ np.array([[self.gx.sample(airspeed)], [self.gy.sample(airspeed)]])
                gx, gy = v_g.reshape((2, ))
                wx = self.wx + gx
                wy = self.wy + gy

        return np.array([wx, wy])
    
    def simple_gust(self, gust_noise=0.2):
        return gust_noise * np.random.randn(2)
    
if __name__ == '__main__':  # you can look wind graph
    
   
    import matplotlib.pyplot as plt 

    wx = []
    wy = []

    wind = Wind(timestep=0.05, mode=3)
    t = np.linspace(0, 2*40, 40 + 1)
    for i in range(40):

        x, y = wind(airspeed=25, rot_mat=np.eye(2))
        wx.append(x)
        wy.append(y)

        plt.arrow(t[i], 0, wx[i], wy[i], width=0.03)

    plt.ylim(0, 0.9)
    plt.grid()
    plt.show()


    plt.figure(figsize=(10, 6))
    plt.title('wind graphics')

    plt.subplot(1, 2, 1)
    plt.plot(wx)
    plt.xlabel('time')
    plt.ylabel('wind-y component')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(wy)
    plt.xlabel('time')
    plt.ylabel('wind-y component')
    plt.grid()
    plt.show()



