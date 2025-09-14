# GEE Sentinel-2 Multiclass Dataset Generator



[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mohamadrahdan/gee-sentinel2-multiclass-dataset-generator/blob/main/notebooks/gee-s2-multiclass-dataset-generator.ipynb)



Generate tiled Sentinel-2 image chips and masks for multiclass hazard detection using Google Earth Engine (GEE).


## Features

- **Load AOI (boundary) and multiple class shapefiles (GeoJSON, SHP , or zipped SHP)**
- **Fetch Sentinel-2 SR imagery with cloud filtering**
- **Generate per-tile image chips and masks with class_id labels**
- **Export tiles in batch to Google Drive (or Kaggle, optional)**
- **Configurable pipeline via configs/config.yaml**


## Setup

- **Clone the repository**
  ```bash
  git clone https://github.com/mohamadrahdan/gee-sentinel2-multiclass-dataset-generator.git
  
  cd gee-sentinel2-multiclass-dataset-generator

  python -m venv .venv && source .venv/bin/activate

  pip install -r requirements.txt


## Private Inputs (AOI + Classes)

- **Provide your own shapefiles** for the boundary and hazard classes.  
  Do not put these inside the repo (they’re private).  

- **Place them in a private folder**, for example:
  D:/hazard-data/areakomeh.zip
  D:/hazard-data/landslides_merged.zip
  D:/hazard-data/PseudoLandslides_merged.zip
  D:/hazard-data/NonLandslides_merged.zip

