from collections.abc import Iterator

from grpc._channel import _MultiThreadedRendezvous as MultiThreadedRendezvous


class PipeableStream(Iterator):
    def __init__(self, stream, generator=None):
        super().__init__()
        self._stream = stream
        self._iterator = generator or self._stream
        assert isinstance(self._stream, MultiThreadedRendezvous)
        assert isinstance(self._iterator, Iterator)

    def __next__(self):
        return self._iterator.__next__()

    def pipe(self, func):
        stream = self._stream
        generator = func(self._stream)
        return type(self)(stream, generator)

    def __getattr__(self, name):
        try:
            return getattr(self._stream, name)
        except AttributeError:
            return getattr(self._iterator, name)
