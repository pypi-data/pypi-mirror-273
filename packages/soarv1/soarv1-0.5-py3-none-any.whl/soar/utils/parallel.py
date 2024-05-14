import torch
import torch.distributed as dist
from torch.nn.parallel import DataParallel, DistributedDataParallel


def gather(loss, outputs, labels, world_size):
    all_loss, all_outputs, all_labels = [], [], []
    for _ in range(world_size):
        all_loss.append(torch.empty_like(loss.data.unsqueeze(0)))
        all_outputs.append(torch.empty_like(outputs.data))
        all_labels.append(torch.empty_like(labels))
    dist.all_gather(all_loss, loss.data.unsqueeze(0))
    dist.all_gather(all_outputs, outputs.data)
    dist.all_gather(all_labels, labels)
    loss = torch.cat(all_loss, dim=0).sum().item()
    outputs = torch.cat(all_outputs, dim=0)
    labels = torch.cat(all_labels, dim=0)
    return loss, outputs, labels


def de_parallel(model):
    if isinstance(model, (DataParallel, DistributedDataParallel)):
        model = model.module
    return model
