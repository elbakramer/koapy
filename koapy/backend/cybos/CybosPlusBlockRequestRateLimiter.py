import time
import threading
import collections
import logging

from functools import wraps

class TimeWindowRateLimiter:

    def __init__(self, period, calls):
        self._period = period
        self._calls = calls

        self._lock = threading.RLock()
        self._clock = time.time

        if hasattr(time, 'monotonic'):
            self._clock = time.monotonic

        self._call_history = collections.deque(maxlen=self._calls)

    def period_remaining(self):
        if len(self._call_history) < self._calls:
            return 0
        else:
            clock = self._clock()
            while len(self._call_history) > 0:
                remaining = self._call_history[0] - clock + self._period
                if remaining < 0:
                    self._call_history.popleft()
                else:
                    break
            return remaining

    def add_call_history(self):
        self._call_history.append(self._clock())

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._lock:
                period_remaining = self.period_remaining()
                if period_remaining > 0:
                    logging.debug('Sleeping %s seconds due to rate limiting...', period_remaining)
                    time.sleep(period_remaining)
                self.add_call_history()
            return func(*args, **kwargs)
        return wrapper

class CybosPlusBlockRequestRateLimiter(TimeWindowRateLimiter):

    """
    15초에 최대 60건으로제한

    Q. 플러스 데이터 요청 사용 제한에 대해 알고 싶습니다.
    http://money2.daishin.com/e5/mboard/ptype_accordion/plusFAQ/DW_Basic_List.aspx?boardseq=298&m=9508&p=8835&v=8640
    """

    def __init__(self):
        super().__init__(15, 60)
