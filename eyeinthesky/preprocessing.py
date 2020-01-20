import numpy


def preprocess_input(image):
    offsets = numpy.array([
        1264.06439133,  993.71959535,  879.00178412,  740.15150524,  990.24213408,
        1798.24382807, 2154.90345801, 2121.7030217 ,  695.56159991,   11.36244131,
        1707.93913123, 1008.18696351])
    factors = numpy.array([
         92.55388916, 139.58717587, 193.49003888, 319.68365431, 317.27768991,
        444.25386892, 565.17997105, 593.66462148, 160.98605446,   2.23359842,
        631.6088602 , 520.73160082])

    image -= offsets[(numpy.newaxis, ) * (len(image.shape) - 1)]
    for i, f in enumerate(factors):
        image[..., i] /= f

    numpy.clip(image, -2, 2, image)
    return image
