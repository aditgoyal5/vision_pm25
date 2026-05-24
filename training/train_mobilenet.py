import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from models.mobilenet_regression import MobileNetRegressor
from training.pm25_dataset import PM25VisionImageDataset
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

train_dataset = PM25VisionImageDataset("pm25vision", split="train")
test_dataset = PM25VisionImageDataset("pm25vision", split="test")

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

model = MobileNetRegressor().to(device)

# Freeze early layers (transfer learning)
for param in model.backbone.features.parameters():
    param.requires_grad = False

criterion = nn.MSELoss()
optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.001)

for epoch in range(15):
    model.train()
    total_loss = 0

    for imgs, targets in train_loader:
        imgs = imgs.to(device)
        targets = targets.to(device)

        optimizer.zero_grad()
        outputs = model(imgs)
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
    for imgs, targets in test_loader:
        imgs = imgs.to(device)
        outputs = model(imgs)

        preds = outputs.cpu().numpy().flatten()
        targets = targets.numpy().flatten()

        # Denormalize
        preds = train_dataset.denormalize(preds)
        targets = train_dataset.denormalize(targets)

        all_preds.extend(preds)
        all_targets.extend(targets)

mae = mean_absolute_error(all_targets, all_preds)
r2 = r2_score(all_targets, all_preds)

print("Test MAE:", mae)
print("Test R2:", r2)

torch.save(model.state_dict(), "models/mobilenet_pm25.pth")
print("Model Saved.")