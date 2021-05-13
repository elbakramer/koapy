from collections.abc import Iterator

from grpc._channel import _MultiThreadedRendezvous as MultiThreadedRendezvous


class PipeableMultiThreadedRendezvous(Iterator):
    def __init__(self, rendezvous, iterator=None):
        super().__init__()
        self._rendezvous = rendezvous
        self._iterator = iterator or self._rendezvous
        assert isinstance(self._rendezvous, MultiThreadedRendezvous)
        assert isinstance(self._iterator, Iterator)

    def __next__(self):
        return self._iterator.__next__()

    def pipe(self, func):
        rendezvous = self._rendezvous
        iterator = func(self._iterator)
        return type(self)(rendezvous, iterator)

    def __getattr__(self, name):
        try:
            return getattr(self._rendezvous, name)
        except AttributeError:
            return getattr(self._iterator, name)
