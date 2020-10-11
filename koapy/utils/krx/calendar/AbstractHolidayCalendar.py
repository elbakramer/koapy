"""
"""

# pylint: disable=pointless-string-statement

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

from pandas import DatetimeIndex, Series, Timestamp
from pandas.tseries.holiday import AbstractHolidayCalendar as PandasAbstractHolidayCalendar

class AbstractHolidayCalendar(PandasAbstractHolidayCalendar):

    def concat(self, pre_holidays):
        combined = Series(index=DatetimeIndex([]), dtype=object)
        for holidays in pre_holidays:
            combined = combined.combine_first(holidays)
        return combined

    def holidays(self, start=None, end=None, return_name=False):
        """
        Returns a curve with holidays between start_date and end_date
        Parameters
        ----------
        start : starting date, datetime-like, optional
        end : ending date, datetime-like, optional
        return_name : bool, optional
            If True, return a series that has dates and holiday names.
            False will only return a DatetimeIndex of dates.
        Returns
        -------
            DatetimeIndex of holidays
        """
        if self.rules is None:
            raise Exception(
                f"Holiday Calendar {self.name} does not have any rules specified"
            )

        if start is None:
            start = AbstractHolidayCalendar.start_date

        if end is None:
            end = AbstractHolidayCalendar.end_date

        start = Timestamp(start)
        end = Timestamp(end)

        # If we don't have a cache or the dates are outside the prior cache, we
        # get them again
        if self._cache is None or start < self._cache[0] or end > self._cache[1]:
            pre_holidays = [
                rule.dates(start, end, return_name=True) for rule in self.rules
            ]
            if pre_holidays:
                holidays = self.concat(pre_holidays) # This line is changed from original implementation
            else:
                holidays = Series(index=DatetimeIndex([]), dtype=object)

            self._cache = (start, end, holidays.sort_index())

        holidays = self._cache[2]
        holidays = holidays[start:end]

        if return_name:
            return holidays
        else:
            return holidays.index
