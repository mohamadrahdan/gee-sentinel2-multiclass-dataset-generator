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
  - `D:/hazard-data/areakomeh.zip`
  - `D:/hazard-data/landslides_merged.zip`
  - `D:/hazard-data/PseudoLandslides_merged.zip`
  - `D:/hazard-data/NonLandslides_merged.zip`

- **Set the environment variable `DATA_ROOT`** to that folder:

  - Windows (PowerShell):
    ```powershell
    setx DATA_ROOT "D:\hazard-data"
    ```

  - Linux/macOS:
    ```bash
    export DATA_ROOT=/Users/me/hazard-data
    ```

  - Google Colab:
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    import os
    os.environ["DATA_ROOT"] = "/content/drive/MyDrive/hazard-data"
    ```


## Config File (configs/config.yaml)

- **Example configuration:**
  ```yaml
  output_dir: "./outputs"

  boundary_path: "areakomeh.zip"
  classes:
    - { name: "landslide",        path: "landslides_merged.zip",       class_id: 1 }
    - { name: "pseudo_landslide", path: "PseudoLandslides_merged.zip", class_id: 2 }
    - { name: "non_landslide",    path: "NonLandslides_merged.zip",    class_id: 3 }

  start_date: "2024-01-01"
  end_date: "2024-12-31"
  cloud_max: 10

  tile_size: 256
  bands: ["B02","B03","B04","B08"]

  output_destination: "local"   # local | drive | kaggle
  kaggle_dataset_slug: "mohamadrahdan/gee-s2-multiclass"

  export:
    drive_folder: "gee_s2_multiclass"
    image_prefix: "img_"
    mask_prefix: "mask_"
    format: "GEO_TIFF"
    scale: 10
    max_tiles: 200


## Run the Pipeline

- **Local usage**

  > Make sure to activate your virtual environment and set `DATA_ROOT` first.

  ```bash
  jupyter notebook notebooks/gee-s2-multiclass-dataset-generator.ipynb


Google Colab

Click the "Open in Colab" badge above.

Mount your Drive, set DATA_ROOT, and run the cells.