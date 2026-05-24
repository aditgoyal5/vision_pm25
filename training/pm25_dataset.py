# dataset/image_dataset.py

import os
import pandas as pd
from PIL import Image
import torch
from torch.utils.data import Dataset
from torchvision import transforms


def pm_to_aqi_class(pm):
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


train_transform = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.3, 0.3, 0.3, 0.1),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

test_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class ImageAQIDataset(Dataset):
    def __init__(self, root_dir, split="train"):
        self.data = pd.read_csv(
            os.path.join(root_dir, split, "metadata.csv")
        )
        self.image_dir = os.path.join(root_dir, split, "images")
        self.transform = train_transform if split == "train" else test_transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]

        img_path = os.path.join(self.image_dir, row["filename"])
        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)

        pm_value = float(row["pm25"])
        label = pm_to_aqi_class(pm_value)

        return image, torch.tensor(label, dtype=torch.long)