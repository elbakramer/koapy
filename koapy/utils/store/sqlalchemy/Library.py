from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import aliased, object_session, relationship
from sqlalchemy.orm.exc import NoResultFound

from .Base import Base
from .Snapshot import Snapshot
from .SnapshotAssociation import SnapshotAssociation
from .Symbol import Symbol
from .Version import Version


class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)

    symbols = relationship("Symbol", back_populates="library")
    snapshots = relationship("Snapshot", back_populates="library")

    def get_symbol(self, symbol, deleted=False):
        symbol_name = symbol
        session = object_session(self)
        symbol = (
            session.query(Symbol).with_parent(self).filter(Symbol.name == symbol_name)
        )
        symbol = symbol.one()
        if not deleted:
            _version = symbol.get_latest_version()
        return symbol

    def get_or_create_symbol(self, symbol):
        symbol_name = symbol
        try:
            symbol = self.get_symbol(symbol_name, deleted=True)
        except NoResultFound:
            symbol = Symbol(name=symbol_name)
            self.symbols.append(symbol)
        return symbol

    def get_symbols(self, deleted=False):
        if deleted:
            return self.symbols

        session = object_session(self)

        symbols = session.query(Symbol).with_parent(self)

        versions = session.query(Version, func.max(Version.version)).group_by(
            Version.symbol_id
        )
        version = aliased(Version, alias=versions.subquery())
        versions = session.query(version)

        if not deleted:
            versions = versions.filter(version.deleted != True)

        symbols = symbols.join(versions.subquery())
        symbols = symbols.all()
        return symbols

    def get_versions(self, deleted=False):
        session = object_session(self)

        symbols = session.query(Symbol).with_parent(self)
        versions = session.query(Version).join(symbols.subquery())

        if not deleted:
            versions = versions.filter(Version.deleted != True)

        versions = versions.all()
        return versions

    def get_latest_versions(self, deleted=False):
        session = object_session(self)

        symbols = session.query(Symbol).with_parent(self)

        versions = session.query(Version, func.max(Version.version)).group_by(
            Version.symbol_id
        )
        version = aliased(Version, alias=versions.subquery())
        versions = session.query(version)

        if not deleted:
            versions = versions.filter(version.deleted != True)

        versions = versions.join(symbols.subquery())
        versions = versions.all()
        return versions

    def get_snapshot(self, snapshot):
        snapshot_name = snapshot
        session = object_session(self)
        snapshot = (
            session.query(Snapshot)
            .with_parent(self)
            .filter(Snapshot.name == snapshot_name)
            .one()
        )
        return snapshot

    def create_snapshot(self, snapshot):
        snapshot_name = snapshot
        snapshot = Snapshot(name=snapshot_name)

        versions = self.get_latest_versions()
        associations = [SnapshotAssociation(version=version) for version in versions]
        snapshot.versions.extend(associations)

        self.snapshots.append(snapshot)
        return snapshot

    def delete(self):
        session = object_session(self)

        symbols = session.query(Symbol).with_parent(self)
        versions = session.query(Version).join(symbols)

        snapshots = session.query(Snapshot).with_parent(self)
        associations = session.query(SnapshotAssociation).join(snapshots)

        associations.delete()
        snapshots.delete()

        versions.delete()
        symbols.delete()

        session.delete(self)
