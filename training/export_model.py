# export_model.py

import torch
from convnext_regression import ConvNeXtTinyRegression

device = torch.device("cpu")

model = ConvNeXtTinyRegression()
model.load_state_dict(torch.load("best_convnext_regression.pth", map_location=device))
model.eval()

example_input = torch.randn(1, 3, 224, 224)

traced_model = torch.jit.trace(model, example_input)
traced_model.save("convnext_regression_scripted.pt")

print("Model exported successfully.")