from tqdm import tqdm
from ..utils import Metric
from ..utils import gather


class BaseValidator:
    def __init__(self, valid_loader, model, criterion, ema, device):
        self.device = device
        self.model = model
        self.criterion = criterion
        self.valid_loader = valid_loader
        self.valid_size = len(valid_loader.dataset)
        self.steps = len(valid_loader)
        self.ema = ema

    def __call__(self, epoch, logger, header, master, world_size):
        self.model.eval()
        self.ema.apply_shadow()
        metric = Metric(self.steps)
        process = tqdm(total=self.steps, desc=" " * 72, disable=not master)
        self.valid_loader.sampler.set_epoch(epoch)
        for step, (images, labels, _) in enumerate(self.valid_loader):
            images = images.to(self.device)
            labels = labels.float().squeeze().to(self.device)
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss, outputs, labels = gather(loss, outputs, labels, world_size)
            loss, precision, recall, f1 = metric(loss, outputs, labels)
            if step < self.steps - 1:
                logger(header + [loss, precision, recall, f1], process)
        self.ema.restore()
        m_loss, m_precision, m_recall, m_f1 = metric.release()
        logger(header + [m_loss, m_precision, m_recall, m_f1], process)
        return m_loss, m_precision, m_recall, m_f1
