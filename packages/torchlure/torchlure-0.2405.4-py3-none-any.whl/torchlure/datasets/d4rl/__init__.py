from pathlib import Path
from typing import Any, Dict, List, Literal

import gdown
import gymnasium as gym
import minari
from minari.data_collector.episode_buffer import EpisodeBuffer
from minari.dataset._storages.hdf5_storage import HDF5Storage
from minari.utils import create_dataset_from_buffers
from torch.utils.data import DataLoader, Dataset


def download_d4rl_dataset(dataset_name):
    datasets = {
        "d4rl_halfcheetah-expert-v2": "https://drive.google.com/drive/folders/1YcUMTS7cMrUP8KJ6aQL87D9uYnrvGT02?usp=drive_link",
        "d4rl_hopper-expert-v2": "https://drive.google.com/drive/folders/1upUt_aCRc3MCWhfVwpDlnW7YoVFEHre9?usp=drive_link",
        "d4rl_walker2d-expert-v2": "https://drive.google.com/drive/folders/1ncu2DEhADWQBH6EeU_SrywQm8ETMM15M?usp=drive_link",
    }
    assert (
        dataset_name in datasets
    ), f"Dataset {dataset_name} not found in available datasets: {datasets.keys()}"

    # Create directories if they do not exist
    minari_dir = Path.home() / ".minari"
    datasets_dir = minari_dir / "datasets"
    minari_dir.mkdir(parents=True, exist_ok=True)
    datasets_dir.mkdir(parents=True, exist_ok=True)

    # Download dataset if it does not exist already
    target_path = datasets_dir / dataset_name
    if target_path.exists():
        print(f"{dataset_name} already exists at {target_path}, skipping download.")
    else:
        url = datasets[dataset_name]
        gdown.download_folder(
            url=url, output=str(target_path), quiet=False, use_cookies=False
        )


def collect_all_episodes(storage: HDF5Storage) -> List[Dict[str, Any]]:
    """Collect and return all episodes from the storage."""
    episodes = []
    index = 0
    while True:
        try:
            episode = storage.get_episodes([index])[0]
            episodes.append(episode)
            index += 1
        except (IndexError, KeyError):
            break
    return episodes


def initialize_episode_fields(episodes: List[Dict[str, Any]]) -> None:
    """Ensure that all fields in each episode are correctly initialized."""
    for ep in episodes:
        ep.setdefault("observations", [])
        ep.setdefault("actions", [])
        ep.setdefault("rewards", [])
        ep.setdefault("terminations", [])
        ep.setdefault("truncations", [])
        ep["infos"] = ep.get("infos") or {}

        # # Log the episode content to debug any potential issues
        # print(f"Episode ID: {ep.get('id')}, Seed: {ep.get('seed')}")
        # print(f"Observations: {len(ep.get('observations'))}")
        # print(f"Actions: {len(ep.get('actions'))}")
        # print(f"Rewards: {len(ep.get('rewards'))}")
        # print(f"Terminations: {len(ep.get('terminations'))}")
        # print(f"Truncations: {len(ep.get('truncations'))}")
        # print(f"Infos: {len(ep['infos'])}")


def create_episode_buffer_list(episodes: List[Dict[str, Any]]) -> List[EpisodeBuffer]:
    """Create and return a list of EpisodeBuffer objects from the episodes."""
    return [
        EpisodeBuffer(
            id=ep.get("id"),
            seed=ep.get("seed"),
            observations=ep.get("observations", []),
            actions=ep.get("actions", []),
            rewards=ep.get("rewards", []),
            terminations=ep.get("terminations", []),
            truncations=ep.get("truncations", []),
            infos=ep.get("infos", {}),
        )
        for ep in episodes
    ]


def create_minari_dataset(
    dataset_id: str, episode_buffer_list: List[EpisodeBuffer], env: gym.Env
) -> None:
    """Create a Minari dataset from the episode buffers."""
    create_dataset_from_buffers(
        dataset_id=dataset_id,
        buffer=episode_buffer_list,
        env=env.spec.id,
        minari_version=minari.__version__,
        action_space=env.action_space,
        observation_space=env.observation_space,
    )
    print(f"Dataset '{dataset_id}' created successfully.")


class D4RLDataset(Dataset):
    def __init__(
        self,
        dataset_id: str,
        d4rl_name: (
            Literal[
                "d4rl_halfcheetah-expert-v2",
                "d4rl_hopper-expert-v2",
                "d4rl_walker2d-expert-v2",
            ]
            | None
        ) = None,
        env_id: str | None = None,
    ):

        try:
            dataset = minari.load_dataset(dataset_id)
            self.dataset = dataset
            return
        except:
            pass

        download_d4rl_dataset(dataset_name=d4rl_name)

        # Initialize the environment
        env = gym.make(env_id)

        # Get the path to the HDF5 file
        data_path = Path.home() / ".minari" / "datasets" / d4rl_name / "data"
        if not data_path.exists():
            raise FileNotFoundError(f"Data path does not exist: {data_path}")

        # Initialize HDF5Storage
        storage = HDF5Storage(data_path, env.observation_space, env.action_space)

        # Collect all episodes
        episodes = collect_all_episodes(storage)

        # Ensure that all fields are correctly initialized
        initialize_episode_fields(episodes)

        # Create the list of episode buffers
        episode_buffer_list = create_episode_buffer_list(episodes)

        # Create the Minari dataset from buffers
        create_minari_dataset(dataset_id, episode_buffer_list, env)

        # Load and print the length of the dataset
        dataset = minari.load_dataset(dataset_id)

        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx: int):
        return self.dataset[idx]
