from __future__ import annotations

import asyncio
import copy
import os
import secrets
import shutil
import tempfile
from dataclasses import dataclass, field, replace
from typing import Any, Callable, Dict, Optional, SupportsFloat, Type, Union

import gymnasium as gym
import jax.tree_util as jtu
import numpy as np
from gymnasium.core import ActType, ObsType
from gymnasium.envs.registration import EnvSpec
from minari import StepData
from minari.data_collector.callbacks import EpisodeMetadataCallback, StepDataCallback
from minari.dataset.minari_dataset import MinariDataset
from minari.dataset.minari_storage import MinariStorage
from minari.utils import _generate_dataset_metadata, _generate_dataset_path

AUTOSEED_BIT_SIZE = 64


@dataclass(frozen=True)
class EpisodeBuffer:
    """Contains the data of a single episode."""

    id: Optional[int] = None
    seed: Optional[int] = None
    observations: Union[None, list, dict, tuple] = None
    actions: Union[None, list, dict, tuple] = None
    rewards: list = field(default_factory=list)
    terminations: list = field(default_factory=list)
    truncations: list = field(default_factory=list)
    infos: Optional[dict] = None

    def add_step_data(self, step_data: StepData) -> EpisodeBuffer:
        """Add step data dictionary to episode buffer.

        Args:
            step_data (StepData): dictionary with data for a single step

        Returns:
            EpisodeBuffer: episode buffer with appended data
        """

        def _append(data, buffer):
            if isinstance(buffer, list):
                buffer.append(data)
                return buffer
            else:
                return [buffer, data]

        observations = step_data["observation"]
        if self.observations is not None:
            observations = jtu.tree_map(
                _append, step_data["observation"], self.observations
            )
        actions = step_data["action"]
        if self.actions is not None:
            actions = jtu.tree_map(_append, step_data["action"], self.actions)
        infos = step_data["info"]
        if self.infos is not None:
            infos = jtu.tree_map(_append, step_data["info"], self.infos)
        self.rewards.append(step_data["reward"])
        self.terminations.append(step_data["termination"])
        self.truncations.append(step_data["truncation"])

        return EpisodeBuffer(
            id=self.id,
            seed=self.seed,
            observations=observations,
            actions=actions,
            rewards=self.rewards,
            terminations=self.terminations,
            truncations=self.truncations,
            infos=infos,
        )

    def __len__(self) -> int:
        """Buffer length."""
        return len(self.rewards)


