import datetime
import inspect

import pytz

from sqlalchemy import DateTime
from sqlalchemy.types import TypeDecorator


class Timestamp(TypeDecorator):  # pylint: disable=abstract-method

    impl = DateTime
    signature = inspect.signature(impl)

    utc = datetime.timezone.utc
    local_timezone = datetime.datetime.now().astimezone().tzinfo

    def __init__(self, *args, **kwargs):
        self._timezone = self.local_timezone
        bound = self.signature.bind(*args, **kwargs)
        bound.apply_defaults()
        if bound.arguments["timezone"]:
            if not isinstance(bound.arguments["timezone"], bool):
                self._timezone = bound.arguments["timezone"]
                bound.arguments["timezone"] = True
                if isinstance(self._timezone, str):
                    self._timezone = pytz.timezone(self._timezone)
        super().__init__(*bound.args, **bound.kwargs)

    @classmethod
    def is_naive(cls, value):
        return value.tzinfo is None or value.tzinfo.utcoffset(value) is None

    def process_bind_param(self, value, dialect):
        if self.is_naive(value):
            value = value.replace(tzinfo=self.local_timezone)
        return value.astimezone(self.utc)

    def process_result_value(self, value, dialect):
        if self.is_naive(value):
            value = value.replace(tzinfo=self.utc)
        value = value.astimezone(self._timezone)
        if not self.timezone:
            value = value.replace(tzinfo=None)
        return value
