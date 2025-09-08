import ee

# get a python list of first N tile geometries
def _take_tile_geoms(tiles_fc, max_n=None):
    """
    Pull first N features (geometries) client-side for exporting.
    Warning: for very large collections, keep N reasonable.
    """
    size = ee.Number(tiles_fc.size())
    n = size if max_n is None else ee.Number(min(max_n, size.getInfo()))
    lst = tiles_fc.toList(n)  # server list
    out = []
    for i in range(int(n.getInfo())):
        f = ee.Feature(lst.get(i))
        out.append(f.geometry())
    return out

def export_tiles_to_drive(mosaic_image, label_mask_image, tiles_fc, cfg):
    """
    Batch-export images + masks per tile to Google Drive.
    One export task per tile (image+ mask).
    """
    exp = cfg.get("export", {})
    drive_folder= exp.get("drive_folder", "gee_s2_multiclass")
    img_prefix= exp.get("image_prefix", "img_")
    mask_prefix= exp.get("mask_prefix", "mask_")
    fmt= exp.get("format", "GEO_TIFF")
    scale = exp.get("scale",10)
    max_tiles = exp.get("max_tiles",200)

    # Pull a reasonable number of tiles client-side
    geoms = _take_tile_geoms(tiles_fc, max_n=max_tiles)
    print(f"Will export up to {len(geoms)} tiles to Drive → {drive_folder}")

    tasks = []
    for idx, geom in enumerate(geoms):
        img_name = f"{img_prefix}{idx:05d}"
        mask_name = f"{mask_prefix}{idx:05d}"

        # Clip per-tile
        img = mosaic_image.clip(geom)
        mask = label_mask_image.clip(geom)

        # Create export tasks
        t_img = ee.batch.Export.image.toDrive(
            image=img,
            description=img_name,
            folder=drive_folder,
            fileNamePrefix=img_name,
            scale=scale,
            region=geom,
            fileFormat=fmt
        )
        t_mask = ee.batch.Export.image.toDrive(
            image=mask,
            description=mask_name,
            folder=drive_folder,
            fileNamePrefix=mask_name,
            scale=scale,
            region=geom,
            fileFormat=fmt
        )
        t_img.start()
        t_mask.start()
        tasks.append((img_name, t_img.status()))
        tasks.append((mask_name, t_mask.status()))

    print("Export tasks started. Track progress in the EE Tasks tab or Console.")
    return tasks  # statuses snapshot
