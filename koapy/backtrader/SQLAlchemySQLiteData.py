from .SQLAlchemyData import SQLAlchemyData


class SQLAlchemySQLiteData(SQLAlchemyData):

    # pylint: disable=no-member

    params = (("filename", None),)

    def __init__(self):
        if not self.p.url:
            self.p.url = "sqlite://"

            if self.p.filename:
                self.p.url += "/" + self.p.filename

        super().__init__()
