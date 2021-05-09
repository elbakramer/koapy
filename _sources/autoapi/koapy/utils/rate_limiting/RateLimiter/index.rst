:mod:`koapy.utils.rate_limiting.RateLimiter`
============================================

.. py:module:: koapy.utils.rate_limiting.RateLimiter


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.rate_limiting.RateLimiter.RateLimiter
   koapy.utils.rate_limiting.RateLimiter.TimeWindowRateLimiter
   koapy.utils.rate_limiting.RateLimiter.CompositeTimeWindowRateLimiter




.. class:: RateLimiter

   .. method:: check_sleep_seconds(self)


   .. method:: sleep_if_necessary(self)


   .. method:: __call__(self, func)



.. class:: TimeWindowRateLimiter(period, calls)


   Bases: :py:obj:`RateLimiter`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: check_sleep_seconds(self)


   .. method:: add_call_history(self)


   .. method:: sleep_if_necessary(self)



.. class:: CompositeTimeWindowRateLimiter(limiters)


   Bases: :py:obj:`RateLimiter`

   .. method:: check_sleep_seconds(self)


   .. method:: add_call_history(self)


   .. method:: sleep_if_necessary(self)



