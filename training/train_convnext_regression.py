import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

from training.regression_dataset import ImageRegressionDataset
from training.convnext_regression import ConvNeXtTinyRegression

MAX_PM = 530.0


def evaluate(model, loader, device):
    model.eval()
    preds = []
    targets = []

    with torch.no_grad():
        for images, pm in loader:
            images = images.to(device)
            pm = pm.to(device)

            outputs = model(images)

            preds.extend(outputs.cpu().numpy())
            targets.extend(pm.cpu().numpy())

    preds = np.array(preds) * MAX_PM
    targets = np.array(targets) * MAX_PM
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

    pred_bins = [pm_to_bin(p) for p in preds]
    true_bins = [pm_to_bin(t) for t in targets]

    bin_accuracy = np.mean(np.array(pred_bins) == np.array(true_bins))
    mae = mean_absolute_error(targets, preds)
    r2 = r2_score(targets, preds)
    rmse = np.sqrt(np.mean((preds - targets) ** 2))

    return mae, rmse, r2


def main():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    train_dataset = ImageRegressionDataset("pm25vision", split="train")
    test_dataset = ImageRegressionDataset("pm25vision", split="test")

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False, num_workers=0)

    model = ConvNeXtTinyRegression().to(device)

    # ---- Load pretrained classification weights ----
    state_dict = torch.load("best_convnext_model.pth", map_location=device)
    state_dict = {k: v for k, v in state_dict.items() if "classifier.2" not in k}
    model.load_state_dict(state_dict, strict=False)

    # ======================
    # PHASE 1
    # ======================

    for param in model.model.features.parameters():
        param.requires_grad = False

    print("\nPhase 1: Training regression head only\n")

    criterion = nn.SmoothL1Loss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

    for epoch in range(5):

        model.train()
        total_loss = 0

        for images, pm in train_loader:
            images = images.to(device)
            pm = pm.to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, pm)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        mae, rmse, r2 = evaluate(model, test_loader, device)

        print(f"Epoch {epoch+1}/5")
        print(f"Train Loss: {total_loss/len(train_loader):.4f}")
        print(f"MAE: {mae:.2f} | RMSE: {rmse:.2f} | R2: {r2:.4f}")
        print("-" * 50)

    # ======================
    # PHASE 2
    # ======================

    print("\nPhase 2: Fine-tuning entire network\n")

    for param in model.model.features.parameters():
        param.requires_grad = True

    criterion = nn.HuberLoss(delta=0.05)

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=7e-6,
        weight_decay=1e-4
    )

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer,
        T_max=20
    )

    for epoch in range(20):

        model.train()
        total_loss = 0

        for images, pm in train_loader:
            images = images.to(device)
            pm = pm.to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, pm)

            loss.backward()

            torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)

            optimizer.step()

            total_loss += loss.item()

        scheduler.step()

        mae, rmse, r2 = evaluate(model, test_loader, device)

        print(f"Epoch {epoch+1}/20")
        print(f"Train Loss: {total_loss/len(train_loader):.4f}")
        print(f"MAE: {mae:.2f} | RMSE: {rmse:.2f} | R2: {r2:.4f}")
        print("-" * 50)

    torch.save(model.state_dict(), "best_convnext_regression.pth")


if __name__ == "__main__":
    main()