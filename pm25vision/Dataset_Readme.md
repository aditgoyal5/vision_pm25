# PM25Vision

## Dataset Summary
PM25Vision (PM25V) is a large-scale dataset for estimating air quality (PM2.5) from street-level imagery. It pairs **Mapillary** photos with **World Air Quality Index (WAQI)** PM2.5 records, covering 2014–2025, 3,261 monitoring stations, and 11,114 cleaned and balanced images.

## Tasks
- **Regression**: Predict continuous PM2.5 **AQI** values.  
- **Classification**: Predict discrete AQI levels.

## Baseline Results
### Regression
| Model           | R²   | MAE  | RMSE | Acc  | F1   |
|-----------------|------|------|------|------|------|
| EfficientNet-B0 | 0.55 | 36.6 | 54.6 | 0.46 | 0.45 |
| ResNet50        | 0.50 | 38.6 | 57.5 | 0.44 | 0.35 |
| ViT-B/16        | 0.23 | 50.3 | 71.7 | 0.35 | 0.30 |

### Classification
| Model           | Acc  | F1   | Precision | Recall |
|-----------------|------|------|-----------|--------|
| ResNet50        | 0.44 | 0.38 | 0.48      | 0.37   |
| ViT-B/16        | 0.40 | 0.37 | 0.41      | 0.36   |
| EfficientNet-B0 | 0.40 | 0.34 | 0.42      | 0.33   |

## Dataset Structure

The dataset is organized into two main splits: **train** and **test**, each containing:

- **`images/`**: all image files used in the dataset.  
- **`samples_by_bin/`**: a small set of 30 example images per AQI bin (for quick visual inspection).  
- **`metadata.csv`**: a CSV file describing metadata (including pm2.5 labels) for each image.  

### Metadata Fields

Each row in `metadata.csv` contains:

| Field          | Type    | Description                                                          |
|----------------|---------|----------------------------------------------------------------------|
| `**image_id**` | int64   | Unique image identifier (from Mapillary).                            |
| `station_id`   | int64   | WAQI monitoring station ID.                                          |
| `captured_at`  | object  | Date when the image was captured (YYYY-MM-DD).                       |
| `camera_angle` | float64 | Camera orientation (if available).                                   |
| `longitude`    | float64 | Longitude of the station.                                            |
| `latitude`     | float64 | Latitude of the station.                                             |
| `quality_score`| float64 | Image quality score from Mapillary (if available).                   |
| `downloaded_at`| object  | Timestamp when the sample was downloaded.                            |
| `**pm25**`     | float64 | Average PM2.5 AQI value of the day that the image was captured.      |
| `filename`     | object  | Image filename, located in the `images/` directory.                  |
| `quality`      | object  | ResNet18 classified label for image quality (e.g., `good` or `bad`). |
| `pm25_bin`     | object  | Discrete AQI level label (e.g., `0–50`, `51–100`, etc.).             |

### Splits

- **Train**: 80% of samples, balanced across AQI bins.  
- **Test**: 20% of samples, balanced across AQI bins.  


## Limitations
- WAQI temporal resolution is **daily**, may miss intra-day variation.  
- Spatial accuracy limited to 5 km around stations.  
- Rare extreme AQI classes remain underrepresented.

## Access
- Arxiv: ...
- Online demo: [pm25vision.com](http://www.pm25vision.com)

## Citation
```bibtex
@misc{pm25vision2025,
  title        = {PM25Vision: Street-level imagery with PM2.5 annotations},
  author       = {Han, Yang},
  year         = {2025},
  publisher    = {Hugging Face Datasets},
  url          = {https://huggingface.co/datasets/DeadCardassian/PM25Vision}
}
```