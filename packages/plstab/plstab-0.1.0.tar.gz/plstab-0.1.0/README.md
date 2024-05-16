# Plstab = plane-stabilization envirnoment

This is a simple env. based on __OpenAI Gym__ library.
Envirnoment for training reinforcement learning (RL) agents.


#### Example of code to launch enviroment


``` python
import plstab
import numpy as np
import gymnasium as gym

env = gym.make('PlaneStab-v0', render_mode='human', wind_mode=3) # create env
obs, info = env.reset(seed=42)

for _ in range(100):
   action = np.zeros(2) # sample action
   obs, reward, terminated, truncated, info = env.step(action) # step env


   if terminated or truncated: # reset if episode ends
      obs, info = env.reset()
     
   env.render()

env.close()
```


args:

|     name or arg  |available value| default value|
|-------|------------| ---|
| render_mode   | "human", None                       | None|
| wind_mode | $ {0, 1, 2, 3} $  | 0|
| wind_mag | $x \in [0, \infty ]$                     | 4.0|
| reward_fn | lambda X, Vx, Y, Vy, Phi, Omega: ...                 | None|

wind mode provides to 1 of 4 wind models:

- 0: off (zero windspeed)
- 1: no_gust (wind without randonmness)  
- 2: simple (simple gust model)
- 3: dryden (dryden's turbulence model)

#### Observation space:

8-dim numpy vector which contains: 
[X, Vx, Y, Vy, Phi, Omega, Wx, Wy], where

- X - x-component of pos
- Vx - x-component of velocity
- Y - y-component of pos
- Vy - y-component of velocity
- Phi - pitch angle of airplane
- Omega - derivative of Phi
- Wx - x-component of wind speed
- Wy - y-component of wind speed


#### Action space:

Actions are: 
- rate of propeler [-1, 1] -> [0, max]
- angle of elevator [-1, 1] -> [-15, 15] (degrees)

#### Rewards:

By defalt: 

-(Phi ** 2 + 0.1 * Omega ** 2 + 0.01 * alpha ** 2)
