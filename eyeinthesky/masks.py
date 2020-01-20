import cv2
import numpy
import shapely.geometry


def iter_exteriors(shp):
    if isinstance(shp, shapely.geometry.MultiPolygon):
        for geom in shp.geoms:
            yield geom.exterior
    elif isinstance(shp, shapely.geometry.Polygon):
        yield shp.exterior
    else:
        raise ValueError(f'Don\'t know how to deal with type {type(shp)}, '
                         'only shapely.geometry.Polygon and '
                         'shapely.geometry.MultiPolygon are supported.')


def draw_mask(mask_shape, geojson):
    mask = numpy.zeros(mask_shape, numpy.uint8)

    for feature in geojson['features']:
        for ext in iter_exteriors(shapely.geometry.shape(feature['geometry'])):
            xs, ys = map(numpy.array, ext.xy)
            pts = numpy.round(numpy.concatenate([
                xs[None, :, None],
                ys[None, :, None]
            ], axis=2)).astype(numpy.int64)

            cv2.fillPoly(mask, pts, 1)
    return mask


def iter_exteriors(shp):
    if isinstance(shp, shapely.geometry.MultiPolygon):
        for geom in shp.geoms:
            yield geom.exterior
    elif isinstance(shp, shapely.geometry.Polygon):
        yield shp.exterior
    else:
        raise ValueError(f'Don\'t know how to deal with type {type(shp)}, '
                         'only shapely.geometry.Polygon and '
                         'shapely.geometry.MultiPolygon are supported.')


def draw_mask(mask_shape, geojson):
    mask = numpy.zeros(mask_shape, numpy.uint8)

    for feature in geojson['features']:
        for ext in iter_exteriors(shapely.geometry.shape(feature['geometry'])):
            xs, ys = map(numpy.array, ext.xy)
            pts = numpy.round(numpy.concatenate([
                xs[None, :, None],
                ys[None, :, None]
            ], axis=2)).astype(numpy.int64)

            cv2.fillPoly(mask, pts, 1)
    return mask
