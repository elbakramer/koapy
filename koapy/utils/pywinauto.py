import time

from typing import Callable, Optional, Sequence, TypeVar

T = TypeVar("T")


def wait_any(
    waits: Sequence[Callable[[], T]],
    timeout: Optional[int] = None,
    retry_interval: Optional[int] = None,
) -> T:
    import pywinauto.timings

    if timeout is None:
        timeout = pywinauto.timings.Timings.window_find_timeout
    if retry_interval is None:
        retry_interval = pywinauto.timings.Timings.window_find_retry

    start_time = time.time()
    should_stop = False

    while not should_stop:
        for wait in waits:
            try:
                return wait()
            except pywinauto.timings.TimeoutError:
                elapsed_seconds = time.time() - start_time
                if elapsed_seconds > timeout:
                    raise
                time.sleep(retry_interval)
