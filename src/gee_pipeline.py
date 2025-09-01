import ee
import json
import os


def init_ee(auth=True):
    """
    Start Google Earth Engine.
    auth=True → login first (needed in Colab/local the first time)
    """
    if auth:
        ee.Authenticate()
    ee.Initialize()
    print("Earth Engine ready.")


def load_region_from_geojson(path):
    """
    Load an AOI from a GeoJSON or Shapefile and convert to EE geometry.
    - If path is GeoJSON: reads directly
    - If path is Shapefile: convert to GeoJSON first (e.g., via geopandas)
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Region file not found: {path}")

    # Read GeoJSON
    if path.lower().endswith(".geojson") or path.lower().endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        # Convert to EE geometry
        region = ee.Geometry(geojson_data["features"][0]["geometry"])
        print(f"Loaded region from {path}")
        return region

    # Shapefile case: requires geopandas
    elif path.lower().endswith(".shp"):
        try:
            import geopandas as gpd
        except ImportError:
            raise ImportError("geopandas is required to read shapefiles. Install via: pip install geopandas")

        gdf = gpd.read_file(path)
        geojson_str = gdf.to_json()
        geojson_data = json.loads(geojson_str)
        region = ee.Geometry(geojson_data["features"][0]["geometry"])
        print(f"Loaded region from Shapefile {path}")
        return region

    else:
        raise ValueError("Unsupported file format. Use .geojson, .json, or .shp")
    

def get_s2_collection(region, start_date, end_date, cloud_max=10):
    """
    Get Sentinel-2 SR images for a region and date range.
    Filters by CLOUDY_PIXEL_PERCENTAGE ≤ cloud_max.
    """
    coll = (ee.ImageCollection("COPERNICUS/S2_SR")
            .filterBounds(region)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_max)))
    
    print(f"Found {coll.size().getInfo()} images.")
    return coll
