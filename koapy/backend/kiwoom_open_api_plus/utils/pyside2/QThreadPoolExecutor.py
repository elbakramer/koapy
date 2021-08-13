import atexit

from concurrent.futures import Executor, Future
from threading import RLock

from koapy.compat.pyside2.QtCore import QObject, QRunnable, QThreadPool


class QThreadPoolExecutorRunnable(QRunnable):
    def __init__(self, future: Future, fn, args, kwargs):
        super().__init__()
        self._future = future
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def run(self):
        if not self._future.set_running_or_notify_cancel():
            return
        try:
            result = self._fn(*self._args, **self._kwargs)
        except BaseException as exc:
            self._future.set_exception(exc)
            self = None
        else:
            self._future.set_result(result)


class QThreadPoolExecutor(QObject, Executor):
    def __init__(self, *args, **kwargs):
        thread_pool = None
        parent = None

        args = list(args)
        kwargs = dict(kwargs)

        if len(args) > 0 and isinstance(args[0], QThreadPool):
            thread_pool = args.pop(0)
        elif "thread_pool" in kwargs:
            thread_pool = kwargs.pop("thread_pool")

        if len(args) > 0:
            parent = args[0]
        elif "parent" in kwargs:
            parent = kwargs["parent"]

        if thread_pool is None:
            thread_pool = QThreadPool.globalInstance()

        QObject.__init__(self, *args, **kwargs)
        Executor.__init__(self)

        self._thread_pool = thread_pool
        self._shutdown = False
        self._shutdown_lock = RLock()

        atexit.register(self.shutdown)

    def __del__(self):
        atexit.unregister(self.shutdown)

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")
            future = Future()
            runnable = QThreadPoolExecutorRunnable(future, fn, args, kwargs)
            self._thread_pool.start(runnable)
            return future

    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
        if wait:
            self._thread_pool.waitForDone()
