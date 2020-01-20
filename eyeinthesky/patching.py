import numpy


def patches_around_positive_areas(mask, radius=256, max_walk=16):
    """Randomly yields a tuple of two slices marking a 2*`radius` x 2*`radius`
    area's containing at least some True `mask`-pixels at most `max_walk` pixels
    from the center. The areas may overlap and iteration stops if each positive
    pixel in mask was included in at least one of the yielded areas."""
    y, x = numpy.where(mask)
    #     x = numpy.minimum(numpy.maximum(x, radius), mask.shape[1] - radius)
    #     y = numpy.minimum(numpy.maximum(y, radius), mask.shape[0] - radius)

    while len(x) > 0:
        patch = numpy.random.choice(len(x), 1)[0]

        x_ = x[patch] + numpy.random.randint(-max_walk, max_walk + 1, 1)[0]
        y_ = y[patch] + numpy.random.randint(-max_walk, max_walk + 1, 1)[0]

        x_ = max(radius, min(mask.shape[1] - radius, x_))
        y_ = max(radius, min(mask.shape[0] - radius, y_))

        done = (numpy.abs(x - x_) <= radius) & (numpy.abs(y - y_) <= radius)
        x, y = x[~done], y[~done]

        yield (
            slice(y_ - radius, y_ + radius),
            slice(x_ - radius, x_ + radius)
        )


def take(it, n):
    """Return a list of the next `n` items in the generator `it`,
    or less if there aren't anymore."""
    return [x for _, x in zip(range(n), it)]


def batched_patches(mask, *args, batch_size=32, radius=256, max_walk=16):
    """Yield batches of `batch_size` patches from `patches_around_positive_areas`, until
    patches are done. The last batch will likely be smaller than `batch_size`. Each
    yield returns a tuple containing `batch_size` areas from `mask`, and the same areas
    for each of `args`. The numpy arrays are reused every yield."""
    def area_shape(x):
        return (batch_size, 2 * radius, 2 * radius) + x.shape[2:]

    M = numpy.zeros(area_shape(mask), dtype=mask.dtype)
    R = tuple(
        numpy.zeros(area_shape(arg), dtype=arg.dtype)
        for arg in args
    )

    it = patches_around_positive_areas(mask, radius=radius, max_walk=max_walk)

    while True:
        patches = take(it, batch_size)
        n_patches = len(patches)

        if n_patches == 0:
            break

        for i, patch in enumerate(patches):
            M[i] = mask[patch]
            for arg, r in zip(args, R):
                r[...] = arg[patch]
        yield (M, ) + R
