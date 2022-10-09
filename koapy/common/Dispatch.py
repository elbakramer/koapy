import types

from typing import Union

from pythoncom import ProgIDFromCLSID
from pythoncom import com_error as PythonComError
from pywintypes import IID
from win32com.client import getevents as GetEvents
from win32com.client.gencache import EnsureDispatch

from koapy.common.EventInstance import EventInstance


class Dispatch:
    def __init__(self, clsid: Union[IID, str]):
        if isinstance(clsid, str):
            clsid = IID(clsid)

        self._clsid = clsid
        self._disp = EnsureDispatch(self._clsid)
        self._events_class = GetEvents(self._clsid)

        if self._events_class:

            def exec_body(ns):
                # pylint: disable=protected-access
                for name in self._events_class._dispid_to_func_.values():
                    ns[name] = EventInstance()

            self._user_event_class = types.new_class(
                name="UserDispatchEventClass",
                bases=(),
                kwds={},
                exec_body=exec_body,
            )
            self._result_class = types.new_class(
                name="DispatchEventClass",
                bases=(self._events_class, self._user_event_class),
                kwds={},
            )

            self._disp_events = self._result_class(self._disp)

            if hasattr(self._user_event_class, "__init__"):
                # pylint: disable=non-parent-init-called
                self._user_event_class.__init__(self._disp_events)
        else:
            self._disp_events = None

    def __del__(self):
        if (
            "_disp_events" in self.__dict__
            and self.__dict__["_disp_events"] is not None
        ):
            try:
                self.__dict__["_disp_events"].close()
            except PythonComError:
                pass

    def __getattr__(self, name):
        if "_disp" in self.__dict__ and hasattr(self.__dict__["_disp"], name):
            return getattr(self.__dict__["_disp"], name)
        if "_disp_events" in self.__dict__ and hasattr(
            self.__dict__["_disp_events"], name
        ):
            return getattr(self.__dict__["_disp_events"], name)
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            return super().__setattr__(name, value)
        if "_disp" in self.__dict__ and hasattr(self.__dict__["_disp"], name):
            return setattr(self.__dict__["_disp"], name, value)
        return super().__setattr__(name, value)

    def __dir__(self):
        res = super().__dir__()
        res = set(res)
        if "_disp" in self.__dict__:
            disp_dir = dir(self.__dict__["_disp"])
            res = res.union(set(disp_dir))
        if "_disp_events" in self.__dict__:
            disp_events_dir = dir(self.__dict__["_disp_events"])
            res = res.union(set(disp_events_dir))
        res = list(res)
        return res

    def __repr__(self):
        class_name = self.__class__.__name__
        progid = ProgIDFromCLSID(self._clsid)
        return f"{class_name}({progid!r})"
