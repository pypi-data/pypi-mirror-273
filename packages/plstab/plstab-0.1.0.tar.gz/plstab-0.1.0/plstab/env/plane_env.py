import gymnasium as gym
from gymnasium import spaces
import numpy as np
import time
from .dynamics import *
from .visplane2 import *


class PlaneEnv(gym.Env):
    """
    ## Description
    This is a simple 2d airplane sim.

    There are 4 modes of wind:
        1. off - no wind
        2. constant wind - do not add gust
        3. simple - gust is a white noise
        4. drygen - wind + gust(according to dryden turbulence model; p.s. look -> https://en.wikipedia.org/wiki/Dryden_Wind_Turbulence_Model)

    To solve the normal version, you need to get 300 points in 1600 time steps.
    To solve the hardcore version, you need 300 points in 2000 time steps.


    ## Action Space
    Actions are: 
    - rate of propeler [-1, 1] -> [0, max]
    - angle of elevator [-1, 1] -> [-15, 15] (degrees)

    ## Observation Space
    State consists of 
    X - x-component of pos
    Vx - x-component of velocity
    Y - y-component of pos
    Vy - y-component of velocity
    Phi - pitch angle of airplane
    Omega - derivative of Phi
    Wx - x-component of wind speed
    Wy - y-component of wind speed

    ## Rewards
    By defalt R = -(Phi ** 2 + 0.1 * Omega ** 2 + 0.01 * alpha ** 2)

    ## Starting State
    start with zero state vector, except Vx(inital value id 50.0)

    ## Episode Termination
    The episode will terminate if the time runs out(more than 2000 timesteps) or 
    pitch will be more than allowed

    ## Arguments
    you can set
    
    - wind_mode = 0 (or 1, or 2, or 3)
    - wind_mag = 4.32 (or another value from [0, inf])
    - reward_fn = lambda X, Vx, Y, Vy, Phi, Omega, rate, alpha: ... come up with smth
    
    ```python
    import gymnasium as gym
    import plane
    env = gym.make("PlaneStab-v0", wind_mode=0, wind_mag=4)
    ```

    ## Credits
    Created by Maly

    """
    metadata = {'render_modes':['human'], 'render_fps': 10}

    def __init__(self, render_mode=None, wind_mode=0, wind_mag=4,
                 reward_fn=lambda X, Vx, Y, Vy, Phi, Omega, rate, alpha: -(Phi ** 2 + 0.1 * Omega ** 2 + 0.01 * alpha ** 2)):

        self.observation_space = spaces.Box(np.array([float('-inf')]*8), np.array([float('inf')]*8), shape=(8,), dtype=float)
        self.action_space = spaces.Box(np.array([-1, -1]), np.array([1, 1]))
        self.plane = PlaneModel(turbulence=wind_mode, wind_mag=wind_mag)
        self.reward_fn = reward_fn
        self.render_mode = render_mode
        self.pv = None


    
    def mix(self, action):
        return np.array([0.5, 15 * np.pi / 180]) * (action + np.array([1.0, 0.0]))
    
    def _get_obs(self):
        return self._agent_state
    
    def  reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if not(self.pv is None):
            self.close()
        if self.render_mode == "human":
            self.pv = PlaneVisualizer()

        self.episode_reward = []

        s = self.plane.reset()

        self._agent_state = s
        self.prev_state = s
        self.steps = 0

        observation = self._get_obs()
        info = self._get_info()


        return observation, info

    def step(self, action):

        # make mixer_func
        action = self.mix(action)
        self.s = self.plane.step(action) # new state

        X, Vx, Y, Vy, Phi, Omega, _, _ = self.s
        rate, alpha = action

        # reward = -(Phi ** 2 + 0.1 * Omega ** 2 + 0.001 * alpha ** 2 + (Phi - prev_Phi) ** 2 + (Omega - prev_Omega) ** 2)
        reward = self.reward_fn(X, Vx, Y, Vy, Phi, Omega, rate, alpha)

        self.episode_reward.append(reward)

        terminated = bool(self.steps > 2000) 
        truncated = bool(self.steps > 2000 or abs(self.plane.s[4]) > np.pi / 12)

        info = self._get_info()

        self.steps += 1
        self.prev_state = self.s[:]
        


        return self.s[:], reward, terminated, truncated, info

    def _get_info(self):
        return {}
    
    def close(self):
        if self.render_mode == 'human':
            self.pv.close()

    def render(self):
        X, Vx, Y, Vy, Phi, Omega, _, _ = self.s

        if self.render_mode == 'human':
            self.pv.step(0, 0, Vx, Vy, rphi=int(Phi * 180 / np.pi))
            time.sleep(0.05)

plane_env = lambda: PlaneEnv()

if __name__ == "__main__":
    env_id = "PlaneStab-v0"
    gym.register(env_id, entry_point=plane_env)