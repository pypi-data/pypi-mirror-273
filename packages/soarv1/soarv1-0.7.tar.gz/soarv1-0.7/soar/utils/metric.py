import torch


class Metric:
    def __init__(self, size):
        self.size = size
        self.all_loss = 0.0
        self.all_output_num = 0.0
        self.all_label_num = 0.0
        self.all_right_num = 0.0
        self.ins = 1e-8

    def __call__(self, loss: float, outputs: torch.Tensor, labels: torch.Tensor):
        outputs = outputs.ge(0.5)
        labels = labels == 1.0
        output_num = outputs.sum().item()
        label_num = labels.sum().item()
        right_num = (outputs & labels).sum().item()
        self.all_loss += loss
        self.all_output_num += output_num
        self.all_label_num += label_num
        self.all_right_num += right_num
        precision = right_num / (output_num + self.ins)
        recall = right_num / (label_num + self.ins)
        f1 = 2 * (precision * recall) / (precision + recall + self.ins)
        return loss, precision, recall, f1

    def release(self):
        m_loss = self.all_loss / (self.size + self.ins)
        m_precision = self.all_right_num / (self.all_output_num + self.ins)
        m_recall = self.all_right_num / (self.all_label_num + self.ins)
        m_f1 = 2 * (m_precision * m_recall) / (m_precision + m_recall + self.ins)
        self.all_loss = 0.0
        self.all_output_num = 0.0
        self.all_label_num = 0.0
        self.all_right_num = 0.0
        return m_loss, m_precision, m_recall, m_f1
