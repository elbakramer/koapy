import itertools

def chunk(iterable, n):
    fillvalue = object()
    args = [iter(iterable)] * n
    it = itertools.zip_longest(fillvalue=fillvalue, *args)
    it = map(lambda items: [item for item in items if item is not fillvalue], it)
    return it
