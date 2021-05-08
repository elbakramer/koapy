import pandas as pd

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import aliased, object_session, relationship
from sqlalchemy.orm.exc import NoResultFound

from .Base import Base
from .SnapshotAssociation import SnapshotAssociation
from .Version import Version


class Symbol(Base):
    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)

    library_id = Column(Integer, ForeignKey("libraries.id"), nullable=False)
    library = relationship("Library", back_populates="symbols")

    versions = relationship(
        "Version", back_populates="symbol", order_by="Version.version"
    )

    __table_args__ = (UniqueConstraint("library_id", "name"),)

    def get_versions(self, deleted=False):
        """
        versions = self.versions
        if not deleted:
            versions = [version for version in versions if not version.deleted]
        """
        session = object_session(self)
        versions = session.query(Version).with_parent(self)
        version = aliased(Version, alias=versions.subquery())
        versions = session.query(version)
        if not deleted:
            versions = versions.filter(version.deleted != True)
        versions = versions.order_by(version.version)
        versions = versions.all()
        return versions

    def get_latest_version(self, deleted=False):
        """
        versions = self.versions
        if len(versions) == 0:
            raise NoResultFound
        latest_version = self.versions[-1]
        if not deleted and latest_version.deleted:
            raise NoResultFound
        """
        session = object_session(self)
        latest_version = session.query(Version, func.max(Version.version)).with_parent(
            self
        )
        version = aliased(Version, alias=latest_version.subquery())
        latest_version = session.query(version)
        if not deleted:
            latest_version = latest_version.filter(version.deleted != True)
        latest_version = latest_version.one()
        return latest_version

    def create_new_version(
        self, table_name=None, user_metadata=None, pandas_metadata=None, deleted=None
    ):
        try:
            latest_version = self.get_latest_version()
        except NoResultFound:
            next_version = 0
        else:
            next_version = latest_version.version + 1
        new_version = Version(
            version=next_version,
            table_name=table_name,
            user_metadata=user_metadata,
            pandas_metadata=pandas_metadata,
            deleted=deleted,
        )
        self.versions.append(new_version)
        return new_version

    def get_version_by_number(self, version_number, deleted=False):
        session = object_session(self)
        version = (
            session.query(Version)
            .with_parent(self)
            .filter(Version.version == version_number)
        )
        if not deleted:
            version = version.filter(Version.deleted != True)
        version = version.one()
        return version

    def get_prunable_versions(self, keep_mins=120):
        session = object_session(self)
        versions = session.query(Version).with_parent(self)
        latest_version = self.get_latest_version(deleted=True)
        keep_mins_seconds = keep_mins * 60
        latest_timestamp = latest_version.timestamp
        oldest_timestamp = latest_timestamp - pd.Timedelta(keep_mins_seconds, unit="s")
        prunable_verions = (
            versions.outerjoin(SnapshotAssociation)
            .filter(SnapshotAssociation.version_id == None)
            .filter(Version.timestamp < oldest_timestamp)
        )
        prunable_verions = prunable_verions.all()
        return prunable_verions
