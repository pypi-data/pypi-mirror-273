import minari
from torch.utils.data import DataLoader, Dataset

from .d4rl import *
from .helpers import *
from .minari_ext import *


class MinariRLDataset(Dataset):
    def __init__(
        self,
        dataset_id: str,
        env_id: str | None = None,
        num_episodes: int | None = None,
    ):

        try:
            dataset = minari.load_dataset(dataset_id)
            self.dataset = dataset
            return
        except:
            pass

        assert env_id is not None, "env_id must be provided if dataset_id is not found"
        assert (
            num_episodes is not None
        ), "num_episodes must be provided if dataset_id is not found"

        self.dataset_id = dataset_id
        self.env_id = env_id
        self.num_episodes = num_episodes
        self.dataset = None

    async def collect_episodes(self, num_envs: int = 1, print_every: int = 1000):
        if self.dataset:
            print("Dataset already exists")
            return

        await collect_samples_async(
            env_id=self.env_id,
            num_episodes=self.num_episodes,
            dataset_id=self.dataset_id,
            num_envs=num_envs,
            print_every=print_every,
        )
        self.dataset = minari.load_dataset(self.dataset_id)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx: int):
        return self.dataset[idx]


#
