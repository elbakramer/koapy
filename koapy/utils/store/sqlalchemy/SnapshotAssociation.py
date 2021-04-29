from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .Base import Base


class SnapshotAssociation(Base):
    __tablename__ = "snapshot_associations"

    snapshot_id = Column(Integer, ForeignKey("snapshots.id"), primary_key=True)
    version_id = Column(Integer, ForeignKey("versions.id"), primary_key=True)

    snapshot = relationship("Snapshot", back_populates="versions")
    version = relationship("Version", back_populates="snapshots")
