# models/convnext_regression_model.py

import torch.nn as nn
import torchvision.models as models


class ConvNeXtTinyRegression(nn.Module):
    def __init__(self):
        super().__init__()

        self.model = models.convnext_tiny(weights=None)

        in_features = self.model.classifier[2].in_features

        # Replace final layer with regression output
        self.model.classifier[2] = nn.Linear(in_features, 1)

    def forward(self, x):
        return self.model(x).squeeze(1)