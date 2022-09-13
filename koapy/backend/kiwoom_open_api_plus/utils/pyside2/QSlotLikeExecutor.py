from __future__ import annotations

from concurrent.futures import Executor, Future
from typing import Any, Callable, Dict, Optional, Sequence

try:
    from typing import ParamSpec, TypeVar
except ImportError:
    from typing_extensions import ParamSpec
    from typing import TypeVar

from functools import update_wrapper

from koapy.compat.pyside2.QtCore import QObject, Qt, Signal
from koapy.utils.logging.Logging import Logging

P = ParamSpec("P")
R = TypeVar("R")


class QSlotLikeExecutorRunnable(Logging):
    def __init__(
        self,
        future: Future,
        fn: Callable[P, R],
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
            self.logger.exception("Exception while running QSlotLikeExecutorRunnable")
            self._future.set_exception(exc)
            # break a reference cycle with the exception 'exc'
            self = None  # pylint: disable=self-cls-assignment
        else:
            self._future.set_result(result)


class QSlotLikeCallable:
    def __init__(self, fn: Callable[P, R], executor: QSlotLikeExecutor):
        self._fn = fn
        self._executor = executor
        update_wrapper(self, self._fn, updated=[])

    def directCall(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self._fn(*args, **kwargs)

    def queuedCall(self, *args: P.args, **kwargs: P.kwargs) -> Future:
        return self._executor.submit(self._fn, *args, **kwargs)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self.directCall(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._fn, name)


class QSlotLikeExecutor(QObject, Executor):

    readyRunnable = Signal(QSlotLikeExecutorRunnable)

    def __init__(self, parent: Optional[QObject] = None):
        QObject.__init__(self, parent)
        Executor.__init__(self)
        self.readyRunnable.connect(self.onReadyRunnable, Qt.QueuedConnection)

    def onReadyRunnable(self, runnable: QSlotLikeExecutorRunnable):
        runnable.run()

    def submit(self, fn: Callable[P, R], /, *args, **kwargs):
        future = Future()
        runnable = QSlotLikeExecutorRunnable(future, fn, args, kwargs)
        self.readyRunnable.emit(runnable)
        return future

    def wrapCallable(self, fn: Callable[P, R]) -> QSlotLikeCallable:
        wrapped = QSlotLikeCallable(fn, self)
        return wrapped
