import os


def listdir_withoutextension(folder, ext):
    return {
        fn[:-len(ext) - 1]
        for fn in os.listdir(folder)
        if fn.endswith(f'.{ext}')
    }


def get_samples(sources, destinations):
    """Returns an iterator over sample names (without extensions) for
    all (extension, folder) tuples in `sources`. The iterator returns tuples
    of 
     - the sample name,
     - each path leading to that sample for all `sources`, and
     - each path leading to a sample to be created in `destinations`."""
    if len(sources) > 0:
        r = listdir_withoutextension(sources[0][1], sources[0][0])
        u = r
        for ext, folder in sources[1:]:
            n = listdir_withoutextension(folder, ext)
            r = r & n
            u = u | n
    else:
        r, u = set(), set()

    if len(u - r) > 0:
        print(f'{len(r)} out of {len(u)} ({int(100 * len(r) / len(u) + 0.5):d}%) samples were in all folders.')
        print(f'Incomplete samples: {"; ".join(u - r)}')
    else:
        print(f'All samples were in all folders.')

    class it:
        def __iter__(self):
            for sample in r:
                yield (sample,) + tuple(
                    f'{folder}/{sample}.{ext}'
                    for ext, folder in sources
                ) + tuple(
                    f'{folder}/{sample}.{ext}'
                    for ext, folder in destinations
                )

        def __len__(self):
            return len(r)

    return it()
