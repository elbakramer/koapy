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




.. py:class:: QThreadPoolExecutorRunnable(future: concurrent.futures.Future, fn, args, kwargs)

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QRunnable`

   .. py:method:: run(self)



.. py:class:: QThreadPoolExecutor(*args, **kwargs)

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QObject`, :py:obj:`concurrent.futures.Executor`

   This is an abstract base class for concrete asynchronous executors.

   .. py:method:: __del__(self)


   .. py:method:: submit(self, fn, *args, **kwargs)

      Submits a callable to be executed with the given arguments.

      Schedules the callable to be executed as fn(*args, **kwargs) and returns
      a Future instance representing the execution of the callable.

      :returns: A Future representing the given call.


   .. py:method:: shutdown(self, wait=True)

      Clean-up the resources associated with the Executor.

      It is safe to call this method several times. Otherwise, no other
      methods can be called after this one.

      :param wait: If True then shutdown will not return until all running
                   futures have finished executing and the resources used by the
                   executor have been reclaimed.



