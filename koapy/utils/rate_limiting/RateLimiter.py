import collections
import threading
import time

from functools import wraps

from koapy.utils.logging.Logging import Logging


class RateLimiter:
    def check_sleep_seconds(self):
        return 0

    def sleep_if_necessary(self):
        sleep_seconds = self.check_sleep_seconds()
        if sleep_seconds > 0:
            time.sleep(sleep_seconds)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.sleep_if_necessary()
            return func(*args, **kwargs)

        return wrapper


class TimeWindowRateLimiter(RateLimiter, Logging):
    def __init__(self, period, calls):
        super().__init__()

        self._period = period
        self._calls = calls

        self._lock = threading.RLock()
        self._clock = time.time

        if hasattr(time, "monotonic"):
            self._clock = time.monotonic

        self._call_history = collections.deque(maxlen=self._calls)

    def check_sleep_seconds(self):
        with self._lock:
            if len(self._call_history) < self._calls:
                return 0
            clock = self._clock()
            remaining = self._call_history[0] + self._period - clock
            return remaining

    def add_call_history(self):
        with self._lock:
            return self._call_history.append(self._clock())

    def sleep_if_necessary(self):
        with self._lock:
            sleep_seconds = self.check_sleep_seconds()
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
            self.add_call_history()


class CompositeTimeWindowRateLimiter(RateLimiter):
    def __init__(self, limiters):
        super().__init__()

        self._lock = threading.RLock()
        self._limiters = limiters

    def check_sleep_seconds(self):
        with self._lock:
            return max(limiter.check_sleep_seconds() for limiter in self._limiters)

    def add_call_history(self):
        with self._lock:
            for limiter in self._limiters:
                limiter.add_call_history()

    def sleep_if_necessary(self):
        with self._lock:
            sleep_seconds = self.check_sleep_seconds()
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
            self.add_call_history()
