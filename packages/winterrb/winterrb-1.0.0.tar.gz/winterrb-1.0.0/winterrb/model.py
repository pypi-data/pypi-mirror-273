"""
Module for the model
"""

import torch
import torch.nn.functional as F
from torch import nn


class WINTERNet(nn.Module):
    """
    WINTERNet model
    """

    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)
        # self.conv1 = nn.Conv2d(81, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(
            in_channels=16, out_channels=16, kernel_size=3, padding=1
        )
        self.conv3 = nn.Conv2d(
            in_channels=16, out_channels=16, kernel_size=3, padding=1
        )
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.batch_norm1 = nn.BatchNorm2d(16, momentum=0.99, eps=1e-3)
        self.dropout1 = nn.Dropout2d(p=0.25)
        self.conv4 = nn.Conv2d(
            in_channels=16, out_channels=32, kernel_size=3, padding=1
        )
        self.conv5 = nn.Conv2d(
            in_channels=32, out_channels=32, kernel_size=3, padding=1
        )
        self.conv6 = nn.Conv2d(
            in_channels=32, out_channels=32, kernel_size=3, padding=1
        )
        self.pool2 = nn.MaxPool2d(kernel_size=4, stride=4)
        self.batch_norm2 = nn.BatchNorm2d(32, momentum=0.99, eps=1e-3)
        self.dropout2 = nn.Dropout2d(p=0.25)
        # self.fc1 = nn.Linear(32 * 5 * 5, 256)  # Calculated based on the size after applying max pooling
        self.fc1 = nn.Linear(3200, 256)
        self.batch_norm3 = nn.BatchNorm1d(256, momentum=0.99, eps=1e-3)
        self.dropout3 = nn.Dropout(p=0.5)
        self.fc_out = nn.Linear(256, 1)

    def forward(self, x):
        x = x.to(self.conv1.bias.dtype)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = self.pool(x)
        x = self.batch_norm1(x)
        x = self.dropout1(x)
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        x = F.relu(self.conv6(x))
        x = self.pool2(x)
        x = self.batch_norm2(x)
        x = self.dropout2(x)
        x = x.reshape(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.batch_norm3(x)
        x = self.dropout3(x)
        x = self.fc_out(x)
        x = torch.sigmoid(x)
        return x.view(-1, 1)
