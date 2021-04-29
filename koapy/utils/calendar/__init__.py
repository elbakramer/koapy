from exchange_calendars.calendar_utils import ExchangeCalendarDispatcher

from .exchange_calendar_xkrx import XKRXExchangeCalendar

_default_calendar_factories = {
    "XKRX": XKRXExchangeCalendar,
}

_default_calendar_aliases = {
    "KRX": "XKRX",
}

global_calendar_dispatcher = ExchangeCalendarDispatcher(
    calendars={},
    calendar_factories=_default_calendar_factories,
    aliases=_default_calendar_aliases,
)

get_calendar = global_calendar_dispatcher.get_calendar
get_calendar_names = global_calendar_dispatcher.get_calendar_names
clear_calendars = global_calendar_dispatcher.clear_calendars
deregister_calendar = global_calendar_dispatcher.deregister_calendar
register_calendar = global_calendar_dispatcher.register_calendar
register_calendar_type = global_calendar_dispatcher.register_calendar_type
register_calendar_alias = global_calendar_dispatcher.register_calendar_alias
resolve_alias = global_calendar_dispatcher.resolve_alias
