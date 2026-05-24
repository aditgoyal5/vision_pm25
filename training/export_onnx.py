import torch
from convnext_regression import ConvNeXtTinyRegression

model = ConvNeXtTinyRegression()
model.load_state_dict(torch.load("best_convnext_regression.pth", map_location="cpu"))
model.eval()

dummy = torch.randn(1,3,224,224)

torch.onnx.export(
    model,
    dummy,
    "convnext_regression.onnx",
    input_names=["image"],
    output_names=["pm"],
    opset_version=12
)

print("ONNX export complete")