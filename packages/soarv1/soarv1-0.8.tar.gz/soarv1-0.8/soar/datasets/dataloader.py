from torch.utils.data.dataloader import DataLoader
from torch.utils.data import DistributedSampler


class LMDBDataLoader(DataLoader):
    def __init__(self, config, dataset, mode, *args, **kwargs):
        self.mode = mode
        self.config = config[mode]
        self.world_size = config["world_size"] if "world_size" in config.keys() else 1
        self.batch_size = self.config["batch_size"] // self.world_size
        self.num_workers = self.config["num_workers"] // self.world_size
        self.drop_last = self.config["drop_last"]
        self.sampler = LMDBDataSampler(config, dataset, mode)
        super(LMDBDataLoader, self).__init__(
            dataset=dataset,
            batch_size=self.batch_size,
            num_workers=self.num_workers,
            sampler=self.sampler,
            drop_last=self.drop_last,
            *args, **kwargs)


class LMDBDataSampler(DistributedSampler):
    def __init__(self, config, dataset, mode):
        self.rank = config["rank"] if "rank" in config.keys() else 0
        self.world_size = config["world_size"] if "world_size" in config.keys() else 1
        self.config = config[mode]
        self.shuffle = self.config["shuffle"]
        super(LMDBDataSampler, self).__init__(
            dataset=dataset,
            num_replicas=self.world_size,
            rank=self.rank,
            shuffle=self.shuffle)
