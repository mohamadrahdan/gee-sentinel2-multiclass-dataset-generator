# GEE Sentinel-2 Multiclass Dataset Generator



[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/mohamadrahdan/gee-sentinel2-multiclass-dataset-generator/blob/main/notebooks/gee-s2-multiclass-dataset-generator.ipynb)



Generate tiled Sentinel-2 image chips and masks for multiclass hazard detection using Google Earth Engine.



---



## 🔹 Setup

Clone the repo:

```bash

git clone https://github.com/mohamadrahdan/gee-sentinel2-multiclass-dataset-generator.git

cd gee-sentinel2-multiclass-dataset-generator

python -m venv .venv && source .venv/bin/activate

pip install -r requirements.txt