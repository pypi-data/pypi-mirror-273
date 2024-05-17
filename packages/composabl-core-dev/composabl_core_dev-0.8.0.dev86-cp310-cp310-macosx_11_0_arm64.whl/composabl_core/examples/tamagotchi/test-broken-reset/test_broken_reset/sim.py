# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential


from typing import Any, Dict, List, Tuple, Union

import gymnasium as gym
from gymnasium.envs.registration import EnvSpec

from composabl_core.agent.scenario import Scenario
from composabl_core.networking.server_composabl import ServerComposabl


class TamagotchiSim(ServerComposabl):
    def __init__(self):
        self.render_mode = "ascii"
        self.health = 100
        self.happiness = 100
        self.hunger = 0
        self.energy = 100
        self.is_alive = True

        self.sensor_space = gym.spaces.Discrete(4)
        self.action_space = gym.spaces.Discrete(4)

    async def make(self, env_id: str, env_init: Dict[str, Any]) -> EnvSpec:
        return EnvSpec(env_id, self.sensor_space, self.action_space)

    async def sensor_space_info(self) -> gym.Space:
        return self.sensor_space

    async def action_space_info(self) -> gym.Space:
        return self.action_space

    async def action_space_sample(self) -> Union[Any, List[Any]]:
        return self.action_space.sample()

    async def reset(self) -> Tuple[Any, Dict[str, Any]]:
        self.health = 100
        self.happiness = 100
        self.hunger = 0
        self.energy = 100
        self.is_alive = True
        state = (self.health, self.happiness, self.hunger, self.energy)
        info = {}

        return state, info

    async def step(self, action) -> Tuple[Any, float, bool, bool, Dict[str, Any]]:
        if not self.is_alive:
            return (self.health, self.happiness, self.hunger, self.energy), 0.0, True, True, {}

        if action == 0:  # Feed
            self.hunger = max(0, self.hunger - 10)
            self.happiness = min(100, self.happiness + 5)
        elif action == 1:  # Play
            self.energy = max(0, self.energy - 10)
            self.happiness = min(100, self.happiness + 10)
        elif action == 2:  # Sleep
            self.energy = min(100, self.energy + 20)
            self.happiness = max(0, self.happiness - 5)
        elif action == 3:  # Heal
            self.health = min(100, self.health + 10)
            self.energy = max(0, self.energy - 10)

        # Update hunger over time
        self.hunger = min(100, self.hunger + 5)
        if self.hunger >= 100:
            self.health = max(0, self.health - 10)

        if self.health <= 0:
            self.is_alive = False

        state = (self.health, self.happiness, self.hunger, self.energy)
        reward = self.happiness / 100.0
        done = not self.is_alive
        info = {}

        return state, reward, done, done, info

    async def close(self) -> None:
        pass

    async def set_scenario(self, scenario) -> None:
        pass

    async def get_scenario(self) -> Any:
        return None

    async def set_render_mode(self, render_mode) -> None:
        pass

    async def get_render_mode(self) -> str:
        return self.render_mode

    async def get_render(self) -> Any:
        if self.render_mode == "ascii":
            return self.render_ascii()

        return None

    def render_ascii(self):
        health_bar = "Health: [" + "#" * (self.health // 10) + "-" * ((100 - self.health) // 10) + "]"
        happiness_bar = "Happiness: [" + "#" * (self.happiness // 10) + "-" * ((100 - self.happiness) // 10) + "]"
        hunger_bar = "Hunger: [" + "#" * (self.hunger // 10) + "-" * ((100 - self.hunger) // 10) + "]"
        energy_bar = "Energy: [" + "#" * (self.energy // 10) + "-" * ((100 - self.energy) // 10) + "]"
        tamagotchi = """
        ____
       /    \\
      | o  o |
      |  []  |
       \____/

        """
        return f"{tamagotchi}\n{health_bar}\n{happiness_bar}\n{hunger_bar}\n{energy_bar}"

