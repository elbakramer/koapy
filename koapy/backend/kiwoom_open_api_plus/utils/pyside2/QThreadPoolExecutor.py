import atexit

from concurrent.futures import Executor, Future
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, overload

from koapy.compat.pyside2.QtCore import QObject, QRunnable, QThreadPool


class QThreadPoolExecutorRunnable(QRunnable):
    def __init__(
        self,
        future: Future,
        fn: Callable[..., Any],
        args: Union[Tuple[Any], List[Any]],
        kwargs: Dict[str, Any],
    ):
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
            # break a reference cycle with the exception 'exc'
            self = None
        else:
            self._future.set_result(result)

    def __del__(self):
        self._future.cancel()


class QThreadPoolExecutor(QObject, Executor):
    @overload
    def __init__(self, thread_pool: QThreadPool, parent: Optional[QObject]):
        ...

    @overload
    def __init__(self, parent: Optional[QObject]):
        ...

    def __init__(self, *args, **kwargs):
        thread_pool: Optional[QThreadPool] = None
        parent: Optional[QObject] = None

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
            thread_pool = QThreadPool(self)

        self._thread_pool = thread_pool
        self._parent = parent

        QObject.__init__(self, *args, **kwargs)
        Executor.__init__(self)

        self._shutdown = False
        self._shutdown_lock = RLock()

        atexit.register(self.shutdown)

    def __del__(self):
        atexit.unregister(self.shutdown)

    def submit(self, fn, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("Cannot schedule new futures after shutdown")
            future = Future()
            runnable = QThreadPoolExecutorRunnable(future, fn, args, kwargs)
            runnable.setAutoDelete(True)
            self._thread_pool.start(runnable)
            return future

    def shutdown(self, wait=True, cancel_futures=False):
        with self._shutdown_lock:
            self._shutdown = True
            if cancel_futures:
                self._thread_pool.clear()
        if wait:
            self._thread_pool.waitForDone()
