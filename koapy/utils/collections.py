import collections

class ChainList(collections.abc.Sequence):

    def __init__(self, lists):
        self._lists = lists

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                key = len(self) + key
            if key < 0:
                raise IndexError
            i = 0
            j = key
            l = len(self._lists[i])
            while j >= l:
                j -= l
                i += 1
            return self._lists[i][j]
        elif isinstance(key, slice):
            if key.step == 0:
                raise ValueError
            lst = []
            i = 0
            s = 0
            start = key.start or 0
            stop = key.stop or 0 + len(self)
            step = key.step or 1
            if step < 0:
                start = key.start or -1
                stop = key.stop or -1 - len(self)
            if start < 0:
                start = len(self) + start
            if stop < 0:
                stop = len(self) + stop
            rng = range(start, stop, step)
            if step < 0:
                rng = reversed(rng)
            for k in rng:
                j = k - s
                l = len(self._lists[i])
                while j >= l:
                    j -= l
                    s += l
                    i += 1
                    l = len(self._lists[i])
                lst.append(self._lists[i][j])
            if step < 0:
                lst = list(reversed(lst))
            return lst
        elif isinstance(key, tuple):
            if len(key) != 2:
                raise TypeError
            i, j = key
            return self._lists[i][j]
        else:
            raise TypeError

    def __len__(self):
        return sum(len(l) for l in self._lists)
