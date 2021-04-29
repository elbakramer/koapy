from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    PickleType,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import object_session, relationship
from sqlalchemy.schema import DropTable, MetaData, Table
from sqlalchemy.sql.functions import current_timestamp

from .Base import Base
from .Timestamp import Timestamp


class Version(Base):
    __tablename__ = "versions"

    id = Column(Integer, primary_key=True)
    version = Column(Integer, nullable=False)

    table_name = Column(String)
    user_metadata = Column(PickleType)
    pandas_metadata = Column(PickleType)

    deleted = Column(Boolean, default=False)

    timestamp = Column(Timestamp(timezone=True), server_default=current_timestamp())

    symbol_id = Column(Integer, ForeignKey("symbols.id"))
    symbol = relationship("Symbol", back_populates="versions")

    snapshots = relationship("SnapshotAssociation", back_populates="version")

    __table_args__ = (UniqueConstraint("symbol_id", "version"),)

    def get_snapshots(self):
        # quick fix fir circular dependency
        from .Snapshot import Snapshot
        from .SnapshotAssociation import SnapshotAssociation

        session = object_session(self)
        snapshots = session.query(SnapshotAssociation).with_parent(self)
        snapshots = session.query(Snapshot).join(snapshots.subquery())
        snapshots = snapshots.all()
        return snapshots

    def delete(self):
        session = object_session(self)
        if self.table_name is not None:
            table_reference_count = (
                session.query(Version)
                .filter(Version.table_name == self.table_name)
                .count()
            )
            if table_reference_count <= 1:
                session.execute(
                    DropTable(Table(self.table_name, MetaData()), if_exists=True)
                )
        session.delete(self)
