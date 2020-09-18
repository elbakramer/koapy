import time
import threading

from functools import wraps

class SimpleRateLimiter:

    """
    [조회횟수 제한 관련 가이드]
      - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
      - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
      - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기
    """

    def __init__(self, period, calls):
        self._period = period
        self._calls = calls

        self._lock = threading.RLock()
        self._clock = time.time

        if hasattr(time, 'monotonic'):
            self._clock = time.monotonic

        self._num_calls = 0
        self._last_reset = 0

    def _period_remaining(self):
        elapsed = self._clock() - self._last_reset
        return self._period - elapsed

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._lock:
                period_remaining = self._period_remaining()
                if period_remaining <= 0:
                    self._num_calls = 0
                    self._last_reset = self._clock()
                self._num_calls += 1
                if self._num_calls > self._calls:
                    if period_remaining > 0:
                        time.sleep(period_remaining)
                    self._num_calls = 1
                    self._last_reset = self._clock()
            return func(*args, **kwargs)
        return wrapper
        