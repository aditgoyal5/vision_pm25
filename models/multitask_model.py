# models/convnext_tiny_model.py

import torch.nn as nn
import torchvision.models as models


class ConvNeXtTinyAQI(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = models.convnext_tiny(weights="DEFAULT")

        in_features = self.model.classifier[2].in_features

        # Replace ONLY the final linear layer
        self.model.classifier[2] = nn.Linear(in_features, 5)

    def forward(self, x):
        return self.model(x)