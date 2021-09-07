:py:mod:`koapy.utils.rate_limiting.pyside2.QRateLimitedExecutor`
================================================================

.. py:module:: koapy.utils.rate_limiting.pyside2.QRateLimitedExecutor


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.rate_limiting.pyside2.QRateLimitedExecutor.QRateLimitedExecutorRunnable
   koapy.utils.rate_limiting.pyside2.QRateLimitedExecutor.QRateLimitedExecutorDecoratedFunction
   koapy.utils.rate_limiting.pyside2.QRateLimitedExecutor.QRateLimitedExecutor




.. py:class:: QRateLimitedExecutorRunnable(limiter: koapy.utils.rate_limiting.RateLimiter.RateLimiter, future: concurrent.futures.Future, fn: Callable[Ellipsis, Any], args: Union[Tuple[Any], List[Any]], kwargs: Dict[str, Any])

   .. py:method:: check_sleep_seconds(self)


   .. py:method:: add_call_history(self)


   .. py:method:: sleep_if_necessary(self)


   .. py:method:: run(self)


   .. py:method:: cancel(self)



.. py:class:: QRateLimitedExecutorDecoratedFunction(func, limiter: koapy.utils.rate_limiting.RateLimiter.RateLimiter, executor: concurrent.futures.Executor)

   .. py:method:: call(self, *args, **kwargs)


   .. py:method:: async_call(self, *args, **kwargs)


   .. py:method:: __call__(self, *args, **kwargs)



.. py:class:: QRateLimitedExecutor(limiter: koapy.utils.rate_limiting.RateLimiter.RateLimiter, parent=None)

   Bases: :py:obj:`koapy.utils.logging.pyside2.QThreadLogging.QThreadLogging`, :py:obj:`concurrent.futures.Executor`

   This is an abstract base class for concrete asynchronous executors.

   .. py:attribute:: readyRunnable
      

      

   .. py:method:: __del__(self)


   .. py:method:: run(self)


   .. py:method:: onReadyRunnable(self, runnable)


   .. py:method:: submit(self, fn, *args, **kwargs)

      Submits a callable to be executed with the given arguments.

      Schedules the callable to be executed as fn(*args, **kwargs) and returns
      a Future instance representing the execution of the callable.

      :returns: A Future representing the given call.


   .. py:method:: shutdown(self, wait=True, cancel_futures=False)

      Clean-up the resources associated with the Executor.

      It is safe to call this method several times. Otherwise, no other
      methods can be called after this one.

      :param wait: If True then shutdown will not return until all running
                   futures have finished executing and the resources used by the
                   executor have been reclaimed.


   .. py:method:: wrap(self, func)


   .. py:method:: __call__(self, func)



