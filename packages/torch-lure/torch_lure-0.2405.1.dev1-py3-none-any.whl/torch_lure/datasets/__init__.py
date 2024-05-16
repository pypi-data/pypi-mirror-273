from .minari_ext import *
import minari
from torch.utils.data import DataLoader, Dataset


class D4RLDataset(Dataset):
    def __init__(
        self, dataset_name: str, env_id: str | None = None, n_episode: int | None = None
    ):

        try:
            dataset = minari.load_dataset(dataset_name)
            self.dataset = dataset
            return
        except:
            pass

        assert (
            env_id is not None
        ), "env_id must be provided if dataset_name is not found"
        assert (
            n_episode is not None
        ), "n_episodes must be provided if dataset_name is not found"

        self.dataset_name = dataset_name
        self.env_id = env_id
        self.n_episodes = n_episodes
        self.dataset = None

    async def collect_episodes(self):
        if self.dataset:
            print("Dataset already exists")
            return

        await collect_samples_async(
            env_id=self.env_id,
            n_episodes=self.n_episodes,
            dataset_name=self.dataset_name,
        )
        self.dataset = minari.load_dataset(self.dataset_name)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx: int):
        return self.dataset[idx]
