import time
import threading
import collections

from functools import wraps

class SimpleRateLimiter:

    def __init__(self, period, calls):
        self._period = period
        self._calls = calls

        self._lock = threading.RLock()
        self._clock = time.time

        if hasattr(time, 'monotonic'):
            self._clock = time.monotonic

        self._num_calls = 0
        self._last_reset = 0

    def period_remaining(self):
        elapsed = self._clock() - self._last_reset
        return self._period - elapsed

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._lock:
                period_remaining = self.period_remaining()
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
                    time.sleep(period_remaining)
                self.add_call_history()
            return func(*args, **kwargs)
        return wrapper

class CompositeTimeWindowRateLimiter:

    def __init__(self, limiters):
        self._limiters = limiters
        self._lock = threading.RLock()

    def period_remaining(self):
        return max(limiter.period_remaining() for limiter in self._limiters)

    def add_call_history(self):
        for limiter in self._limiters:
            limiter.add_call_history()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self._lock:
                period_remaining = self.period_remaining()
                if period_remaining > 0:
                    time.sleep(period_remaining)
                self.add_call_history()
            return func(*args, **kwargs)
        return wrapper

class KiwoomCommRqDataRateLimiter(CompositeTimeWindowRateLimiter):

    """
    [조회횟수 제한 관련 가이드]
      - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
      - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
      - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기
    """

    def __init__(self):
        limiters = [
            TimeWindowRateLimiter(18, 5),
            TimeWindowRateLimiter(90, 25),
            TimeWindowRateLimiter(180, 50),
            TimeWindowRateLimiter(3600, 1000),
        ]
        super().__init__(limiters)

class KiwoomSendConditionRateLimiter(CompositeTimeWindowRateLimiter):

    """
    [조건검색 제한]
      - 조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.
    """

    def __init__(self):
        limiters = [
            TimeWindowRateLimiter(1, 5),
        ]
        super().__init__(limiters)
        self._limiters_per_condition = {}

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            condition_name = kwargs.get('condition_name', args[1])
            condition_index = kwargs.get('condition_index', args[2])
            with self._lock:
                limiter_key = (condition_name, condition_index)
                if limiter_key not in self._limiters_per_condition:
                    self._limiters_per_condition[limiter_key] = TimeWindowRateLimiter(60, 1)
                limiter_per_condition = self._limiters_per_condition[limiter_key]
                period_remaining = max(self.period_remaining(), limiter_per_condition.period_remaining())
                if period_remaining > 0:
                    time.sleep(period_remaining)
                self.add_call_history()
            return func(*args, **kwargs)
        return wrapper

class CybosBlockRequestRateLimiter(TimeWindowRateLimiter):

    """
    15초에 최대 60건으로제한

    Q. 플러스 데이터 요청 사용 제한에 대해 알고 싶습니다.
    http://money2.daishin.com/e5/mboard/ptype_accordion/plusFAQ/DW_Basic_List.aspx?boardseq=298&m=9508&p=8835&v=8640
    """

    def __init__(self):
        super().__init__(15, 60)
