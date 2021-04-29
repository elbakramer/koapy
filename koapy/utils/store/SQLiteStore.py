from sqlalchemy import create_engine, inspect

from .sqlalchemy.Base import Base
from .sqlalchemy.Library import Library
from .sqlalchemy.Session import Session
from .SQLiteStoreLibrary import SQLiteStoreLibrary


class SQLiteStore:
    def __init__(self, filename):
        self._filename = filename
        self._engine = create_engine("sqlite:///" + self._filename)

        Session.configure(bind=self._engine)

        inspector = inspect(self._engine)
        table_names = inspector.get_table_names()

        if len(table_names) == 0:
            Base.metadata.create_all(self._engine)
            inspector = inspect(self._engine)
            table_names = inspector.get_table_names()

        assert all(table_name in table_names for table_name in Base.metadata.tables)

        self._session = Session()
        self._library_cache = {}

    def list_libraries(self):
        libraries = self._session.query(Library).all()
        libraries = [library.name for library in libraries]
        return libraries

    def _get_library(self, library):
        library = self._session.query(Library).filter(Library.name == library).one()
        return library

    def library_exists(self, library):
        try:
            _library = self._get_library(library)
            return True
        except:
            return False

    def initialize_library(self, library):
        library_name = library
        if not self.library_exists(library_name):
            library = Library(name=library_name)
            try:
                self._session.add(library)
                self._session.commit()
            except:
                self._session.rollback()
                raise

    def get_library(self, library):
        library_name = library
        if library_name in self._library_cache:
            return self._library_cache[library_name]
        library = self._get_library(library)
        library = SQLiteStoreLibrary(self, library)
        self._library_cache[library_name] = library
        return library

    def get_or_create_library(self, library):
        if not self.library_exists(library):
            self.initialize_library(library)
        library = self.get_library(library)
        return library

    def delete_library(self, library):
        library_name = library
        library = self._get_library(library_name)
        try:
            library.delete()
            self._session.commit()
        except:
            self._session.rollback()
            raise

    def __getitem__(self, library):
        return self.get_library(library)
