:py:mod:`koapy.backend.kiwoom_open_api_plus.utils.pyside2.QThreadPoolExecutor`
==============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.pyside2.QThreadPoolExecutor


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.pyside2.QThreadPoolExecutor.QThreadPoolExecutorRunnable
   koapy.backend.kiwoom_open_api_plus.utils.pyside2.QThreadPoolExecutor.QThreadPoolExecutor




.. py:class:: QThreadPoolExecutorRunnable(future: concurrent.futures.Future, fn: Callable[Ellipsis, Any], args: Union[Tuple[Any], List[Any]], kwargs: Dict[str, Any])

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QRunnable`

   .. py:method:: run(self)



.. py:class:: QThreadPoolExecutor(thread_pool: koapy.compat.pyside2.QtCore.QThreadPool, parent: Optional[koapy.compat.pyside2.QtCore.QObject])           QThreadPoolExecutor(parent: Optional[koapy.compat.pyside2.QtCore.QObject])

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QObject`, :py:obj:`concurrent.futures.Executor`

   This is an abstract base class for concrete asynchronous executors.

   .. py:method:: __del__(self)


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



