import sys

from logging import StreamHandler

from tqdm.contrib import DummyTqdmFile


class TqdmStreamHandler(StreamHandler):
    def __init__(self, stream=None):
        if stream is None:
            stream = sys.stderr
        stream = DummyTqdmFile(stream)
        StreamHandler.__init__(self, stream)
