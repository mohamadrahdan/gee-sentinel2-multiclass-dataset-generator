import os
from pathlib import Path
import yaml

def load_config(path="configs/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def get_output_dir(cfg):
    return os.getenv("OUTPUT_DIR", cfg.get("output_dir", "./outputs"))
