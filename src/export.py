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

