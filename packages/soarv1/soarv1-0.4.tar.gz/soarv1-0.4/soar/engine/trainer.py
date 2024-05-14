from tqdm import tqdm
from ..utils import Metric
from ..utils import gather


class BaseTrainer:
    def __init__(self, train_loader, model, criterion, optimizer, scheduler, ema, device):
        self.device = device
        self.model = model
        self.criterion = criterion
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.train_loader = train_loader
        self.train_size = len(train_loader.dataset)
        self.steps = len(train_loader)
        self.lr = self.scheduler.get_last_lr()[0]
        self.ema = ema

    def __call__(self, epoch, logger, header, master, world_size):
        self.model.train()
        metric = Metric(self.steps)
        process = tqdm(total=self.steps, desc=" " * 72, disable=not master)
        self.train_loader.sampler.set_epoch(epoch)
        for step, (images, labels, _) in enumerate(self.train_loader):
            images = images.to(self.device)
            labels = labels.float().squeeze().to(self.device)
            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()
            self.scheduler.step()
            self.ema.update()
            self.lr = self.scheduler.get_last_lr()[0]
            loss, outputs, labels = gather(loss, outputs, labels, world_size)
            loss, precision, recall, f1 = metric(loss, outputs, labels)
            if step < self.steps - 1:
                logger(header + [self.lr, loss, precision, recall, f1], process)
        m_loss, m_precision, m_recall, m_f1 = metric.release()
        logger(header + [self.lr, m_loss, m_precision, m_recall, m_f1], process)
        return m_loss, m_precision, m_recall, m_f1
