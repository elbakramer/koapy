:py:mod:`koapy.utils.rate_limiting.RateLimiter`
===============================================

.. py:module:: koapy.utils.rate_limiting.RateLimiter


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.rate_limiting.RateLimiter.RateLimiter
   koapy.utils.rate_limiting.RateLimiter.TimeWindowRateLimiter
   koapy.utils.rate_limiting.RateLimiter.CompositeTimeWindowRateLimiter




.. py:class:: RateLimiter

   .. py:method:: check_sleep_seconds(self)


   .. py:method:: sleep_if_necessary(self)


   .. py:method:: __call__(self, func)



.. py:class:: TimeWindowRateLimiter(period, calls)

   Bases: :py:obj:`RateLimiter`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: check_sleep_seconds(self)


   .. py:method:: add_call_history(self)


   .. py:method:: sleep_if_necessary(self)



.. py:class:: CompositeTimeWindowRateLimiter(limiters)

   Bases: :py:obj:`RateLimiter`

   .. py:method:: check_sleep_seconds(self)


   .. py:method:: add_call_history(self)


   .. py:method:: sleep_if_necessary(self)



