import ee

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
    Get Sentinel-2 SR images for a region and date range.
    Filters by CLOUDY_PIXEL_PERCENTAGE ≤ cloud_max.
    """
    coll = (ee.ImageCollection("COPERNICUS/S2_SR")
            .filterBounds(region)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", cloud_max)))
    
    print(f"Found {coll.size().getInfo()} images.")
    return coll
