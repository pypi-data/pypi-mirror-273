# Copyright (C) Composabl, Inc - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential

from typing import Any, Dict, SupportsFloat, Tuple

import gymnasium as gym
from gymnasium.envs.registration import EnvSpec

import composabl_core.utils.logger as logger_util
from composabl_core.agent.scenario import Scenario
from composabl_core.networking.server_composabl import ServerComposabl
from test_broken_reset.sim import TamagotchiSim

logger = logger_util.get_logger(__name__)


class SimImpl(ServerComposabl):
    def __init__(self):
        self.sim = TamagotchiSim()

    async def make(self, env_id: str, env_init: dict) -> EnvSpec:
        spec = {"id": "starship", "max_episode_steps": 400}
        return spec

    async def sensor_space_info(self) -> gym.Space:
        return self.sim.sensor_space

    async def action_space_info(self) -> gym.Space:
        return self.sim.action_space

    async def action_space_sample(self) -> Any:
        return self.sim.action_space.sample()

    async def reset(self) -> Tuple[Any, Dict[str, Any]]:
        sensors, info = self.sim.reset()
        return sensors, info

    async def step(
        self, action
    ) -> Tuple[Any, SupportsFloat, bool, bool, Dict[str, Any]]:
        return self.sim.step(action)

    async def close(self) -> None:
        self.sim.close()

    async def set_scenario(self, scenario) -> None:
        self.sim.scenario = scenario

    async def get_scenario(self) -> Scenario:
        if self.sim.scenario is None:
            return Scenario({"dummy": 0})

        return self.sim.scenario

    async def set_render_mode(self, render_mode):
        self.sim.render_mode = render_mode

    async def get_render_mode(self) -> str:
        return self.sim.render_mode

    async def get_render(self) -> Any:
        return self.sim.get_render("ascii")
