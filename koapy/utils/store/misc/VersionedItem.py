class VersionedItem:
    def __init__(self, library, symbol, version, timestamp, data, metadata):
        self.library = library
        self.symbol = symbol
        self.version = version
        self.timestamp = timestamp
        self.data = data
        self.metadata = metadata

    def __repr__(self):
        return "<VersionedItem(library={!r}, symbol={!r}, version={!r}, timestamp='{}', data=<{}.{} at {}>, metadata={!r})>".format(
            self.library,
            self.symbol,
            self.version,
            self.timestamp,
            type(self.data).__module__,
            type(self.data).__name__,
            hex(id(self.data)),
            self.metadata,
        )
