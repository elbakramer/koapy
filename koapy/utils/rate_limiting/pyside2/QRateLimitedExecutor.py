import atexit
import functools
import queue

from concurrent.futures import Executor, Future
from queue import Queue
from threading import RLock
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from koapy.compat.pyside2.QtCore import QObject, Qt, Signal
from koapy.utils.logging.pyside2.QThreadLogging import QThreadLogging
from koapy.utils.rate_limiting.RateLimiter import RateLimiter


class QRateLimitedExecutorRunnable:
    def __init__(
        self,
        limiter: RateLimiter,
        future: Future,
        fn: Callable[..., Any],
        args: Union[Tuple[Any], List[Any]],
        kwargs: Dict[str, Any],
    ):
        self._limiter = limiter
        self._future = future
        self._fn = fn
        self._args = args
        self._kwargs = kwargs

    def check_sleep_seconds(self):
        return self._limiter.check_sleep_seconds(self._fn, *self._args, **self._kwargs)

    def add_call_history(self):
        return self._limiter.add_call_history(self._fn, *self._args, **self._kwargs)

    def sleep_if_necessary(self):
        return self._limiter.sleep_if_necessary(self._fn, *self._args, **self._kwargs)

    def run(self):
        if not self._future.set_running_or_notify_cancel():
            return
        try:
            self.add_call_history()
            result = self._fn(*self._args, **self._kwargs)
        except BaseException as exc:  # pylint: disable=broad-except
            self._future.set_exception(exc)
            # break a reference cycle with the exception 'exc'
            self = None  # pylint: disable=self-cls-assignment
        else:
            self._future.set_result(result)

    def cancel(self):
        return self._future.cancel()

    def result(self):
        return self._future.result()


class QRateLimitedExecutorDecoratedFunction:
    def __init__(self, func, limiter: RateLimiter, executor: Executor):
        self._func = func
        self._limiter = limiter
        self._executor = executor

        functools.update_wrapper(self, func)
        self._func_limited = self._limiter.wrap(self._func)

    def call(self, *args, **kwargs):
        return self._func_limited(*args, **kwargs)

    def async_call(self, *args, **kwargs):
        return self._executor.submit(self._func, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)


class QRateLimitedExecutor(QThreadLogging, Executor):

    readyRunnable = Signal(QRateLimitedExecutorRunnable)

    def __init__(self, limiter: RateLimiter, parent: Optional[QObject] = None):
        QThreadLogging.__init__(self, parent)
        Executor.__init__(self)

        self._limiter = limiter
        self._parent = parent

        self._runnable_queue: Queue = Queue()
        self._sentinel = object()

        self._shutdown = False
        self._shutdown_lock = RLock()

        self.readyRunnable.connect(self.onReadyRunnable, Qt.QueuedConnection)

        atexit.register(self.shutdown)

    def __del__(self):
        atexit.unregister(self.shutdown)

    def run(self):
        while True:
            runnable = self._runnable_queue.get()
            if runnable is not self._sentinel:
                runnable.sleep_if_necessary()
                self.readyRunnable.emit(runnable)
                try:
                    runnable.result()  # wait until the emitted runnable finishes
                except:  # pylint: disable=bare-except
                    pass
                del runnable
                continue
            if self._shutdown:
                return

    def onReadyRunnable(self, runnable: QRateLimitedExecutorRunnable):
        runnable.run()

    def submit(
        self, fn: Callable[..., Any], *args, **kwargs
    ):  # pylint: disable=arguments-differ
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("Cannot schedule new futures after shutdown")
            future = Future()
            runnable = QRateLimitedExecutorRunnable(
                self._limiter, future, fn, args, kwargs
            )
            self._runnable_queue.put(runnable)
            return future

    def shutdown(
        self, wait: bool = True, cancel_futures: bool = False
    ):  # pylint: disable=arguments-differ
        with self._shutdown_lock:
            self._shutdown = True
            if cancel_futures:
                while True:
                    try:
                        runnable = self._runnable_queue.get_nowait()
                    except queue.Empty:
                        break
                    if runnable is not self._sentinel:
                        runnable.cancel()
            self._runnable_queue.put(self._sentinel)
        if wait:
            self.wait()

    def wrap(self, func: Callable[..., Any]):
        return QRateLimitedExecutorDecoratedFunction(func, self._limiter, self)

    def __call__(self, func: Callable[..., Any]):
        return self.wrap(func)
