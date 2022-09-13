from __future__ import annotations

import atexit
import queue
import time

from concurrent.futures import Executor, Future
from functools import update_wrapper
from queue import Queue
from threading import RLock
from typing import Any, Callable, Dict, Optional, Sequence

from koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSlotLikeExecutor import (
    QSlotLikeCallable,
)
from koapy.compat.pyside2.QtCore import QObject
from koapy.utils.logging.Logging import Logging
from koapy.utils.logging.pyside2.QThreadLogging import QThreadLogging
from koapy.utils.rate_limiting.RateLimiter import RateLimiter


class QRateLimitedExecutorRunnable(Logging):
    def __init__(
        self,
        future: Future,
        fn: Callable,
        args: Optional[Sequence[Any]] = None,
        kwargs: Optional[Dict[str, Any]] = None,
    ):
        self._future = future
        self._fn = fn
        self._args = ()
        self._kwargs = {}

        if args:
            self._args = args
        if kwargs:
            self._kwargs = kwargs

    def run(self):
        if not self._future.set_running_or_notify_cancel():
            return
        try:
            result = self._fn(*self._args, **self._kwargs)
        except BaseException as exc:  # pylint: disable=broad-except
            self.logger.exception(
                "Exception while running QRateLimitedExecutorRunnable"
            )
            self._future.set_exception(exc)
            # break a reference cycle with the exception 'exc'
            self = None  # pylint: disable=self-cls-assignment
        else:
            self._future.set_result(result)

    def cancel(self):
        return self._future.cancel()

    def result(self):
        return self._future.result()


class QRateLimitedExecutorDecoratedFunction(Logging):
    def __init__(
        self,
        func: QSlotLikeCallable,
        limiter: RateLimiter,
        executor: QRateLimitedExecutor,
    ):
        self._func = func
        self._limiter = limiter
        self._executor = executor

        update_wrapper(self, self._func, updated=[])

    def _checkAndSleepIfNecessary(self, *args, **kwargs):
        sleep_seconds = self._limiter.check_sleep_seconds(*args, **kwargs)
        if sleep_seconds > 0:
            if sleep_seconds > 1:
                self.logger.debug(
                    "Rate limiting function call %s(...), sleeping for %f seconds...",
                    self._func.__name__,
                    sleep_seconds,
                )
            time.sleep(sleep_seconds)
        self._limiter.add_call_history(*args, **kwargs)

    def _directCallFn(self, *args, **kwargs):
        self._checkAndSleepIfNecessary(*args, **kwargs)
        return self._func.directCall(*args, **kwargs)

    def directCall(self, *args, **kwargs):
        return self._directCallFn(*args, **kwargs)

    def _queuedCallFn(self, *args, **kwargs):
        self._checkAndSleepIfNecessary(*args, **kwargs)
        return self._func.queuedCall(*args, **kwargs).result()

    def queuedCall(self, *args, **kwargs):
        return self._executor.submit(self._queuedCallFn, *args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.directCall(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._func, name)


class QRateLimitedExecutor(QThreadLogging, Executor):
    def __init__(self, limiter: RateLimiter, parent: Optional[QObject] = None):
        QThreadLogging.__init__(self, parent)
        Executor.__init__(self)

        self._limiter = limiter
        self._parent = parent

        self._runnable_queue: Queue = Queue()
        self._sentinel = object()

        self._shutdown = False
        self._shutdown_lock = RLock()

        atexit.register(self.shutdown)

    def __del__(self):
        atexit.unregister(self.shutdown)

    def run(self):
        while True:
            runnable = self._runnable_queue.get()
            if runnable is not self._sentinel:
                runnable.run()
                continue
            if self._shutdown:
                return

    def submit(self, fn: Callable, /, *args, **kwargs):
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("Cannot schedule new futures after shutdown")
            future = Future()
            runnable = QRateLimitedExecutorRunnable(future, fn, args, kwargs)
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

    def wrapCallable(self, func: Callable):
        wrapped = QRateLimitedExecutorDecoratedFunction(func, self._limiter, self)
        return wrapped
