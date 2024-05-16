"""Registers the internal gym envs then loads the env plugins for module using the entry point."""
from typing import Any

from gymnasium.envs.registration import (
    load_plugin_envs,
    make,
    pprint_registry,
    register,
    registry,
    spec,
)


register(
    id='PlaneStab-v0',
    entry_point="plstab.env.plane_env:PlaneEnv",
    max_episode_steps=2000,
)

# import gymnasium as gym

# print(gym.pprint_registry())