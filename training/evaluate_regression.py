import torch
from torch.utils.data import DataLoader
import numpy as np

from training.regression_dataset import ImageRegressionDataset
from training.convnext_regression import ConvNeXtTinyRegression


MAX_PM = 530.0


def pm_to_bin(pm):
    if pm <= 50:
        return 0
    elif pm <= 100:
        return 1
    elif pm <= 150:
        return 2
    elif pm <= 200:
        return 3
    else:
        return 4


def main():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    test_dataset = ImageRegressionDataset("pm25vision", split="test")
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

    model = ConvNeXtTinyRegression().to(device)
    model.load_state_dict(torch.load("best_convnext_regression.pth", map_location=device))
    model.eval()

    preds = []
    targets = []

    with torch.no_grad():
        for images, pm in test_loader:
            images = images.to(device)
            outputs = model(images)

            preds.extend(outputs.cpu().numpy())
            targets.extend(pm.numpy())

    preds = np.array(preds) * MAX_PM
    targets = np.array(targets) * MAX_PM

    # Regression metrics
    mae = np.mean(np.abs(preds - targets))
    rmse = np.sqrt(np.mean((preds - targets) ** 2))

    # Bin accuracy
    pred_bins = [pm_to_bin(p) for p in preds]
    true_bins = [pm_to_bin(t) for t in targets]

    bin_accuracy = np.mean(np.array(pred_bins) == np.array(true_bins))

    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"5-bin Accuracy: {bin_accuracy:.4f}")


if __name__ == "__main__":
    main()