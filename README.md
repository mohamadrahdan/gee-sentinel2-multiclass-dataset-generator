# GEE Sentinel-2 Multiclass Dataset Generator



[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mohamadrahdan/gee-sentinel2-multiclass-dataset-generator/blob/main/notebooks/gee-s2-multiclass-dataset-generator.ipynb)



Generate tiled Sentinel-2 image chips and masks for multiclass hazard detection using Google Earth Engine (GEE).


🔹 Features

Load AOI (boundary) + multiple class shapefiles (GeoJSON, SHP, or zipped SHP)

Fetch Sentinel-2 SR imagery with cloud filtering

Generate per-tile image chips + masks (class_id labels)

Export tiles in batch to Google Drive (or Kaggle, optional)

Modular, configurable via configs/config.yaml
