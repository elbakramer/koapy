from collections.abc import Iterator
from typing import Any, Callable, Union

from pythoncom import Empty, Missing
from pywintypes import IID, Time

from koapy.common import EventInstance


class ICpForeTdUtil:
    CLSID = IID("{1427FCED-19F3-4433-90FC-15F92272F6A7}")

    def TradeInit(self, Reserved: int = 0) -> int:
        ...

    def GoodsList(self, acc: str, Filter: int) -> Any:
        ...

    @property
    def AccountNumber(self) -> Any:
        ...


class ICpTdField:
    CLSID = IID("{9B522D78-88D9-4D5F-A4E0-16A936830F43}")

    @property
    def Name(self) -> str:
        ...

    @property
    def fid(self) -> int:
        ...


class ICpTdFields:
    CLSID = IID("{75081DAF-290E-4036-B49D-9C45A990E96F}")

    def __call__(self, Index: int) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[Any]:
        ...


class CpTdField(ICpTdField):
    CLSID = IID("{138DF993-B1BB-4E51-8C71-6248B9C010C4}")


class CpTdFields(ICpTdFields):
    CLSID = IID("{8C150715-212A-453E-AC5A-1A1183B0A36F}")


class ICpForeTdDib:
    CLSID = IID("{18F5F66F-7DC7-4394-B025-5B981C3838F5}")

    def GetHeaderValue(self, _MIDL__ICpForeTdDib0000_: int) -> Any:
        ...

    def GetDataValue(
        self, _MIDL__ICpForeTdDib0001_: int, _MIDL__ICpForeTdDib0002_: int
    ) -> Any:
        ...

    def GetInputValue(self, _MIDL__ICpForeTdDib0003_: int) -> Any:
        ...

    def SetInputValue(self, _MIDL__ICpForeTdDib0004_: int, newVal: Any) -> None:
        ...

    def GetDibStatus(self) -> int:
        ...

    def GetDibMsg1(self) -> str:
        ...

    def GetDibMsg2(self) -> str:
        ...

    def BlockRequest(self) -> int:
        ...

    def BlockRequest2(self, BlockOption: int) -> int:
        ...

    def Request(self) -> int:
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

    @Continue.setter
    def Continue(self, Continue: int) -> None:
        ...


class IForeTdDibEvents:
    CLSID = IID("{EC430179-1510-4E67-96EA-376C4759E928}")

    @property
    def OnReceived(self) -> Union[EventInstance, Callable[[], None]]:
        ...


class IForeTdDibEventsHandler:
    CLSID = IID("{EC430179-1510-4E67-96EA-376C4759E928}")

    def OnReceived(self) -> None:
        ...


class CpForeTdUtil(ICpForeTdUtil):
    CLSID = IID("{D99B83AA-06D4-4944-81BC-7B18C0FCC491}")
    PROGID = "CpForeTrade.CpForeTdUtil.1"


class CpForeTradeKey(ICpForeTdDib):
    CLSID = IID("{31A04D10-E36E-4571-A058-B5FFD650E269}")


class OvFutOrder(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{CF80E93D-C153-404F-8728-DE2B2C259B92}")
    PROGID = "CpForeTrade.OvFutOrder.1"


class OvFutConInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{A03A1CC0-0DD3-4CB6-9DEB-5942013547C9}")
    PROGID = "CpForeTrade.OvFutConInq.1"


class OvFutNotConInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{ECD09FE2-F364-40CE-84D4-0519789852E8}")
    PROGID = "CpForeTrade.OvFutNotConInq.1"


class OvfNotPaymentInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{87C0CF3C-BD04-43C7-A769-258F6ECD4E95}")
    PROGID = "CpForeTrade.OvfNotPaymentInq.1"


class OvfDepositRecInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{EA07EC46-90D7-4FDA-86AB-B9E18FE20B97}")
    PROGID = "CpForeTrade.OvfDepositRecInq.1"


class FxMgOrder(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{EA025F0D-E04D-43E8-B2AD-FB136B7D871A}")
    PROGID = "CpForeTrade.OvFutOrder.1"


class FxMgConInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{35BA0F1E-9483-4A7E-945C-2106D99B86F1}")
    PROGID = "CpForeTrade.FxMgConInq.1"


class FxMgNotConInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{D78F80D3-7189-45B1-9D41-40323059E330}")
    PROGID = "CpForeTrade.FxMgNotConInq.1"


class FxMgNotPaymentInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{46131954-6A5A-43B8-94B2-63056A75171C}")
    PROGID = "CpForeTrade.FxMgNotPaymentInq.1"


class FxMgDepositRecInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{65210B9E-4F64-419A-AB4E-A41FD1202943}")
    PROGID = "CpForeTrade.FxMgDepositRecInq.1"


class OvfOffDepositRecInq(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{1FF05E16-3C49-49F1-A8C9-A6AFB5E89162}")
    PROGID = "CpForeTrade.OvfOffDepositRecInq.1"


class CpTd6345(ICpForeTdDib, IForeTdDibEvents):
    CLSID = IID("{9DFA90BB-7BD9-4F2A-8777-34CB94781FBF}")
    PROGID = "CpForeTrade.CpTd6345.1"
