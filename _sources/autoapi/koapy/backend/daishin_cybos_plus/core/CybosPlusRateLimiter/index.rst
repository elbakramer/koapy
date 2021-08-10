:py:mod:`koapy.backend.daishin_cybos_plus.core.CybosPlusRateLimiter`
====================================================================

.. py:module:: koapy.backend.daishin_cybos_plus.core.CybosPlusRateLimiter


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.daishin_cybos_plus.core.CybosPlusRateLimiter.CybosPlusLookupRequestRateLimiter
   koapy.backend.daishin_cybos_plus.core.CybosPlusRateLimiter.CybosPlusTradeRequestRateLimiter




.. py:class:: CybosPlusLookupRequestRateLimiter

   Bases: :py:obj:`koapy.utils.rate_limiting.RateLimiter.TimeWindowRateLimiter`

   시세 오브젝트 조회 제한: 15초에 최대 60건으로제한

   Q. 플러스 데이터 요청 사용 제한에 대해 알고 싶습니다.
   http://money2.daishin.com/e5/mboard/ptype_accordion/plusFAQ/DW_Basic_List.aspx?boardseq=298&m=9508&p=8835&v=8640


.. py:class:: CybosPlusTradeRequestRateLimiter

   Bases: :py:obj:`koapy.utils.rate_limiting.RateLimiter.TimeWindowRateLimiter`

   주문관련 오브젝트 조회 제한: 15초에 최대 20건으로제한

   Q. 플러스 데이터 요청 사용 제한에 대해 알고 싶습니다.
   http://money2.daishin.com/e5/mboard/ptype_accordion/plusFAQ/DW_Basic_List.aspx?boardseq=298&m=9508&p=8835&v=8640


