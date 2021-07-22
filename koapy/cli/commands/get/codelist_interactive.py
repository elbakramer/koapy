import curses
import curses.ascii
import logging
import unicodedata

import pygtrie

from koapy import KiwoomOpenApiPlusEntrypoint
from koapy.utils.logging.Logging import Logging


class MarketEntry:
    def __init__(self, code, name):
        self.code = code
        self.name = name
        self.stocks = []

    def to_string(self):
        return "[{:2}] {}".format(self.code, self.name)


class StockEntry:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def to_string(self):
        return "[{}] {}".format(self.code, self.name)


markets = [
    MarketEntry(0, "KOSPI"),
    MarketEntry(10, "KOSDAQ"),
    MarketEntry(3, "ELW"),
    MarketEntry(8, "ETF"),
    MarketEntry(50, "KONEX"),
    MarketEntry(4, "MUTUAL FUND"),
    MarketEntry(5, "RIGHTS OFFERING"),
    MarketEntry(6, "REITS"),
    MarketEntry(9, "HIGH YIELD FUND"),
    MarketEntry(30, "K-OTC"),
]


class StatusBarHandler(logging.Handler):
    def __init__(self, screen, level=logging.NOTSET):
        super().__init__(level)
        self._screen = screen

    def emit(self, record):
        self._screen.set_footer_bar(record.getMessage())


def screen_len(str):
    l = 0
    for c in str:
        if unicodedata.east_asian_width(c) in ["F", "W"]:
            l += 2
        else:
            l += 1
    return l


