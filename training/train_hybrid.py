# train_fusion.py

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import accuracy_score, classification_report, f1_score
import numpy as np

from training.pm25_dataset import ImageAQIDataset
from models.multitask_model import ConvNeXtTinyAQI
from tqdm import tqdm

def main():

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)

    # -----------------------
    # Dataset & Dataloader
    # -----------------------

    train_dataset = ImageAQIDataset("pm25vision", split="train")
    test_dataset = ImageAQIDataset("pm25vision", split="test")

    train_loader = DataLoader(
        train_dataset,
        batch_size=16,
        shuffle=True,
        num_workers=0
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=16,
        shuffle=False,
        num_workers=0
    )

    # -----------------------
    # Model
    # -----------------------

    model = ConvNeXtTinyAQI().to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=1e-4,
        weight_decay=1e-4
    )

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer,
        T_max=25
    )

    epochs = 25
    best_f1 = 0

    # ===============================
    # Training Loop
    # ===============================

    for epoch in range(epochs):

        model.train()
        total_loss = 0

        progress_bar = tqdm(
            train_loader,
            desc=f"Epoch {epoch+1}/{epochs}"
        )

        for images, labels in progress_bar:

            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

            progress_bar.set_postfix(loss=loss.item())

        scheduler.step()

        # -----------------------
        # Validation
        # -----------------------

        model.eval()
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for images, labels in test_loader:

                images = images.to(device)

                outputs = model(images)
                preds = torch.argmax(outputs, dim=1)

                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.numpy())

        acc = accuracy_score(all_labels, all_preds)
        f1 = f1_score(all_labels, all_preds, average="macro")

        print("\n--------------------------------------")
        print(f"Epoch {epoch+1}/{epochs}")
        print(f"Train Loss: {total_loss/len(train_loader):.4f}")
        print(f"Val Accuracy: {acc:.4f}")
        print(f"Val Macro F1: {f1:.4f}")
        print("--------------------------------------\n")

        if f1 > best_f1:
            best_f1 = f1
            torch.save(model.state_dict(), "best_convnext_model.pth")

    # ===============================
    # Final Report
    # ===============================

    print("Best Macro F1:", best_f1)

    print(classification_report(
        all_labels,
        all_preds,
        labels=[0, 1, 2, 3, 4],
        zero_division=0
    ))


if __name__ == "__main__":
    main()