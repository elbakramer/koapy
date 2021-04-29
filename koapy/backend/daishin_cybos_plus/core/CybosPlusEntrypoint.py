import platform
import threading

import pywintypes
import win32com.client
from requests.structures import CaseInsensitiveDict

from koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin import (
    CybosPlusEntrypointMixin,
)
from koapy.backend.daishin_cybos_plus.core.CybosPlusError import CybosPlusRequestError
from koapy.backend.daishin_cybos_plus.core.CybosPlusRateLimiter import (
    CybosPlusLookupRequestRateLimiter,
    CybosPlusTradeRequestRateLimiter,
)


class CybosPlusDispatch:
    def __init__(self, entrypoint, progid):
        self._entrypoint = entrypoint
        self._progid = progid
        self._is_trade_related = progid.startswith("CpTrade.")

        self._dispatch = win32com.client.gencache.EnsureDispatch(progid)

        if self._is_trade_related:
            self._rate_limiter = self._entrypoint._trade_rate_limiter
        else:
            self._rate_limiter = self._entrypoint._lookup_rate_limiter

        self._error_checking_request_methods = {}
        self._rate_limited_request_methods = {}

        for name in ["BlockRequest", "BlockRequest2", "Request"]:
            if hasattr(self._dispatch, name):
                method = getattr(self._dispatch, name)
                if callable(method):
                    method = CybosPlusRequestError.wrap_to_check_code_or_raise(method)
                    self._error_checking_request_methods[
                        "ErrorChecking" + name
                    ] = method
                    method = self._rate_limiter(method)
                    self._rate_limited_request_methods["RateLimited" + name] = method

    def __getattr__(self, name):
        if hasattr(self._dispatch, name):
            return getattr(self._dispatch, name)
        elif name in self._rate_limited_request_methods:
            return self._rate_limited_request_methods[name]
        elif name in self._error_checking_request_methods:
            return self._error_checking_request_methods[name]
        else:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (type(self), name)
            )

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self._entrypoint, self._progid)


class CybosPlusIncompleteProgID:
    def __init__(self, entrypoint, prefix):
        self._entrypoint = entrypoint
        self._prefix = prefix

        self._cache = {}
        self._lock = threading.RLock()

    def __getattr__(self, name):
        if name not in self._cache:
            with self._lock:
                if name not in self._cache:
                    progid = "%s.%s" % (self._prefix, name)
                    try:
                        dispatch = CybosPlusDispatch(self._entrypoint, progid)
                    except pywintypes.com_error as e:
                        raise AttributeError(
                            "'%s' object has no attribute '%s'" % (type(self), name)
                        ) from e
                    self._cache[name] = dispatch
        return self._cache[name]

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self._entrypoint, self._prefix)


class CybosPlusEntrypoint(CybosPlusEntrypointMixin):

    """
    http://cybosplus.github.io/
    """

    def __init__(self):
        assert (
            platform.architecture()[0] == "32bit"
        ), "Contorl object should be created in 32bit environment"

        self._attribute_mapping = {
            "CpDib": "DsCbo1",
            "CpSysDib": "CpSysDib",
            "CpTrade": "CpTrade",
            "CpUtil": "CpUtil",
            "DsCbo1": "DsCbo1",
        }
        self._attribute_mapping = CaseInsensitiveDict(self._attribute_mapping)

        self._cache = {}
        self._lock = threading.RLock()

        self._lookup_rate_limiter = CybosPlusLookupRequestRateLimiter()
        self._trade_rate_limiter = CybosPlusTradeRequestRateLimiter()

    def __getattr__(self, name):
        if name not in self._attribute_mapping:
            raise AttributeError(
                "'%s' object has no attribute '%s'" % (type(self), name)
            )
        name = self._attribute_mapping[name]
        if name not in self._cache:
            with self._lock:
                if name not in self._cache:
                    self._cache[name] = CybosPlusIncompleteProgID(self, name)
        return self._cache[name]
