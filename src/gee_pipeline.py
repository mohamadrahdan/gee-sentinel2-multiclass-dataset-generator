import ee
import json
import os
from src.utils import resolve_input

def init_ee(auth=True):
    """
    Start Google Earth Engine.
    auth=True → login first (needed in Colab/local the first time)
    """
    if auth:
        ee.Authenticate()
    ee.Initialize()
    print("Earth Engine ready.")

def get_s2_collection(region, start_date, end_date, cloud_max=10):
    """
    Get Sentinel-2 SR (COPERNICUS/S2_SR) filtered by ROI/date/clouds.
    """
    coll = (ee.ImageCollection("COPERNICUS/S2_SR")
            .filterBounds(region)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_max)))
    print(f"Found {coll.size().getInfo()} images.")
    return coll

# Vectors: loader and converter
def _read_vector_any(path):
    """
    Read vector from GeoJSON/JSON/SHP/ZIP.
    Paths are resolved against DATA_ROOT if relative.
    Returns a GeoJSON dict (FeatureCollection).
    """
    path = resolve_input(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Vector file not found: {path}")

    lower = path.lower()
    if lower.endswith((".geojson", ".json")):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # SHP/ZIP via geopandas
    try:
        import geopandas as gpd
    except ImportError:
        raise ImportError("geopandas is required for SHP/ZIP. Install: pip install geopandas")

    if lower.endswith(".zip"):
        gdf = gpd.read_file(f"zip://{path}")  # zipped shapefile
    elif lower.endswith(".shp"):
        gdf = gpd.read_file(path)
    else:
        raise ValueError("Unsupported vector format. Use .geojson/.json/.shp/.zip")

    return json.loads(gdf.to_json())

def gdf_to_ee_fc(geojson_dict, expected="polygon"):
    """
    Convert a GeoJSON FeatureCollection to ee.FeatureCollection.
    """
    feats = geojson_dict.get("features", [])
    if not feats:
        raise ValueError("Empty GeoJSON (no features).")
    ee_feats = [ee.Feature(ee.Geometry(f["geometry"]), f.get("properties", {})) for f in feats]
    print(f"Loaded {len(ee_feats)} {expected}(s) → EE FeatureCollection")
    return ee.FeatureCollection(ee_feats)

def load_boundary_fc(path):
    """
    Load AOI boundary (GeoJSON/SHP/ZIP) → ee.FeatureCollection.
    """
    gj = _read_vector_any(path)
    return gdf_to_ee_fc(gj, expected="polygon")

def load_classes(cfg):
    """
    Load class vectors from config:
      returns list of (name, class_id, ee.FeatureCollection)
    """
    out = []
    for item in cfg.get("classes", []):
        gj = _read_vector_any(item["path"])
        fc = gdf_to_ee_fc(gj, expected="polygon")
        out.append((item["name"], int(item["class_id"]), fc))
        print(f"Class '{item['name']}' (id={item['class_id']}) ready.")
    return out

def make_class_mask(classes_list, boundary_fc, scale=10):
    """
    Paint classes into a single-band label image
    Pixel value = class_id (0 = background). Last class wins on overlaps.
    """
    mask = ee.Image(0).byte()
    boundary = ee.FeatureCollection(boundary_fc).geometry()
    for (name, cid, fc) in classes_list:
        painted = ee.Image().byte().paint(fc, cid)
        mask = mask.where(painted.gt(0), painted)
    return mask.clip(boundary)
