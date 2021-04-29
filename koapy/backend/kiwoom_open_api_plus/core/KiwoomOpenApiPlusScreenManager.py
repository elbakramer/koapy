import collections
import random
import threading

from koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError import (
    KiwoomOpenApiPlusError,
)
from koapy.utils.logging.Logging import Logging


class KiwoomOpenApiPlusScreenManager(Logging):

    _maximum_num = 200

    def __init__(self, control=None):
        self._control = control
        self._lock = threading.RLock()
        self._occupied_screen_nos = collections.deque(maxlen=self._maximum_num)
        self._borrow_count_by_screen_no = {}

    @staticmethod
    def _number_to_screen_no(number):
        return str(number).zfill(4)

    @staticmethod
    def _screen_no_to_number(screen_no):
        return int(screen_no)

    def is_inuse(self, screen_no):
        return (
            screen_no is not None
            and self._screen_no_to_number(screen_no) in self._occupied_screen_nos
        )

    def get_single_free_screen(self, exclude=None):
        if exclude is None:
            exclude = []
        else:
            exclude = [self._screen_no_to_number(scrnno) for scrnno in exclude]
        with self._lock:
            if len(self._occupied_screen_nos) == self._maximum_num:
                self.logger.warning(
                    "Requesting free screen, but already using maximum number of screens."
                )
            screen_no = random.choice(
                [
                    i
                    for i in range(1, 10000)
                    if i not in self._occupied_screen_nos and i not in exclude
                ]
            )
            screen_no = self._number_to_screen_no(screen_no)
            return screen_no

    def get_multiple_free_screens(self, count):
        screens = []
        for _ in range(count):
            screens.append(self.get_single_free_screen(exclude=screens))
        return screens

    def get_free_screen(self, count=None):
        if count is None:
            return self.get_single_free_screen()
        else:
            return self.get_multiple_free_screens(count)

    def borrow_screen(self, screen_no=None, reuse=True, pop=True):
        with self._lock:
            if screen_no is None or screen_no == "":
                screen_no = self.get_single_free_screen()
            if not reuse:
                if self.is_inuse(screen_no):
                    raise KiwoomOpenApiPlusError(
                        "Borrowing screen %s, but it's already is use." % screen_no
                    )
                if len(self._occupied_screen_nos) == self._maximum_num:
                    self.logger.warning(
                        "Borrowing a screen, but already using maximum number of screens."
                    )
                    if pop:
                        oldest = self._occupied_screen_nos.popleft()
                        del self._borrow_count_by_screen_no[oldest]
                        self.logger.warning(
                            "Oldest screen %s popped.",
                            self._number_to_screen_no(oldest),
                        )
                    else:
                        raise KiwoomOpenApiPlusError("Cannot allocate more screen")
            screen_no_int = self._screen_no_to_number(screen_no)
            if not self.is_inuse(screen_no):
                self._occupied_screen_nos.append(screen_no_int)
            self._borrow_count_by_screen_no[screen_no_int] = (
                self._borrow_count_by_screen_no.get(screen_no_int, 0) + 1
            )
            if len(self._occupied_screen_nos) == self._maximum_num:
                self.logger.warning("Maximum number of screens reached.")
            return screen_no

    def return_screen(self, screen_no):
        try:
            with self._lock:
                screen_no_int = self._screen_no_to_number(screen_no)
                self._borrow_count_by_screen_no[screen_no_int] -= 1
                if self._borrow_count_by_screen_no[screen_no_int] == 0:
                    self._occupied_screen_nos.remove(
                        self._screen_no_to_number(screen_no)
                    )
                    del self._borrow_count_by_screen_no[screen_no_int]
            return True
        except (KeyError, ValueError):
            self.logger.warning("Returned screen %s, but not found.", screen_no)
            return False
