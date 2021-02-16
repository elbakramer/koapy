import threading

import win32com.client
import pywintypes

from requests.structures import CaseInsensitiveDict

from koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin import CybosPlusEntrypointMixin
from koapy.backend.daishin_cybos_plus.core.CybosPlusError import CybosPlusRequestError

from koapy.backend.daishin_cybos_plus.core.CybosPlusRateLimiter import CybosPlusLookupRequestRateLimiter
from koapy.backend.daishin_cybos_plus.core.CybosPlusRateLimiter import CybosPlusTradeRequestRateLimiter

class CybosPlusDispatch:

    def __init__(self, entrypoint, progid):
        self._entrypoint = entrypoint
        self._progid = progid
        self._is_trade_related = progid.startswith('CpTrade.')

        self._dispatch = win32com.client.gencache.EnsureDispatch(progid)

        if self._is_trade_related:
            self._rate_limiter = self._entrypoint._trade_rate_limiter
        else:
            self._rate_limiter = self._entrypoint._lookup_rate_limiter

        self._request_method_names = ['BlockRequest', 'BlockRequest2', 'Request']

        for method_name in self._request_method_names:
            if hasattr(self, method_name):
                new_method_name = 'RateLimited' + method_name
                method = getattr(self, method_name)
                method = self._rate_limiter(method)
                setattr(self, new_method_name, method)

    def __getattr__(self, name):
        result = getattr(self._dispatch, name)
        if name in self._request_method_names and callable(result):
            result = CybosPlusRequestError.make_check_code_or_raise(result)
        return result

    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__, self._entrypoint, self._progid, self._is_trade_related)

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
                    progid = '%s.%s' % (self._prefix, name)
                    try:
                        dispatch = CybosPlusDispatch(self._entrypoint, progid)
                    except pywintypes.com_error as e:
                        raise AttributeError("'%s' object has no attribute '%s'" % (type(self), name), e)
                    self._cache[name] = dispatch
        return self._cache[name]

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self._entrypoint, self._prefix)

class CybosPlusEntrypoint(CybosPlusEntrypointMixin):

    """
    http://cybosplus.github.io/
    """

    def __init__(self):
        self._attribute_mapping = {
            'CpDib': 'DsCbo1',
            'CpSysDib': 'CpSysDib',
            'CpTrade': 'CpTrade',
            'CpUtil': 'CpUtil',
            'DsCbo1': 'DsCbo1',
        }
        self._attribute_mapping = CaseInsensitiveDict(self._attribute_mapping)

        self._cache = {}
        self._lock = threading.RLock()

        self._lookup_rate_limiter = CybosPlusLookupRequestRateLimiter()
        self._trade_rate_limiter = CybosPlusTradeRequestRateLimiter()

    def __getattr__(self, name):
        if name not in self._attribute_mapping:
            raise AttributeError("'%s' object has no attribute '%s'" % (type(self), name))
        name = self._attribute_mapping[name]
        if name not in self._cache:
            with self._lock:
                if name not in self._cache:
                    self._cache[name] = CybosPlusIncompleteProgID(self, name)
        return self._cache[name]
