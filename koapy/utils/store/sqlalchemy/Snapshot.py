from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import object_session, relationship
from sqlalchemy.sql.functions import current_timestamp

from .Base import Base
from .SnapshotAssociation import SnapshotAssociation
from .Symbol import Symbol
from .Timestamp import Timestamp
from .Version import Version


class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)

    timestamp = Column(Timestamp(timezone=True), server_default=current_timestamp())

    library_id = Column(Integer, ForeignKey("libraries.id"), nullable=False)
    library = relationship("Library", back_populates="snapshots")

    versions = relationship("SnapshotAssociation", back_populates="snapshot")

    __table_args__ = (UniqueConstraint("library_id", "name"),)

    def get_symbols(self):
        session = object_session(self)
        associations = session.query(SnapshotAssociation).with_parent(self)
        versions = session.query(Version).join(associations.subquery())
        symbols = session.query(Symbol).join(versions.subquery())
        symbols = symbols.all()
        return symbols

    def get_versions(self):
        session = object_session(self)
        associations = session.query(SnapshotAssociation).with_parent(self)
        versions = session.query(Version).join(associations.subquery())
        versions = versions.all()
        return versions

    def get_version_of_symbol(self, symbol):
        session = object_session(self)
        if isinstance(symbol, str):
            symbol = (
                session.query(Symbol)
                .filter(Symbol.library_id == self.library_id and Symbol.name == symbol)
                .one()
            )
        associations = session.query(SnapshotAssociation).with_parent(self)
        version = (
            session.query(Version)
            .with_parent(symbol)
            .join(associations.subquery())
            .one()
        )
        return version

    def delete(self):
        session = object_session(self)
        associations = session.query(SnapshotAssociation).with_parent(self)
        associations.delete()
        session.delete(self)
