import threading
import time

from koapy.utils.rate_limiting.RateLimiter import (
    CompositeTimeWindowRateLimiter,
    RateLimiter,
    TimeWindowRateLimiter,
)


class KiwoomOpenApiPlusCommRqDataRateLimiter(CompositeTimeWindowRateLimiter):

    # [조회횟수 제한 관련]
    # 단순하게 1초당 5회로 날리다보면 장기적으로 결국 막히기 때문에 기존에는 4초당 1회로 제한했었음 (3초당 1회부턴 제한걸림)
    # 이후 1시간에 1000회로 제한한다는 추측이 있는데 일리 있어 보여서 도입 (http://blog.quantylab.com/htsapi.html)
    # 1초당 1회로 계산했을때 1시간이면 3600 회, 주기를 1초씩 늘려보면
    # 2초당 1회 => 1800 > 1000, 3초당 1회 => 1200 > 1000, 4초당 1회 => 900 < 1000

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


class KiwoomOpenApiPlusSendOrderRateLimiter(TimeWindowRateLimiter):
    def __init__(self):
        super().__init__(1, 5)


class KiwoomOpenApiPlusSendConditionRateLimiter(RateLimiter):

    """
    [조건검색 제한]
      - 조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.

    [조건검색 제한]
        조건검색 요청은 1초당 5회 조회횟수 제한에 포함됩니다.
        동일 조건식에 대한 조건검색 요청은 1분에 1회로 제한됩니다.
        조건검색 결과가 100종목을 넘게 되면 해당조건은 실시간 조건검색 신호를 수신할 수 없습니다.
        실시간 조건검색은 최대 10개까지 사용 가능합니다.
    """

    def __init__(self, comm_rate_limiter):
        self._lock = threading.RLock()

        self._comm_rate_limiter = comm_rate_limiter
        self._limiters_per_condition = {}

    def get_limiter_per_condition(self, condition_name, condition_index):
        limiter_key = (condition_name, condition_index)
        if limiter_key not in self._limiters_per_condition:
            self._limiters_per_condition[limiter_key] = TimeWindowRateLimiter(60, 1)
        limiter_per_condition = self._limiters_per_condition[limiter_key]
        return limiter_per_condition

    def check_sleep_seconds(self, fn, *args, **kwargs):
        condition_name = None
        condition_index = None
        if fn.__name__ == "SendCondition":
            condition_name = kwargs.get("condition_name", args[1])
            condition_index = kwargs.get("condition_index", args[2])
        with self._lock:
            sleep_seconds = self._comm_rate_limiter.check_sleep_seconds()
            if condition_name is not None and condition_index is not None:
                limiter_per_condition = self.get_limiter_per_condition(
                    condition_name, condition_index
                )
                sleep_seconds = max(
                    sleep_seconds, limiter_per_condition.check_sleep_seconds()
                )
            return sleep_seconds

    def add_call_history(self, fn, *args, **kwargs):
        condition_name = None
        condition_index = None
        if fn.__name__ == "SendCondition":
            condition_name = kwargs.get("condition_name", args[1])
            condition_index = kwargs.get("condition_index", args[2])
        with self._lock:
            self._comm_rate_limiter.add_call_history()
            if condition_name is not None and condition_index is not None:
                limiter_per_condition = self.get_limiter_per_condition(
                    condition_name, condition_index
                )
                limiter_per_condition.add_call_history()

    def sleep_if_necessary(self, fn, *args, **kwargs):
        with self._lock:
            sleep_seconds = self.check_sleep_seconds(fn, *args, **kwargs)
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
