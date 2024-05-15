import os
import re
import copy
import pandas as pd
import dill as pickle
from io import BytesIO

import torch
from torch.cuda import amp
from torch import nn, optim
from torch import distributed as dist
from torch.nn.parallel import DistributedDataParallel
from torchsummary import summary

from .models import Model
from .datasets import LMDBDataset, LMDBDataLoader
from .engine import BaseTrainer, BaseValidator
from .utils import Loss, Optimizer, Scheduler, EMA
from .utils import Storager, Logger, Event
from .utils import de_parallel

from . import __version__


class Context:
    def __init__(self, config):
        self.rank = config["rank"]
        self.world_size = config["world_size"]
        self.addr = config["network"]["addr"]
        self.port = config["network"]["port"]
        self.master_process = self.rank == 0 if self.world_size >= 1 else self.rank == -1
        self.logger = Logger(self.master_process)

        self.config = config
        self.config_dataset = self.config["dataset"]
        self.config_dataloader = self.config["dataloader"]
        self.config_dataloader["rank"] = self.rank
        self.config_dataloader["world_size"] = self.world_size
        self.config_model = self.config["model"]
        self.config_train = self.config["train"]

        self.epoch = 0
        self.epochs = self.config_train["epochs"]
        self.save_dir = self.config_train["save_dir"]
        self.save_period = self.config_train["save_period"]
        self.device = self.config_train["device"][self.rank]
        self.resume = self.config_train["resume"]

        self.save_path = self.check_storage_path()
        self.storager, self.event = self.setup_train()
        self.logger("The results are saved in: %s" % self.save_path)

        self.train_dataset = LMDBDataset(self.config_dataset, "train")
        self.valid_dataset = LMDBDataset(self.config_dataset, "valid")
        self.train_loader = LMDBDataLoader(self.config_dataloader, self.train_dataset, "train")
        self.valid_loader = LMDBDataLoader(self.config_dataloader, self.valid_dataset, "valid")
        self.logger("%s size: %d" % ("train", len(self.train_dataset)))
        self.logger("%s size: %d" % ("valid", len(self.valid_dataset)))

        self.model = Model(self.config_model)().to(self.device)
        self.criterion = Loss(self.config_train["loss"])().to(self.device)
        self.optimizer = Optimizer(self.config_train["optimizer"], self.model)()
        self.scheduler = Scheduler(self.config_train["scheduler"], self.optimizer)()
        self.ema = EMA(self.config_train["ema"], self.model)

        self.resume_training()
        self.setup_ddp()
        self.setup_model()

        self.trainer = BaseTrainer(
            train_loader=self.train_loader,
            model=self.model,
            criterion=self.criterion,
            optimizer=self.optimizer,
            scheduler=self.scheduler,
            ema=self.ema,
            device=self.device)
        self.validator = BaseValidator(
            valid_loader=self.valid_loader,
            model=self.model,
            criterion=self.criterion,
            ema=self.ema,
            device=self.device)

    def __del__(self):
        dist.destroy_process_group()

    def train(self):
        while self.epoch < self.epochs:
            self.logger(["Epoch", "LR", "Loss", "P", "R", "F1"])
            self.epoch = self.epoch + 1
            train_result = self.trainer(
                logger=self.logger,
                epoch=self.epoch,
                header=[f"{self.epoch}/{self.epochs}"],
                master=self.master_process,
                world_size=self.world_size)
            valid_result = self.validator(
                epoch=self.epoch,
                logger=self.logger,
                header=["", ""],
                master=self.master_process,
                world_size=self.world_size)
            if self.master_process:
                lr = self.scheduler.get_last_lr()[0]
                self.event(epoch=self.epoch,
                           learning_rate=lr,
                           train_result=train_result,
                           valid_result=valid_result)
                self.save_model()
        self.epoch = 0

    def setup_ddp(self):
        os.environ["MASTER_ADDR"] = self.addr
        os.environ["MASTER_PORT"] = self.port
        backend = 'nccl' if dist.is_nccl_available() else 'gloo'
        dist.init_process_group(backend=backend, rank=self.rank,
                                world_size=self.world_size)
        torch.cuda.set_device(self.device)

    def setup_model(self):
        if self.master_process:
            summary(self.model, tuple(self.config_model["shape"]), -1, "cuda")
        if self.world_size > 1:
            self.model = DistributedDataParallel(
                module=self.model,
                device_ids=[self.device])

    def setup_train(self):
        if self.master_process:
            storager = Storager(self.save_path, self.config_dataset["key"])
            event = Event(storager)
        elif self.resume:
            storager = Storager(self.save_path, self.config_dataset["key"])
            event = None
        else:
            storager, event = None, None
        return storager, event

    def save_model(self):
        """Save model checkpoints based on various conditions."""
        buffer = BytesIO()
        ckpt = {
            'epoch': self.epoch,
            'model': de_parallel(copy.deepcopy(self.model)),
            'ema': de_parallel(copy.deepcopy(self.ema.shadow)),
            'optimizer': pickle.dumps(self.optimizer.state_dict()),
            'scheduler': pickle.dumps(self.scheduler.state_dict()),
            'config': self.config,
            'version': __version__
        }
        torch.save(ckpt, buffer, pickle_module=pickle)
        self.storager.write(f"./weights/last.pt", buffer)
        if self.epoch == self.event.best_epoch:
            self.storager.write(f"./weights/best.pt", buffer)
        if self.epoch % self.save_period == 0:
            model_path = f"./weights/epoch{self.epoch}.pt"
            self.storager.write(model_path, buffer)

    def check_storage_path(self):
        current_id = 0
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        for file_name in os.listdir(self.save_dir):
            match = re.search(r'exp(\d+)\.lmdb', file_name)
            if match is not None:
                match_id = int(match.group(1))
                if match_id > current_id:
                    current_id = match_id
        self.resume = True if self.resume and current_id != 0 else False
        current_id = current_id if self.resume else current_id + 1
        save_path = os.path.join(self.save_dir, "exp{}.lmdb".format(current_id))
        return save_path

    def resume_training(self):
        """Resume training from given epoch."""
        if self.resume:
            csv_key = "./result.csv"
            csv_byte = self.storager.read(csv_key)
            if csv_byte is not None:
                csv_buffer = BytesIO(csv_byte)
                result = pd.read_csv(csv_buffer)
                if self.master_process:
                    self.event.reload(result)
                self.epoch = len(result)

                pt_key = f"./weights/last.pt"
                pt_byte = self.storager.read(pt_key)
                pt_buffer = BytesIO(pt_byte)
                weight = torch.load(pt_buffer)

                state_dict = weight["model"].state_dict()
                self.model.load_state_dict(state_dict)
                self.optimizer.load_state_dict(pickle.loads(weight["optimizer"]))
                self.scheduler.load_state_dict(pickle.loads(weight["scheduler"]))
                self.ema.shadow = {k: v.to(self.device) for k, v in weight["ema"].items()}
