import os
import time
import copy
import pandas as pd
from io import BytesIO
from subprocess import Popen, PIPE
from torch.utils.tensorboard import SummaryWriter


class Event:
    def __init__(self, storager):
        self.storager = storager
        self.writer = SummaryWriter(self.storager.save_path)
        self.process = self.start_tensorboard()
        self.metrics = {
            "epoch": [],
            "precision/train": [],
            "precision/valid": [],
            "recall/train": [],
            "recall/valid": [],
            "f1/train": [],
            "f1/valid": [],
            "loss/train": [],
            "loss/valid": [],
            "learning_rate": []
        }
        self.best_epoch = 0

    def __call__(self, epoch, learning_rate, train_result, valid_result):
        self.metrics["epoch"].append(epoch)
        self.metrics["learning_rate"].append(learning_rate)
        self.metrics["loss/train"].append(train_result[0])
        self.metrics["loss/valid"].append(valid_result[0])
        self.metrics["precision/train"].append(train_result[1])
        self.metrics["precision/valid"].append(valid_result[1])
        self.metrics["recall/train"].append(train_result[2])
        self.metrics["recall/valid"].append(valid_result[2])
        self.metrics["f1/train"].append(train_result[3])
        self.metrics["f1/valid"].append(valid_result[3])
        if valid_result[3] == max(self.metrics["f1/valid"]):
            self.best_epoch = epoch
        self.write_csv()
        self.write_summary()

    def __del__(self):
        self.writer.close()
        self.process.terminate()

    def start_tensorboard(self):
        """Start a tensorboard process"""
        cmd = ["tensorboard",
               "--logdir", self.storager.save_path,
               "--load_fast", "false",
               "--port", "6006"]
        process = Popen(cmd)
        time.sleep(5)
        return process

    def reload(self, result):
        metrics = result.to_dict()
        for key, value in metrics.items():
            metrics[key] = list(value.values())
        self.metrics = copy.deepcopy(metrics)
        epochs = metrics.pop("epoch")
        for epoch in epochs:
            for name, metric in metrics.items():
                self.writer.add_scalar(name, metric[epoch-1], epoch)

        # concat tensorboard output
        # event_list = []
        # for event_name in os.listdir(self.storager.save_path):
        #     if event_name.startswith("events"):
        #         event_list.append(os.path.join(self.storager.save_path, event_name))
        # buffer = BytesIO()
        # for event_path in event_list:
        #     with open(event_path, "rb") as event_file:
        #         buffer.write(event_file.read())
        #         os.remove(event_path)
        # output_path = event_list[-1]
        # with open(output_path, "wb") as output_file:
        #     output_file.write(buffer.getvalue())

    def write_csv(self):
        """Saves training metrics to a CSV file."""
        buffer = BytesIO()
        df = pd.DataFrame(self.metrics)
        df.to_csv(buffer, index=False)
        csv_path = "./result.csv"
        self.storager.write(csv_path, buffer)

    def write_summary(self):
        """Saves training metrics to tensorboard."""
        metrics = copy.deepcopy(self.metrics)
        epoch = metrics.pop("epoch")[-1]
        for name, metric in metrics.items():
            self.writer.add_scalar(name, metric[-1], epoch)
