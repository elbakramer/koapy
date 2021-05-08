from collections import OrderedDict

import numpy as np
import pandas as pd
import toolz

from exchange_calendars.exchange_calendar import (
    ExchangeCalendar as BaseExchangeCalendar,
)
from exchange_calendars.exchange_calendar import (
    _check_breaks_match,
    _overwrite_special_dates,
    _remove_breaks_for_special_dates,
    end_default,
    start_default,
)
from exchange_calendars.utils.memoize import lazyval
from exchange_calendars.utils.pandas_utils import days_at_time as _days_at_time
from pandas import DataFrame, date_range
from pandas.tseries.offsets import CustomBusinessDay
from pytz import UTC

from .pandas_extensions.offsets import MultipleWeekmaskCustomBusinessDay


def selection(arr, start, end):
    predicates = []
    if start is not None:
        predicates.append(start.tz_localize(UTC) <= arr)
    if end is not None:
        predicates.append(arr < end.tz_localize(UTC))

    if not predicates:
        return arr

    return arr[np.all(predicates, axis=0)]


def days_at_time(days, t, tz, day_offset=0):
    if t is None:
        return pd.DatetimeIndex([None for _ in days]).tz_localize(UTC)
    return _days_at_time(days, t, tz, day_offset)


def _group_times(all_days, times, tz, offset=0):
    if times is None:
        return None
    elements = [
        days_at_time(selection(all_days, start, end), time, tz, offset)
        for (start, time), (end, _) in toolz.sliding_window(
            2, toolz.concatv(times, [(None, None)])
        )
    ]
    return elements[0].append(elements[1:])


