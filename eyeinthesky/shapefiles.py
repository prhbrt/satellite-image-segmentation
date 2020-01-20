import cv2
import numbers

import shapefile

import shapely.geometry
from shapely.geometry import shape, box
from shapely.ops import cascaded_union

from skimage.io import imread, imsave
import rasterio, rasterio.features, rasterio.warp, rasterio.crs

def shapefile_to_geojson(filename, transform=None):
    """Load the geojson and potentially transform the coordinates using transform, which
    goes from a list of (x,y) coordinates to a list of (x,y) coordinates in a new coordinate
    system. Or no transformation if is None."""
    shape_file = shapefile.Reader(filename)
    fields = shape_file.fields[1:]
    field_names = [field[0] for field in fields]
    features = []

    def transform_poly(poly):
        if all(
            len(item) == 2 and all(
                isinstance(item, numbers.Number) for item in item)
            for item in poly
        ):
            return transform(poly)
        return list(map(transform, poly))

    for shape_record in shape_file.shapeRecords():
        properties = dict(zip(field_names, shape_record.record))
        geometry = shape_record.shape.__geo_interface__
        if transform is not None:
            geometry['coordinates'] = transform_poly(geometry['coordinates'])

        features.append({
            'type': "Feature",
            'geometry': geometry,
            'properties': properties
        })
    return {
        "type": "FeatureCollection",
        "features": features
    }


def shapefile_to_pixel_geojson(image_filename, label_filename):
    """Transforms a shapefile into a geojson with coordinate's
    in pixel locations of the geotiff in `image_filename`."""
    with rasterio.open(image_filename) as dataset:
    # for translation between the tif-file coordinate system to pixels
        coordinate_to_pixel = ~dataset.transform

    # for translation between lat/lon's to the coordinate system in the tif-file.
    src_crs, dst_crs = dataset.crs, rasterio.crs.CRS.from_epsg(4326)

    def transform(poly):
        return [
            (x, y)  * coordinate_to_pixel
            for x, y in zip(
                *rasterio.warp.transform(dst_crs, src_crs, *zip(*poly)))
        ]

    return shapefile_to_geojson(label_filename, transform=transform)
