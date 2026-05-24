import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from models.multitask_model import HybridModel
from training.pm25_dataset import PM25VisionDataset
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_dataset = PM25VisionDataset("pm25vision", split="train")
test_dataset = PM25VisionDataset("pm25vision", split="test")

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

sample_img, sample_feat, _ = train_dataset[0]
feature_dim = sample_feat.shape[0]

model = HybridModel(feature_dim).to(device)

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training
for epoch in range(10):
    model.train()
    total_loss = 0

    for imgs, feats, targets in train_loader:
        imgs = imgs.to(device)
        feats = feats.to(device)
        targets = targets.to(device)

        optimizer.zero_grad()
        outputs = model(imgs, feats)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    print(f"Epoch {epoch+1}, Train Loss: {total_loss/len(train_loader):.4f}")

# Evaluation
model.eval()
all_preds = []
all_targets = []

with torch.no_grad():
    for imgs, feats, targets in test_loader:
        imgs = imgs.to(device)
        feats = feats.to(device)

        outputs = model(imgs, feats)

        all_preds.extend(outputs.cpu().numpy().flatten())
        all_targets.extend(targets.numpy().flatten())

mae = mean_absolute_error(all_targets, all_preds)
r2 = r2_score(all_targets, all_preds)

print("Test MAE:", mae)
print("Test R2:", r2)

torch.save(model.state_dict(), "models/pm25vision_hybrid.pth")
print("Model Saved.")