class Screen:
    def __init__(self, screen):
        self._screen = screen

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        self._screen.clear()
        self._screen.refresh()

        self._height, self._width = self._screen.getmaxyx()

        self._header_bar = curses.newwin(1, self._width, 0, 0)
        self._header_bar.attron(curses.A_REVERSE)
        self._header_bar_prefix = ">>> "
        self._header_bar_text = self._header_bar_prefix
        self._pad = curses.newpad(0, self._width)
        self._footer_bar = curses.newwin(1, self._width, self._height - 1, 0)
        self._footer_bar.attron(curses.A_REVERSE)
        self._footer_text = ""

        self._exit_key = ord("q")

        self.refresh_header_bar()
        self.set_footer_bar("Logs will appear here...")

        self._handler = StatusBarHandler(self)
        self._logger = Logging.get_logger("koapy")
        self._logger.addHandler(self._handler)

        self._entrypoint = KiwoomOpenApiPlusEntrypoint()
        self._entrypoint.EnsureConnected()

    def refresh_header_bar(self):
        self._height, self._width = self._screen.getmaxyx()
        self._header_bar.resize(1, self._width)
        self._header_bar.mvwin(0, 0)
        self._header_bar.addstr(0, 0, self._header_bar_text.ljust(self._width - 1))
        self._screen.move(0, screen_len(self._header_bar_text))
        self._header_bar.refresh()

    def set_header_bar(self, text):
        self._header_bar_text = self._header_bar_prefix + text
        self.refresh_header_bar()

    def refresh_footer_bar(self):
        self._height, self._width = self._screen.getmaxyx()
        self._footer_bar.resize(1, self._width)
        self._footer_bar.mvwin(self._height - 1, 0)
        self._footer_bar.addstr(0, 0, self._footer_text.ljust(self._width - 1))
        self._footer_bar.refresh()

    def set_footer_bar(self, text):
        self._footer_text = text
        self.refresh_footer_bar()

    def show_entries(self, entries):
        trie = pygtrie.CharTrie()
        for entry in entries:
            trie[str(entry.code)] = entry
            trie[entry.name] = entry
        original_entries = entries
        current_entries = original_entries
        k = 0
        cursor_y = 0
        scroll_y = 0
        query = ""
        while k not in [curses.ascii.ESC, curses.KEY_LEFT]:
            self.set_header_bar(query)
            self.refresh_footer_bar()
            self._height, self._width = self._screen.getmaxyx()
            pad_height = self._height - 2
            pad_width = self._width
            self._pad.resize(len(current_entries), pad_width)
            self._pad.clear()
            if k == curses.KEY_DOWN:
                cursor_y = cursor_y + 1
            elif k == curses.KEY_UP:
                cursor_y = cursor_y - 1
            elif k == curses.KEY_PPAGE:
                prev_scroll_y = scroll_y
                scroll_y = max(scroll_y - pad_height, 0)
                cursor_y -= prev_scroll_y - scroll_y
            elif k == curses.KEY_NPAGE:
                prev_scroll_y = scroll_y
                scroll_y = min(
                    scroll_y + pad_height, len(current_entries) - 1 - pad_height
                )
                scroll_y = max(0, scroll_y)
                cursor_y += scroll_y - prev_scroll_y
            elif k == curses.KEY_RIGHT:
                if len(current_entries) > 0:
                    entry = current_entries[cursor_y]
                    if hasattr(entry, "stocks"):
                        market = entry
                        if len(market.stocks) == 0:
                            stock_codes = self._entrypoint.GetCodeListByMarketAsList(
                                market.code
                            )
                            stock_names = [
                                self._entrypoint.GetMasterCodeName(code)
                                for code in stock_codes
                            ]
                            stocks = [
                                StockEntry(code, name)
                                for code, name in zip(stock_codes, stock_names)
                            ]
                            market.stocks = stocks
                        self._pad.clear()
                        self._pad.refresh(0, 0, 1, 0, pad_height, pad_width - 1)
                        self.show_entries(market.stocks)
                        self._pad.clear()
                        self._pad.refresh(0, 0, 1, 0, pad_height, pad_width - 1)
                        k = 0
                        continue
            elif k in [curses.KEY_BACKSPACE, 8]:
                if len(query) > 0:
                    query = query[:-1]
                    self.set_header_bar(query)
                if len(query) > 0:
                    if trie.has_key(query) or trie.has_subtrie(query):
                        current_entries = trie.values(query)
                else:
                    current_entries = original_entries
                self._pad.clear()
                self._pad.refresh(0, 0, 1, 0, pad_height, pad_width - 1)
                k = 0
                continue
            elif unicodedata.category(chr(k))[0] != "C":
                query += chr(k)
                self.set_header_bar(query)
                if trie.has_key(query) or trie.has_subtrie(query):
                    current_entries = trie.values(query)
                else:
                    current_entries = []
                self._pad.clear()
                self._pad.refresh(0, 0, 1, 0, pad_height, pad_width - 1)
                k = 0
                continue
            cursor_y = min(len(current_entries) - 1, cursor_y)
            cursor_y = max(0, cursor_y)
            if k == curses.KEY_DOWN:
                if cursor_y == (scroll_y + pad_height - 9):
                    scroll_y = cursor_y - pad_height + 10
                elif cursor_y > (scroll_y + pad_height - 2):
                    scroll_y = cursor_y - pad_height + 1
            elif k == curses.KEY_UP:
                if cursor_y == scroll_y + 8:
                    scroll_y = cursor_y - 9
                elif cursor_y < scroll_y:
                    scroll_y = cursor_y
            scroll_y = min(len(current_entries) - 1, scroll_y)
            scroll_y = max(0, scroll_y)
            for i, market in enumerate(current_entries):
                attr = 0
                if i == cursor_y:
                    attr = curses.A_UNDERLINE
                self._pad.addstr(i, 0, market.to_string().ljust(pad_width - 1), attr)
            self._pad.refresh(scroll_y, 0, 1, 0, pad_height, pad_width - 1)
            k = self._screen.getch()


def wrapper(stdscr):
    screen = Screen(stdscr)
    screen.show_entries(markets)


def codelist_interactive():
    curses.wrapper(wrapper)


def main():
    codelist_interactive()


if __name__ == "__main__":
    main()
