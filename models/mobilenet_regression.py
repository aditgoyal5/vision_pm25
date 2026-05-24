import torch
import torch.nn as nn
import torchvision.models as models

class MobileNetRegressor(nn.Module):
    def __init__(self):
        super().__init__()

        self.backbone = models.mobilenet_v2(pretrained=True)

        # Replace classifier
        self.backbone.classifier = nn.Sequential(
            nn.Linear(self.backbone.last_channel, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 1)
        )

    def forward(self, x):
        return self.backbone(x)