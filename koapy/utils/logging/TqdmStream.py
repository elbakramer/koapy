import io
import tqdm

class TqdmStream(io.RawIOBase):

    def __init__(self, file=None):
        super().__init__()
        self._file = file

    def __getattr__(self, name):
        return getattr(self._file, name)

    def fileno(self):
        if self._file is None:
            raise OSError()
        return self._file.fileno()

    def seek(self, offset, whence=io.SEEK_SET):
        if self._file is None:
            raise OSError()
        return self._file.seek(offset, whence)

    def truncate(self):
        if self._file is None:
            raise OSError()
        return self._file.truncate()

    def write(self, b):
        if len(b.rstrip()) > 0:
            tqdm.tqdm.write(b, file=self._file, end='')
