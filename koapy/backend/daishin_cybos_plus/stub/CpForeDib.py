from collections.abc import Iterator
from typing import Any, Callable, Union

from pythoncom import Empty, Missing
from pywintypes import IID, Time

from koapy.common import EventInstance


class IForeDib:
    CLSID = IID("{366798F0-BAC3-4F67-AAB0-0DB7F9EF021C}")

    def Request(self) -> None:
        ...

    def Subscribe(self) -> None:
        ...

    def Unsubscribe(self) -> None:
        ...

    def GetHeaderValue(self, _MIDL__IForeDib0000_: int) -> Any:
        ...

    def GetDataValue(self, _MIDL__IForeDib0001_: int, _MIDL__IForeDib0002_: int) -> Any:
        ...

    def GetInputValue(self, _MIDL__IForeDib0003_: int) -> Any:
        ...

    def SetInputValue(self, _MIDL__IForeDib0004_: int, newVal: Any) -> None:
        ...

    def GetDibStatus(self) -> int:
        ...

    def GetDibMsg1(self) -> str:
        ...

    def GetDibMsg2(self) -> str:
        ...

    def BlockRequest(self) -> int:
        ...

    def SubscribeLatest(self) -> None:
        ...

    def BlockRequest2(self, BlockOption: int) -> int:
        ...

    @property
    def Header(self) -> Any:
        ...

    @property
    def Data(self) -> Any:
        ...

    @property
    def Input(self) -> Any:
        ...

    @property
    def Continue(self) -> int:
        ...


class IForeDibEvents:
    CLSID = IID("{505ECBD8-8FA3-4BFB-B577-2134CE46245E}")

    @property
    def OnReceived(self) -> Union[EventInstance, Callable[[], None]]:
        ...


class IForeDibEventsHandler:
    CLSID = IID("{505ECBD8-8FA3-4BFB-B577-2134CE46245E}")

    def OnReceived(self) -> None:
        ...


class ICpForeField:
    CLSID = IID("{AB43E72A-E1FE-4EDE-B37A-3F75F1B3C026}")

    @property
    def Name(self) -> str:
        ...

    @property
    def fid(self) -> int:
        ...


class ICpForeFields:
    CLSID = IID("{1A154454-862E-4EA9-BE59-D63216EE6EFE}")

    def __call__(self, Index: int) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[Any]:
        ...


class CpForeField(ICpForeField):
    CLSID = IID("{93CEC1C0-47AE-474C-93BD-A952B67C5256}")


class CpForeFields(ICpForeFields):
    CLSID = IID("{EF426FAC-8B2F-4D4E-883F-42ADCA3D258C}")


class OvFutMst(IForeDib, IForeDibEvents):
    CLSID = IID("{60291C5F-0F0D-413F-A7E5-8FB699E8F050}")
    PROGID = "CpForeDib.OvFutMst.1"


class OvFutCur(IForeDib, IForeDibEvents):
    CLSID = IID("{10C45173-F22A-4037-AEF9-0A13BA3FA146}")
    PROGID = "CpForeDib.OvFutCur.1"


class OvFutBid(IForeDib, IForeDibEvents):
    CLSID = IID("{2117D620-501B-48F5-A6C0-2EA83A91453A}")
    PROGID = "CpForeDib.OvFutBid.1"


class FxMgMst(IForeDib, IForeDibEvents):
    CLSID = IID("{DFCAA3BE-2C51-4D22-8B40-8BD5A26987B9}")
    PROGID = "CpForeDib.FxMgMst.1"


class FxMgCur(IForeDib, IForeDibEvents):
    CLSID = IID("{1BA716D8-C71E-42B8-813D-F07BBDC08887}")
    PROGID = "CpForeDib.FxMgCur.1"


class FxMgOrdReceive(IForeDib, IForeDibEvents):
    CLSID = IID("{1BDD5625-B398-44EF-B81D-28F599E5F932}")
    PROGID = "CpForeDib.FxMgOrdReceive.1"


class FxMgConclusion(IForeDib, IForeDibEvents):
    CLSID = IID("{1593F7B5-6E9A-47D2-A121-0A370A363F64}")
    PROGID = "CpForeDib.FxMgConclusion.1"


class FxMgBalance(IForeDib, IForeDibEvents):
    CLSID = IID("{CDB1D9C6-C6DF-4004-8BB7-E6D282BBF938}")
    PROGID = "CpForeDib.FxMgBalance.1"


class OvFutOrdReceive(IForeDib, IForeDibEvents):
    CLSID = IID("{DF4AF880-ED67-4825-A61C-24D1E5D62BF1}")
    PROGID = "CpForeDib.OvFutOrdReceive.1"


class OvFutConclusion(IForeDib, IForeDibEvents):
    CLSID = IID("{F49DAF7B-8F8C-4EBA-A379-A7A8D7119152}")
    PROGID = "CpForeDib.OvFutConclusion.1"


class OvFutBalance(IForeDib, IForeDibEvents):
    CLSID = IID("{B5F48DBB-14A4-4346-966C-35187E1390B6}")
    PROGID = "CpForeDib.OvFutBalance.1"


class OvFutureChart(IForeDib, IForeDibEvents):
    CLSID = IID("{C5082D47-B750-4F6B-A71B-2FFF2BECEFB9}")
    PROGID = "CpForeDib.OvFutureChart.1"


class FxMgChart(IForeDib, IForeDibEvents):
    CLSID = IID("{13C7321A-77F2-46EA-8330-405553D0EB44}")
    PROGID = "CpForeDib.FxMgChart.1"