class ExchangeCalendar(BaseExchangeCalendar):
    """
    An ExchangeCalendar represents the timing information of a single market
    exchange.

    The timing information is made up of two parts: sessions, and opens/closes.

    A session represents a contiguous set of minutes, and has a label that is
    midnight UTC. It is important to note that a session label should not be
    considered a specific point in time, and that midnight UTC is just being
    used for convenience.

    For each session, we store the open and close time in UTC time.
    """

    def __init__(
        self, start=start_default, end=end_default
    ):  # pylint: disable=super-init-not-called

        # Midnight in UTC for each trading day.

        _all_days = date_range(start, end, freq=self.day, tz=UTC)

        # `DatetimeIndex`s of standard opens/closes for each day.
        self._opens = _group_times(
            _all_days,
            self.open_times,
            self.tz,
            self.open_offset,
        )
        self._break_starts = _group_times(
            _all_days,
            self.break_start_times,
            self.tz,
        )
        self._break_ends = _group_times(
            _all_days,
            self.break_end_times,
            self.tz,
        )

        self._closes = _group_times(
            _all_days,
            self.close_times,
            self.tz,
            self.close_offset,
        )

        # Apply special offsets first
        self._calculate_and_overwrite_special_offsets(_all_days, start, end)

        # `Series`s mapping sessions with nonstandard opens/closes to
        # the open/close time.
        _special_opens = self._calculate_special_opens(start, end)
        _special_closes = self._calculate_special_closes(start, end)

        # Overwrite the special opens and closes on top of the standard ones.
        _overwrite_special_dates(_all_days, self._opens, _special_opens)
        _overwrite_special_dates(_all_days, self._closes, _special_closes)
        _remove_breaks_for_special_dates(
            _all_days,
            self._break_starts,
            _special_closes,
        )
        _remove_breaks_for_special_dates(
            _all_days,
            self._break_ends,
            _special_closes,
        )

        self.schedule = DataFrame(
            index=_all_days,
            data=OrderedDict(
                [
                    ("market_open", self._opens),
                    ("break_start", self._break_starts),
                    ("break_end", self._break_ends),
                    ("market_close", self._closes),
                ]
            ),
            dtype="datetime64[ns]",
        )

        # Simple cache to avoid recalculating the same minute -> session in
        # "next" mode. `minute_to_session_label` is often called consecutively
        # with the same inputs.
        self._minute_to_session_label_cache = (None, None)

        self.market_opens_nanos = self.schedule.market_open.values.astype(np.int64)

        self.market_break_starts_nanos = self.schedule.break_start.values.astype(
            np.int64
        )

        self.market_break_ends_nanos = self.schedule.break_end.values.astype(np.int64)

        self.market_closes_nanos = self.schedule.market_close.values.astype(np.int64)

        _check_breaks_match(
            self.market_break_starts_nanos, self.market_break_ends_nanos
        )

        # pylint: disable=no-member
        self._trading_minutes_nanos = self.all_minutes.values.astype(np.int64)

        self.first_trading_session = _all_days[0]
        self.last_trading_session = _all_days[-1]

        self._late_opens = pd.DatetimeIndex(
            _special_opens.map(self.minute_index_to_session_labels)
        )

        self._early_closes = pd.DatetimeIndex(
            _special_closes.map(self.minute_index_to_session_labels)
        )

    @lazyval
    def day(self):
        if self.special_weekmasks:
            return MultipleWeekmaskCustomBusinessDay(
                holidays=self.adhoc_holidays,
                calendar=self.regular_holidays,
                weekmask=self.weekmask,
                weekmasks=self.special_weekmasks,
            )
        else:
            return CustomBusinessDay(
                holidays=self.adhoc_holidays,
                calendar=self.regular_holidays,
                weekmask=self.weekmask,
            )

    @property
    def special_weekmasks(self):
        """
        Returns
        -------
        list: List of (date, date, str) tuples that represent special
         weekmasks that applies between dates.
        """
        return []

    @property
    def special_offsets(self):
        """
        Returns
        -------
        list: List of (timedelta, timedelta, timedelta, timedelta, AbstractHolidayCalendar) tuples
         that represent special open, break_start, break_end, close offsets
         and corresponding HolidayCalendars.
        """
        return []

    @property
    def special_offsets_adhoc(self):
        """
        Returns
        -------
        list: List of (timedelta, timedelta, timedelta, timedelta, DatetimeIndex) tuples
         that represent special open, break_start, break_end, close offsets
         and corresponding DatetimeIndexes.
        """
        return []

    def _overwrite_special_offsets(
        self,
        session_labels,
        opens_or_closes,
        calendars,
        ad_hoc_dates,
        start_date,
        end_date,
        strict=False,
    ):
        # Short circuit when nothing to apply.
        if opens_or_closes is None or not len(opens_or_closes):
            return

        len_m, len_oc = len(session_labels), len(opens_or_closes)
        if len_m != len_oc:
            raise ValueError(
                "Found misaligned dates while building calendar.\n"
                "Expected session_labels to be the same length as "
                "open_or_closes but,\n"
                "len(session_labels)=%d, len(open_or_closes)=%d" % (len_m, len_oc)
            )

        regular = []
        for offset, calendar in calendars:
            days = calendar.holidays(start_date, end_date)
            series = pd.Series(
                index=pd.DatetimeIndex(days, tz=UTC),
                data=offset,
            )
            regular.append(series)

        ad_hoc = []
        for offset, datetimes in ad_hoc_dates:
            series = pd.Series(
                index=pd.to_datetime(datetimes, utc=True),
                data=offset,
            )
            ad_hoc.append(series)

        merged = regular + ad_hoc
        if not merged:
            return pd.Series([], dtype="timedelta64[ns]")

        result = pd.concat(merged).sort_index()
        offsets = result.loc[(result.index >= start_date) & (result.index <= end_date)]

        # Find the array indices corresponding to each special date.
        indexer = session_labels.get_indexer(offsets.index)

        # -1 indicates that no corresponding entry was found.  If any -1s are
        # present, then we have special dates that doesn't correspond to any
        # trading day.
        if -1 in indexer and strict:
            bad_dates = list(offsets.index[indexer == -1])
            raise ValueError("Special dates %s are not trading days." % bad_dates)

        special_opens_or_closes = opens_or_closes[indexer] + offsets

        # Short circuit when nothing to apply.
        if not len(special_opens_or_closes):
            return

        # NOTE: This is a slightly dirty hack.  We're in-place overwriting the
        # internal data of an Index, which is conceptually immutable.  Since we're
        # maintaining sorting, this should be ok, but this is a good place to
        # sanity check if things start going haywire with calendar computations.
        opens_or_closes.values[indexer] = special_opens_or_closes.values

    def _calculate_and_overwrite_special_offsets(self, session_labels, start, end):
        _special_offsets = self.special_offsets
        _special_offsets_adhoc = self.special_offsets_adhoc

        _special_open_offsets = [
            (t[0], t[-1]) for t in _special_offsets if t[0] is not None
        ]
        _special_open_offsets_adhoc = [
            (t[0], t[-1]) for t in _special_offsets_adhoc if t[0] is not None
        ]
        _special_break_start_offsets = [
            (t[1], t[-1]) for t in _special_offsets if t[1] is not None
        ]
        _special_break_start_offsets_adhoc = [
            (t[1], t[-1]) for t in _special_offsets_adhoc if t[1] is not None
        ]
        _special_break_end_offsets = [
            (t[2], t[-1]) for t in _special_offsets if t[2] is not None
        ]
        _special_break_end_offsets_adhoc = [
            (t[2], t[-1]) for t in _special_offsets_adhoc if t[2] is not None
        ]
        _special_close_offsets = [
            (t[3], t[-1]) for t in _special_offsets if t[3] is not None
        ]
        _special_close_offsets_adhoc = [
            (t[3], t[-1]) for t in _special_offsets_adhoc if t[3] is not None
        ]

        self._overwrite_special_offsets(
            session_labels,
            self._opens,
            _special_open_offsets,
            _special_open_offsets_adhoc,
            start,
            end,
        )
        self._overwrite_special_offsets(
            session_labels,
            self._break_starts,
            _special_break_start_offsets,
            _special_break_start_offsets_adhoc,
            start,
            end,
        )
        self._overwrite_special_offsets(
            session_labels,
            self._break_ends,
            _special_break_end_offsets,
            _special_break_end_offsets_adhoc,
            start,
            end,
        )
        self._overwrite_special_offsets(
            session_labels,
            self._closes,
            _special_close_offsets,
            _special_close_offsets_adhoc,
            start,
            end,
        )