class AsyncDataCollector(gym.Wrapper):
    def __init__(
        self,
        env: gym.Env,
        step_data_callback: Type[StepDataCallback] = StepDataCallback,
        episode_metadata_callback: Type[
            EpisodeMetadataCallback
        ] = EpisodeMetadataCallback,
        record_infos: bool = False,
        observation_space: Optional[gym.Space] = None,
        action_space: Optional[gym.Space] = None,
        data_format: Optional[str] = None,
    ):
        super().__init__(env)
        self._step_data_callback = step_data_callback()
        self._episode_metadata_callback = episode_metadata_callback()

        self.datasets_path = os.environ.get("MINARI_DATASETS_PATH")
        if self.datasets_path is None:
            self.datasets_path = os.path.join(
                os.path.expanduser("~"), ".minari", "datasets"
            )
        if not os.path.exists(self.datasets_path):
            os.makedirs(self.datasets_path)
        self.data_format = data_format

        if observation_space is None:
            observation_space = env.observation_space
        self._observation_space = observation_space
        if action_space is None:
            action_space = env.action_space
        self._action_space = action_space

        self._record_infos = record_infos
        self._buffer: Optional[EpisodeBuffer] = None
        self._episode_id = 0
        self._reset_storage()

    def _reset_storage(self):
        self._episode_id = 0
        self._tmp_dir = tempfile.TemporaryDirectory(dir=self.datasets_path)
        data_format_kwarg = (
            {"data_format": self.data_format} if self.data_format is not None else {}
        )
        self._storage = MinariStorage.new(
            self._tmp_dir.name,
            observation_space=self._observation_space,
            action_space=self._action_space,
            env_spec=self.env.spec,
            **data_format_kwarg,
        )

    def step(
        self, action: ActType
    ) -> tuple[ObsType, SupportsFloat, bool, bool, dict[str, Any]]:
        obs, rew, terminated, truncated, info = self.env.step(action)

        step_data = self._step_data_callback(
            env=self.env,
            obs=obs,
            info=info,
            action=action,
            rew=rew,
            terminated=terminated,
            truncated=truncated,
        )

        assert self._storage.observation_space.contains(
            step_data["observation"]
        ), "Observation is not in observation space."
        assert self._storage.action_space.contains(
            step_data["action"]
        ), "Action is not in action space."

        assert self._buffer is not None
        if not self._record_infos:
            step_data["info"] = {}
        elif not self._buffer.infos:
            # Initialize buffer infos with the keys from the first step
            self._buffer = replace(
                self._buffer, infos={key: [] for key in step_data["info"].keys()}
            )

        # Ensure consistency in the info dictionary structure
        for key in self._buffer.infos.keys():
            if key not in step_data["info"]:
                step_data["info"][key] = None

        self._buffer = self._buffer.add_step_data(step_data)

        if step_data["termination"] or step_data["truncation"]:
            self._storage.update_episodes([self._buffer])
            self._episode_id += 1
            self._buffer = EpisodeBuffer(
                id=self._episode_id,
                observations=step_data["observation"],
                infos=(
                    {key: [] for key in step_data["info"].keys()}
                    if self._record_infos
                    else None
                ),
            )

        return obs, rew, terminated, truncated, info

    def reset(
        self,
        *,
        seed: int | None = None,
        options: dict[str, Any] | None = None,
    ) -> tuple[ObsType, dict[str, Any]]:
        self._flush_to_storage()

        autoseed_enabled = (not options) or options.get("minari_autoseed", True)
        if seed is None and autoseed_enabled:
            seed = secrets.randbits(AUTOSEED_BIT_SIZE)

        obs, info = self.env.reset(seed=seed, options=options)
        step_data = self._step_data_callback(env=self.env, obs=obs, info=info)

        self._buffer = EpisodeBuffer(
            id=self._episode_id,
            seed=seed,
            observations=step_data["observation"],
            infos=(
                {key: [] for key in step_data["info"].keys()}
                if self._record_infos
                else None
            ),
        )
        return obs, info

    def add_to_dataset(self, dataset: MinariDataset):
        self._flush_to_storage()

        first_id = dataset.storage.total_episodes
        dataset.storage.update_from_storage(self._storage)
        if dataset.episode_indices is not None:
            new_ids = first_id + np.arange(self._storage.total_episodes)
            dataset.episode_indices = np.append(dataset.episode_indices, new_ids)

        self._reset_storage()

    def create_dataset(
        self,
        dataset_id: str,
        eval_env: Optional[str | gym.Env | EnvSpec] = None,
        algorithm_name: Optional[str] = None,
        author: Optional[str] = None,
        author_email: Optional[str] = None,
        code_permalink: Optional[str] = None,
        ref_min_score: Optional[float] = None,
        ref_max_score: Optional[float] = None,
        expert_policy: Optional[Callable[[ObsType], ActType]] = None,
        num_episodes_average_score: int = 100,
        minari_version: Optional[str] = None,
        description: Optional[str] = None,
    ):
        dataset_path = _generate_dataset_path(dataset_id)
        metadata: Dict[str, Any] = _generate_dataset_metadata(
            dataset_id,
            copy.deepcopy(self.env.spec),
            eval_env,
            algorithm_name,
            author,
            author_email,
            code_permalink,
            ref_min_score,
            ref_max_score,
            expert_policy,
            num_episodes_average_score,
            minari_version,
            description,
        )

        self._save_to_disk(dataset_path, metadata)

        dataset = MinariDataset(dataset_path)
        metadata["dataset_size"] = dataset.storage.get_size()
        dataset.storage.update_metadata(metadata)
        return dataset

    def _flush_to_storage(self):
        if self._buffer is not None and len(self._buffer) > 0:
            if not self._buffer.terminations[-1]:
                self._buffer.truncations[-1] = True
            self._storage.update_episodes([self._buffer])
            self._episode_id += 1
        self._buffer = None

    def _save_to_disk(
        self, path: str | os.PathLike, dataset_metadata: Dict[str, Any] = {}
    ):
        self._flush_to_storage()

        assert (
            "observation_space" not in dataset_metadata.keys()
        ), "'observation_space' is not allowed as an optional key."
        assert (
            "action_space" not in dataset_metadata.keys()
        ), "'action_space' is not allowed as an optional key."
        assert (
            "env_spec" not in dataset_metadata.keys()
        ), "'env_spec' is not allowed as an optional key."
        self._storage.update_metadata(dataset_metadata)

        episode_metadata = self._storage.apply(self._episode_metadata_callback)
        self._storage.update_episode_metadata(episode_metadata)

        files = os.listdir(self._storage.data_path)
        for file in files:
            shutil.move(
                os.path.join(self._storage.data_path, file),
                os.path.join(path, file),
            )

        self._reset_storage()

    def close(self):
        super().close()
        self._buffer = None
        shutil.rmtree(self._tmp_dir.name)


async def collect_episode(env, i, policy=None):
    await asyncio.sleep(0)  # Allow other tasks to run
    env.reset()
    done = False
    while not done:
        action = env.action_space.sample() if policy is None else policy()
        obs, rew, terminated, truncated, info = env.step(action)
        done = terminated or truncated
    if i % 1000 == 0:
        print(f"Collected {i} episodes")


async def collect_samples_async(env_id, n_episodes, dataset_name, policy=None):
    env = gym.make(env_id)
    env = AsyncDataCollector(env, record_infos=True)

    tasks = [collect_episode(env, i, policy) for i in range(n_episodes)]
    await asyncio.gather(*tasks)

    dataset = env.create_dataset(dataset_name)
    env.close()
    return dataset
