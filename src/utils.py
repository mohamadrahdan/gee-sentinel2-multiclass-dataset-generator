import os
from pathlib import Path
import yaml

def load_config(path="configs/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def get_data_root():
    """
    Private input folder (not in Git).
    Set DATA_ROOT in your environment:
      Local:  DATA_ROOT=D:/hazard-data
      Colab:  DATA_ROOT=/content/drive/MyDrive/hazard-data
    """
    return os.getenv("DATA_ROOT", "./data")  # ./data is in .gitignore

def resolve_input(path_like):
    """
    Resolve path against DATA_ROOT if relative.
    """
    p = Path(path_like)
    if p.is_absolute():
        return str(p)
    return str((Path(get_data_root()) / path_like).resolve())

def get_output_dir(cfg):
    return os.getenv("OUTPUT_DIR", cfg.get("output_dir", "./outputs"))