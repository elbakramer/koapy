"""
BSD 3-Clause License

Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team
All rights reserved.

Copyright (c) 2011-2020, Open source contributors.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

# https://github.com/pandas-dev/pandas/blob/master/pandas/tseries/holiday.py

import warnings
import datetime

from pandas.errors import PerformanceWarning
from pandas import DateOffset, DatetimeIndex, Timestamp, date_range
from pandas.tseries.holiday import Holiday

from koapy.utils.krx.holiday.KoreanLunarCalendar import KoreanLunarCalendar

class LunarHoliday(Holiday):

    def __init__(
        self,
        name,
        year=None,
        month=None,
        day=None,
        offset=None,
        observance=None,
        start_date=None,
        end_date=None,
        days_of_week=None,
    ):
        super().__init__(
            name,
            year,
            month,
            day,
            None,
            None,
            start_date,
            end_date,
            days_of_week,
        )
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.offset = offset
        self.start_date = (
            Timestamp(start_date) if start_date is not None else start_date
        )
        self.end_date = Timestamp(end_date) if end_date is not None else end_date
        self.observance = observance
        assert days_of_week is None or type(days_of_week) == tuple
        self.days_of_week = days_of_week

    def _reference_dates(self, start_date, end_date):
        """
        Get reference dates for the holiday.
        Return reference dates for the holiday also returning the year
        prior to the start_date and year following the end_date.  This ensures
        that any offsets to be applied will yield the holidays within
        the passed in dates.
        """
        if self.start_date is not None:
            start_date = self.start_date.tz_localize(start_date.tz)

        if self.end_date is not None:
            end_date = self.end_date.tz_localize(start_date.tz)

        year_offset = DateOffset(years=1)
        reference_start_date = Timestamp(
            KoreanLunarCalendar.lunar_to_solar_datetime(start_date.year - 1, self.month, self.day)
        )
        reference_end_date = Timestamp(
            KoreanLunarCalendar.lunar_to_solar_datetime(end_date.year + 1, self.month, self.day)
        )

        # Don't process unnecessary holidays
        dates = date_range(
            start=reference_start_date,
            end=reference_end_date,
            freq=year_offset,
            tz=start_date.tz,
        )
        dates = dates.to_series().apply(lambda date: KoreanLunarCalendar.lunar_to_solar_datetime(date.year, self.month, self.day))
        dates = DatetimeIndex(dates)

        return dates

    def _apply_rule(self, dates):
        """
        Apply the given offset/observance to a DatetimeIndex of dates.
        Parameters
        ----------
        dates : DatetimeIndex
            Dates to apply the given offset/observance rule
        Returns
        -------
        Dates with rules applied
        """

        if self.offset is not None:
            if not isinstance(self.offset, list):
                offsets = [self.offset]
            else:
                offsets = self.offset
            for offset in offsets:

                # if we are adding a non-vectorized value
                # ignore the PerformanceWarnings:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", PerformanceWarning)
                    dates += offset

        if self.observance is not None:
            return dates.map(self.observance)

        return dates

    def to_solar_datetime(self):
        today = datetime.datetime.today()
        year = self.year
        if year is None:
            year = today.year
        date = KoreanLunarCalendar.lunar_to_solar_datetime(year, self.month, self.day)
        dates = DatetimeIndex([date])
        dates = self._apply_rule(dates)
        date = dates[0]
        return date
