import numpy as np
from .aerodynamics import Cx, Cy
from .wind import Wind, WindMode
from .drive_unit import DriveUnit

#parameters
# ------
m = 2961.383272
J = 98712.77573#60865.35
g = 9.81
a = 10
wing_d = 2
tail_d = 10


S0 = 43.55 + 27.96 
S1 = S0 * wing_d / tail_d

thrust_max = 5e4
density = 1.2255
# ------

#inital conditions
# ------
X0 = 0
Y0 = 0
Phi0 = 0
Vx0 = 50
Vy0 = 0
Omega0 = 0
Wx = 0
Wy = 0

s = np.array([X0, Vx0, Y0, Vy0, Phi0, Omega0, Wx, Wy])
# ------


class PlaneModel:
    """
    This module contains equations of movement
    """
    def __init__(self, turbulence=WindMode.off, wind_mag=4, dt=0.05):
        """
        Args:
            turbilence: 1 of 4 wind models
            wind_mag: expected valu of wind magnitude
            dt: step of integration(to avoid divergence don't make it larger)
            s: initial state

        """
        
        self.s = s[:]
        self.wind = Wind(timestep=dt, mode=turbulence, magnitude=wind_mag) # set mode of wind
        self.du = DriveUnit(dt=dt)
        self.dt = dt
        self.Va = np.sqrt(Vx0**2 + Vy0**2)
        self.time=0
        
    def integrate(self, u): # compute new-step-state
        """ Make one integration step

        Args: 
            u: vector of control input vector

        Returns:
        """
        k1 = self.acc(self.s, u) # rk-4
        k2 = self.acc(self.s + self.dt * k1/2, u)
        k3 = self.acc(self.s + self.dt * k2/2, u)
        k4 = self.acc(self.s + self.dt * k3, u)
        self.s = self.s + self.dt * (k1 + 2*k2 + 2*k3 + k4) / 6


    def acc(self, state, action): # compute right hand equation
        """ Compute forces and torques

        Args: 
            state: airplane state vector
            action: vector of control input vector

        Returns:
            derivative of state vector
        """
        #state and actions vectors
        X, Vx, Y, Vy, phi, Omega, _, _ = state
        rate, alpha = action
        alpha = self.du(alpha)
        rot_matrix = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])

        Wx, Wy = self.wind(airspeed=self.Va, rot_mat=rot_matrix) # get wind speed

        Va_x = Vx - Wx # compute airspeed
        Va_y = Vy - Wy

        self.Va = np.sqrt(Va_x**2 + Va_y**2)

        #forces & torques
        attack = phi - np.arctan2(Va_y, Va_x)

        rot_matrix_v = np.array([[np.cos(attack), -np.sin(attack)], [np.sin(attack), np.cos(attack)]]) # velocity frame -> body frame

        Drag = rot_matrix_v @ np.array([[S0 * Cx(attack) * density * (Va_x ** 2 + Va_y ** 2) / 2], [0.0]])
        Lift = rot_matrix_v @ np.array([[0.0], [S0 * Cy(attack) * density * (Va_x ** 2 + Va_y ** 2) / 2]])
        Thrust = np.array([[thrust_max * rate], [0.0]])
     
        fw_x = -Cx(attack + alpha) * density * (Va_x ** 2 + Va_y ** 2) / 2 * S1 # ?
        fw_y = Cy(attack + alpha) * density * (Va_x ** 2 + Va_y ** 2) / 2 * S1
        Mech = np.array([[fw_x * np.sin(alpha)], [fw_y * np.cos(alpha)]])
        mg = np.array([[0.0], [g]])
        self.alpha = attack + alpha

        wx, wy = rot_matrix @ (Lift - Drag + Thrust + Mech) / m - mg
        eps = (Lift[1][0] * wing_d  - Mech[1][0] * tail_d) / J

        return np.array([Vx, *wx, Vy, *wy, Omega, eps, Wx, Wy])


    def reset(self):
        self.s = s + 0.01 * np.random.randn(8)
        return  self.s[:]
    
    
    def step(self, action):
        """Makes one timestep, for externa usage

        Args: 
            action: vector of control input vector

        Returns:
            Copy of airplane state vector
        """
        self.integrate(u=action)
        self.time += 1
        return self.s[:]


if __name__ == '__main__':
    plane = PlaneModel(turbulence=3)
    for _ in range(500):
        plane.step(np.array([0, 0]))