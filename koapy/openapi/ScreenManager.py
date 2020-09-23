import random
import logging
import threading
import collections

class ScreenManager:

    _maximum_num = 200

    def __init__(self, control=None):
        self._control = control
        self._lock = threading.RLock()
        self._occupied_screen_nos = collections.deque(maxlen=self._maximum_num)

    @staticmethod
    def _number_to_screen_no(number):
        return str(number).zfill(4)

    @staticmethod
    def _screen_no_to_number(screen_no):
        return int(screen_no)

    def is_inuse(self, screen_no):
        return screen_no is not None and self._number_to_screen_no(screen_no) in self._occupied_screen_nos

    def ensure_not_using(self, screen_no):
        if screen_no is None or self.is_inuse(screen_no):
            raise ValueError
        return screen_no

    def ensure_not_using_or_get(self, screen_no):
        if screen_no is None:
            return self.get_single_free_screen()
        else:
            self.ensure_not_using(screen_no)
            return screen_no

    def get_single_free_screen(self, exclude=None):
        if exclude is None:
            exclude = []
        else:
            exclude = [self._screen_no_to_number(scrnno) for scrnno in exclude]
        with self._lock:
            if len(self._occupied_screen_nos) == self._maximum_num:
                logging.warning('Requesting free screen, but already using maximum number of screens.')
            screen_no = random.choice([i for i in range(1, 10000) if i not in self._occupied_screen_nos and i not in exclude])
            screen_no = self._number_to_screen_no(screen_no)
            return screen_no

    def get_multiple_free_screens(self, count):
        screens = []
        for _ in range(count):
            screens.append(self.get_single_free_screen(), screens)
        return screens

    def get_free_screen(self, count=None):
        if count is None:
            return self.get_single_free_screen()
        else:
            return self.get_multiple_free_screens(count)

    def borrow_screen(self, screen_no):
        with self._lock:
            if len(self._occupied_screen_nos) == self._maximum_num:
                logging.warning('Borrowing a screen, but already using maximum number of screens.')
                oldest = self._occupied_screen_nos.popleft()
                logging.warning('Oldest screen %s popped.', self._number_to_screen_no(oldest))
            screen_no = self.ensure_not_using_or_get(screen_no)
            self._occupied_screen_nos.append(self._screen_no_to_number(screen_no))
            if len(self._occupied_screen_nos) == self._maximum_num:
                logging.warning('Maximum number of screens reached.')
            return screen_no

    def return_screen(self, screen_no):
        try:
            with self._lock:
                self._occupied_screen_nos.remove(self._screen_no_to_number(screen_no))
            return True
        except ValueError:
            logging.warning('Returned screen %s, but not found.', screen_no)
            return False
