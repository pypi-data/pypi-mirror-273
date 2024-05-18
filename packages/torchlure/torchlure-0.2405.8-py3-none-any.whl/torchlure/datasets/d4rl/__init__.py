from pathlib import Path
from typing import Any, Dict, List, Union

import gymnasium as gym
import h5py
import minari
import requests
from minari.data_collector.episode_buffer import EpisodeBuffer
from minari.utils import create_dataset_from_buffers
from torch.utils.data import Dataset


class D4RLDataset(Dataset):
    def __init__(
        self,
        dataset_id: str,
        d4rl_name: Union[str, None] = None,
        env_id: Union[str, None] = None,
        hdf5_url: Union[str, None] = None,
    ):
        self.dataset_id = dataset_id
        self.d4rl_name = d4rl_name
        self.env_id = env_id
        self.hdf5_url = hdf5_url
        self.dataset = self.load_or_create_dataset()

    def load_or_create_dataset(self) -> minari.MinariDataset:
        """Load an existing dataset or create a new one if not found."""
        try:
            dataset = minari.load_dataset(self.dataset_id)
            print(f"Loaded dataset '{self.dataset_id}' with {len(dataset)} episodes.")
            return dataset
        except Exception as e:
            print(f"Could not load dataset '{self.dataset_id}': {e}")

        if self.d4rl_name is None or self.env_id is None or self.hdf5_url is None:
            raise ValueError(
                "d4rl_name, env_id, and hdf5_url must be provided to create the dataset."
            )

        self.download_d4rl_dataset()
        self.verify_hdf5_contents()
        env = gym.make(self.env_id)
        episodes = self.collect_all_episodes_from_hdf5()
        self.initialize_episode_fields(episodes)
        episode_buffer_list = self.create_episode_buffer_list(episodes)
        self.create_minari_dataset(episode_buffer_list, env)

        dataset = minari.load_dataset(self.dataset_id)
        print(f"Created dataset '{self.dataset_id}' with {len(dataset)} episodes.")
        return dataset

    def download_d4rl_dataset(self) -> None:
        """Download the dataset from a given URL if it does not already exist."""
        minari_dir = Path.home() / ".minari"
        dataset_dir = minari_dir / "datasets" / self.d4rl_name

        minari_dir.mkdir(parents=True, exist_ok=True)
        dataset_dir.mkdir(parents=True, exist_ok=True)

        target_path = dataset_dir / "main_data.hdf5"
        if target_path.exists():
            print(
                f"{self.d4rl_name} already exists at {target_path}, skipping download."
            )
        else:
            print(f"Downloading {self.d4rl_name} from {self.hdf5_url}...")
            response = requests.get(self.hdf5_url, stream=True)
            response.raise_for_status()
            with open(target_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded {self.d4rl_name} to {target_path}.")

    def verify_hdf5_contents(self) -> None:
        """Verify the contents of the HDF5 file."""
        hdf5_path = (
            Path.home() / ".minari" / "datasets" / self.d4rl_name / "main_data.hdf5"
        )
        with h5py.File(hdf5_path, "r") as f:
            print(f"Verifying contents of {hdf5_path}:")
            f.visititems(lambda name, obj: print(f"{name}: {obj}"))

    def collect_all_episodes_from_hdf5(self) -> List[Dict[str, Any]]:
        """Collect and return all episodes from the HDF5 file."""
        hdf5_path = (
            Path.home() / ".minari" / "datasets" / self.d4rl_name / "main_data.hdf5"
        )
        with h5py.File(hdf5_path, "r") as f:
            observations = f["observations"][:]
            actions = f["actions"][:]
            rewards = f["rewards"][:]
            terminals = f["terminals"][:]
            timeouts = f["timeouts"][:]
            infos = {key: f["infos"][key][:] for key in f["infos"]}
            next_observations = f["next_observations"][:]

        episodes = []
        episode = {
            "observations": [],
            "actions": [],
            "rewards": [],
            "terminations": [],
            "truncations": [],
            "infos": {key: [] for key in infos},
            "next_observations": [],
        }

        for i in range(len(observations)):
            episode["observations"].append(observations[i])
            episode["actions"].append(actions[i])
            episode["rewards"].append(rewards[i])
            episode["terminations"].append(terminals[i])
            episode["truncations"].append(timeouts[i])
            for key in infos:
                episode["infos"][key].append(infos[key][i])
            episode["next_observations"].append(next_observations[i])

            if terminals[i] or timeouts[i]:
                episodes.append(episode)
                episode = {
                    "observations": [],
                    "actions": [],
                    "rewards": [],
                    "terminations": [],
                    "truncations": [],
                    "infos": {key: [] for key in infos},
                    "next_observations": [],
                }

        print(f"Collected {len(episodes)} episodes from HDF5 file.")
        return episodes

    @staticmethod
    def initialize_episode_fields(episodes: List[Dict[str, Any]]) -> None:
        """Ensure that all fields in each episode are correctly initialized."""
        for ep in episodes:
            ep.setdefault("observations", [])
            ep.setdefault("actions", [])
            ep.setdefault("rewards", [])
            ep.setdefault("terminations", [])
            ep.setdefault("truncations", [])
            ep["infos"] = ep.get("infos") or {}
            ep.setdefault("next_observations", [])

    @staticmethod
    def create_episode_buffer_list(
        episodes: List[Dict[str, Any]]
    ) -> List[EpisodeBuffer]:
        """Create and return a list of EpisodeBuffer objects from the episodes."""
        episode_buffers = [
            EpisodeBuffer(
                id=i,
                seed=None,
                observations=ep["observations"],
                actions=ep["actions"],
                rewards=ep["rewards"],
                terminations=ep["terminations"],
                truncations=ep["truncations"],
                infos=ep["infos"],
            )
            for i, ep in enumerate(episodes)
        ]
        print(f"Created {len(episode_buffers)} episode buffers.")
        return episode_buffers

    def create_minari_dataset(
        self, episode_buffer_list: List[EpisodeBuffer], env: gym.Env
    ) -> None:
        """Create a Minari dataset from the episode buffers."""
        create_dataset_from_buffers(
            dataset_id=self.dataset_id,
            buffer=episode_buffer_list,
            env=env.spec.id,
            minari_version=minari.__version__,
            action_space=env.action_space,
            observation_space=env.observation_space,
        )
        print(f"Dataset '{self.dataset_id}' created successfully.")

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx: int):
        return self.dataset[idx]
