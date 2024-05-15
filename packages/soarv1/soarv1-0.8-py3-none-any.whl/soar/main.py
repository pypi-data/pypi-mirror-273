import torch
import torch.multiprocessing as mp
from .context import Context


def run(rank, world_size, config):
    config["rank"] = rank
    config["world_size"] = world_size
    trainer = Context(config)
    trainer.train()


def main(config):
    world_size = len(config["train"]["device"])
    device_num = torch.cuda.device_count()
    assert world_size <= device_num
    mp.spawn(run, args=(world_size, config), nprocs=world_size, join=True)
