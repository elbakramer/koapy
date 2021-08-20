:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRateLimiter`
==============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRateLimiter


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRateLimiter.KiwoomOpenApiPlusCommRqDataRateLimiter
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRateLimiter.KiwoomOpenApiPlusSendOrderRateLimiter
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRateLimiter.KiwoomOpenApiPlusSendConditionRateLimiter




.. py:class:: KiwoomOpenApiPlusCommRqDataRateLimiter

   Bases: :py:obj:`koapy.utils.rate_limiting.RateLimiter.CompositeTimeWindowRateLimiter`

   [조회횟수 제한 관련 가이드]
     - 1초당 5회 조회를 1번 발생시킨 경우 : 17초대기
     - 1초당 5회 조회를 5연속 발생시킨 경우 : 90초대기
     - 1초당 5회 조회를 10연속 발생시킨 경우 : 3분(180초)대기


.. py:class:: KiwoomOpenApiPlusSendOrderRateLimiter

   Bases: :py:obj:`koapy.utils.rate_limiting.RateLimiter.TimeWindowRateLimiter`


.. py:class:: KiwoomOpenApiPlusSendConditionRateLimiter(comm_rate_limiter)

   Bases: :py:obj:`koapy.utils.rate_limiting.RateLimiter.RateLimiter`

   [조건검색 제한]
     - 조건검색(실시간 조건검색 포함)은 시세조회와 관심종목조회와 합산해서 1초에 5회만 요청 가능하며 1분에 1회로 조건검색 제한됩니다.

   [조건검색 제한]
       조건검색 요청은 1초당 5회 조회횟수 제한에 포함됩니다.
       동일 조건식에 대한 조건검색 요청은 1분에 1회로 제한됩니다.
       조건검색 결과가 100종목을 넘게 되면 해당조건은 실시간 조건검색 신호를 수신할 수 없습니다.
       실시간 조건검색은 최대 10개까지 사용 가능합니다.

   .. py:method:: get_limiter_per_condition(self, condition_name, condition_index)


   .. py:method:: check_sleep_seconds(self, fn, *args, **kwargs)


   .. py:method:: add_call_history(self, fn, *args, **kwargs)


   .. py:method:: sleep_if_necessary(self, fn, *args, **kwargs)



