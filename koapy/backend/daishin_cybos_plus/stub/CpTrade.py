from collections.abc import Iterator
from typing import Any, Callable, Union

from pythoncom import Empty, Missing
from pywintypes import IID, Time

from koapy.common import EventInstance


class ICpTdUtil:
    CLSID = IID("{15CA8DD1-1CF9-4544-A1A4-5593CE63A845}")

    def TradeInit(self, Reserved: int = 0) -> int:
        ...

    def GoodsList(self, acc: str, Filter: int) -> Any:
        ...

    @property
    def AccountNumber(self) -> Any:
        ...


class ICpTdField:
    CLSID = IID("{E7BD5AF6-4EB1-47E1-BB3B-9505E2F09F0A}")

    @property
    def Name(self) -> str:
        ...

    @property
    def fid(self) -> int:
        ...


class ICpTdFields:
    CLSID = IID("{F3A9F36B-F36F-462C-B418-F4A31D8FE46F}")

    def __call__(self, Index: int) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[Any]:
        ...


class CpTdField(ICpTdField):
    CLSID = IID("{672A5C44-9446-4405-9F0E-1EA1FEFC29ED}")


class CpTdFields(ICpTdFields):
    CLSID = IID("{4AABFB5F-4AC0-41D5-9458-D670489A8B66}")


class ICpTdDib:
    CLSID = IID("{F75A3C47-4B29-46E8-AD1C-D34BD89B5143}")

    def GetHeaderValue(self, _MIDL__ICpTdDib0000_: int) -> Any:
        ...

    def GetDataValue(self, _MIDL__ICpTdDib0001_: int, _MIDL__ICpTdDib0002_: int) -> Any:
        ...

    def GetInputValue(self, _MIDL__ICpTdDib0003_: int) -> Any:
        ...

    def SetInputValue(self, _MIDL__ICpTdDib0004_: int, newVal: Any) -> None:
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


class ITdDibEvents:
    CLSID = IID("{8B55AD34-73A3-4C33-B8CD-C95ED13823CB}")

    @property
    def OnReceived(self) -> Union[EventInstance, Callable[[], None]]:
        ...


class ITdDibEventsHandler:
    CLSID = IID("{8B55AD34-73A3-4C33-B8CD-C95ED13823CB}")

    def OnReceived(self) -> None:
        ...


class CpTdUtil(ICpTdUtil):
    CLSID = IID("{1172DA0D-1235-4348-880B-10F95AC86E46}")
    PROGID = "CpTrade.CpTdUtil.1"


class CpTradeKey(ICpTdDib):
    CLSID = IID("{0CAA9637-7CAA-4A96-80D2-8CBEAFD66EEE}")


class CpTd0311(ICpTdDib, ITdDibEvents):
    CLSID = IID("{ACAD853E-9FA9-4165-9CE9-166BF4414AA3}")
    PROGID = "CpTrade.CpTd0311.1"


class CpTd5341(ICpTdDib, ITdDibEvents):
    CLSID = IID("{8203C86A-2282-4225-A79E-A9559357A3BC}")
    PROGID = "CpTrade.CpTd5341.1"


class CpTd5339(ICpTdDib, ITdDibEvents):
    CLSID = IID("{D82177A9-9AD3-4B30-9134-9C28BE43656D}")
    PROGID = "CpTrade.CpTd5339.1"


class CpTd0312(ICpTdDib, ITdDibEvents):
    CLSID = IID("{1497FD6D-0439-47BC-95B3-B838CD32D00F}")
    PROGID = "CpTrade.CpTd0312.1"


class CpTd0313(ICpTdDib, ITdDibEvents):
    CLSID = IID("{CB3DDA0D-E824-4008-8E69-CF168ABB6361}")
    PROGID = "CpTrade.CpTd0313.1"


class CpTd0303(ICpTdDib, ITdDibEvents):
    CLSID = IID("{A4B66D34-D296-477C-B4C2-3900810DF8F3}")
    PROGID = "CpTrade.CpTd0303.1"


class CpTd0314(ICpTdDib, ITdDibEvents):
    CLSID = IID("{15110F2E-4E3A-4921-AF52-EE6BF85AAD6E}")
    PROGID = "CpTrade.CpTd0314.1"


class CpTd6033(ICpTdDib, ITdDibEvents):
    CLSID = IID("{1E090CEF-B084-4961-93C3-92360F4D2226}")
    PROGID = "CpTrade.CpTd6033.1"


class CpTd5342(ICpTdDib, ITdDibEvents):
    CLSID = IID("{4E87EAB5-DB31-4FA6-AE19-47FFFE0672B9}")
    PROGID = "CpTrade.CpTd5342.1"


class CpTd0315(ICpTdDib, ITdDibEvents):
    CLSID = IID("{ED55E435-4C27-48A0-9033-309EF9D88E1F}")
    PROGID = "CpTrade.CpTd0315.1"


class CpTd0316(ICpTdDib, ITdDibEvents):
    CLSID = IID("{91875829-5FDE-4254-BA35-52272D546F8F}")
    PROGID = "CpTrade.CpTd0316.1"


class CpTd0306(ICpTdDib, ITdDibEvents):
    CLSID = IID("{0002AEE1-A91F-4CF8-AD84-13E5844EC471}")
    PROGID = "CpTrade.CpTd0306.1"


class CpTd0317(ICpTdDib, ITdDibEvents):
    CLSID = IID("{60D268EF-1D95-49B2-9E83-35B5DCD2A241}")
    PROGID = "CpTrade.CpTd0317.1"


class CpTd6740(ICpTdDib, ITdDibEvents):
    CLSID = IID("{F717B1BE-567C-4F55-A140-6E02FA7B8BD9}")


class CpTd6743R(ICpTdDib, ITdDibEvents):
    CLSID = IID("{F1BEF87C-30DC-424E-B5FC-01F1B5E10FED}")


class CpTd6750L(ICpTdDib, ITdDibEvents):
    CLSID = IID("{6B725C6E-D885-480B-B08C-D6AAF4BB76AC}")


class CpTd6751(ICpTdDib, ITdDibEvents):
    CLSID = IID("{138A98B2-BA82-4CB9-BFD1-5FD4AE078DDF}")


class CpTd6753(ICpTdDib, ITdDibEvents):
    CLSID = IID("{1C5CD253-54F6-4175-AD38-0F9BFE7B7B5A}")


class CpTd6754(ICpTdDib, ITdDibEvents):
    CLSID = IID("{233AA076-0DF8-47DA-BAED-A035138540F8}")


class CpTd6831(ICpTdDib, ITdDibEvents):
    CLSID = IID("{BB347FF1-D974-4A50-85FB-C751235AE061}")
    PROGID = "CpTrade.CpTd6831.1"


class CpTd6832(ICpTdDib, ITdDibEvents):
    CLSID = IID("{0BF841E1-849B-4AB9-8D85-5821458A437C}")
    PROGID = "CpTrade.CpTd6832.1"


class CpTd6833(ICpTdDib, ITdDibEvents):
    CLSID = IID("{6DCE8A22-6811-4399-9D34-B915D84F0727}")
    PROGID = "CpTrade.CpTd6833.1"


class CpTd5371(ICpTdDib, ITdDibEvents):
    CLSID = IID("{2370A08A-7AE8-4ADE-89A3-09477A941C1D}")
    PROGID = "CpTrade.CpTd5371.1"


class CpTd3811(ICpTdDib, ITdDibEvents):
    CLSID = IID("{EF56DD80-F726-4C1A-A5A8-12D30A2543EF}")
    PROGID = "CpTrade.CpTd3811.1"


class CpTd5372(ICpTdDib, ITdDibEvents):
    CLSID = IID("{BD6AF962-E715-4014-ADC7-7AE2132DB763}")
    PROGID = "CpTrade.CpTd5372.1"


class CpTd0723(ICpTdDib, ITdDibEvents):
    CLSID = IID("{F4294E75-719A-4728-A240-161773E1C964}")
    PROGID = "CpTrade.CpTd0723.1"


class CpTd6722(ICpTdDib, ITdDibEvents):
    CLSID = IID("{BE3394F1-4D4E-4508-923E-865CDAB9DCC8}")
    PROGID = "CpTrade.CpTd6722.1"


class CpTd6841(ICpTdDib, ITdDibEvents):
    CLSID = IID("{B6E99909-F65C-4DF9-9C0A-8EF2318610D0}")
    PROGID = "CpTrade.CpTd6841.1"


class CpTd6842(ICpTdDib, ITdDibEvents):
    CLSID = IID("{20A0CCAB-B4C8-4671-9624-AF420FCA1831}")
    PROGID = "CpTrade.CpTd6842.1"


class CpTd6843(ICpTdDib, ITdDibEvents):
    CLSID = IID("{97ABDC4A-3287-4D8C-822D-BB1476504E23}")
    PROGID = "CpTrade.CpTd6843.1"


class CpTd0322(ICpTdDib, ITdDibEvents):
    CLSID = IID("{BCF369E7-2657-4BD5-AE57-3E06A0FE461B}")
    PROGID = "CpTrade.CpTd0322.1"


class CpTd0326(ICpTdDib, ITdDibEvents):
    CLSID = IID("{BCB65B18-E3E5-4099-9070-B602D9B4BB42}")
    PROGID = "CpTrade.CpTd0326.1"


class CpTd0355(ICpTdDib, ITdDibEvents):
    CLSID = IID("{40A1A9C2-43E3-4BD8-A0A6-223C5BC5E86F}")
    PROGID = "CpTrade.CpTd0355.1"


class CpTd0356(ICpTdDib, ITdDibEvents):
    CLSID = IID("{C82BFF91-9F5C-400D-9B52-40BA3AC47F73}")
    PROGID = "CpTrade.CpTd0356.1"


class CpTdNew5331A(ICpTdDib, ITdDibEvents):
    CLSID = IID("{A01B00EA-B723-4F29-884E-F12F6760F248}")
    PROGID = "CpTrade.CpTdNew5331A.1"


class CpTdNew5331B(ICpTdDib, ITdDibEvents):
    CLSID = IID("{99EE8587-50FE-4520-8551-BEE017B3C16F}")
    PROGID = "CpTrade.CpTdNew5331B.1"


class CpTd6197(ICpTdDib, ITdDibEvents):
    CLSID = IID("{4DE84A1D-FB39-4B57-8E61-0216777A1B31}")
    PROGID = "CpTrade.CpTd6197.1"


class CpTd0386(ICpTdDib, ITdDibEvents):
    CLSID = IID("{A7984EA5-C50B-4DF3-A92C-7E6CC7AFB20A}")
    PROGID = "CpTrade.CpTd0386.1"


class CpTd0387(ICpTdDib, ITdDibEvents):
    CLSID = IID("{EB4C7EC4-5D99-454B-930C-12081EA02658}")
    PROGID = "CpTrade.CpTd0387.1"


class CpTd0389(ICpTdDib, ITdDibEvents):
    CLSID = IID("{C24DC073-D02C-409A-8358-C8BEB483BE41}")
    PROGID = "CpTrade.CpTd0389.1"


class CpTd9065(ICpTdDib, ITdDibEvents):
    CLSID = IID("{DA92E1FD-717F-4549-BB5C-90391302E84F}")
    PROGID = "CpTrade.CpTd9065.1"


class CpTd9081(ICpTdDib, ITdDibEvents):
    CLSID = IID("{8B8DA4AD-72A4-4D06-B249-90273D97CC14}")
    PROGID = "CpTrade.CpTd9081.1"


class CpTd9082(ICpTdDib, ITdDibEvents):
    CLSID = IID("{4C91160F-8C08-432D-A809-48A908D96016}")
    PROGID = "CpTrade.CpTd9082.1"


class CpTd9083(ICpTdDib, ITdDibEvents):
    CLSID = IID("{D44BB8E2-8E72-42E5-8B83-0D70E4338128}")
    PROGID = "CpTrade.CpTd9083.1"


class CpTd9084(ICpTdDib, ITdDibEvents):
    CLSID = IID("{D178011D-1CEB-4250-BB80-F9D42776BB46}")
    PROGID = "CpTrade.CpTd9084.1"


class CpTd9085(ICpTdDib, ITdDibEvents):
    CLSID = IID("{D585FF27-E7C3-484F-8F19-CAFF39CE0A49}")
    PROGID = "CpTrade.CpTd9085.1"


class CpTd0354(ICpTdDib, ITdDibEvents):
    CLSID = IID("{63A29BB8-469C-4965-B4E2-FC1A545E4E2B}")
    PROGID = "CpTrade.CpTd0354.1"


class CpTd0323(ICpTdDib, ITdDibEvents):
    CLSID = IID("{5BE98374-8EE2-4C9C-AF7A-46D33E12F476}")
    PROGID = "CpTrade.CpTd0323.1"


class CpTd0359(ICpTdDib, ITdDibEvents):
    CLSID = IID("{E476724F-D2F2-4BB9-86E5-C350891E4FB4}")
    PROGID = "CpTrade.CpTd0359.1"


class CpTd0388(ICpTdDib, ITdDibEvents):
    CLSID = IID("{C9410BA8-F7DB-4433-BEBA-670FC9D71C74}")
    PROGID = "CpTrade.CpTd0388.1"


class CpTd0721F(ICpTdDib, ITdDibEvents):
    CLSID = IID("{CE7160AC-297A-4274-9AEB-26F9D1312DF8}")
    PROGID = "CpTrade.CpTd0721F.1"


class CpTd0732(ICpTdDib, ITdDibEvents):
    CLSID = IID("{FCC8B385-6ABB-44E5-AD6C-78448F901895}")
    PROGID = "CpTrade.CpTd0732.1"


class CpTdNew9061(ICpTdDib, ITdDibEvents):
    CLSID = IID("{6C7B3B4E-7D8B-4598-AE1A-518E8FD459C2}")
    PROGID = "CpTrade.CpTdNew9061.1"


class CpTdNew9064(ICpTdDib, ITdDibEvents):
    CLSID = IID("{3AE88694-EAE6-4DDE-AB31-CA5A1408319B}")
    PROGID = "CpTrade.CpTdNew9064.1"


class CpTd3661(ICpTdDib, ITdDibEvents):
    CLSID = IID("{AB94158B-0724-46B5-985D-75D818856A56}")
    PROGID = "CpTrade.CpTd3661.1"


class CpTd3661D(ICpTdDib, ITdDibEvents):
    CLSID = IID("{9842E02C-187C-4B0B-9120-5D02FEB58474}")
    PROGID = "CpTrade.CpTd3661D.1"


class CmeOrder(ICpTdDib, ITdDibEvents):
    CLSID = IID("{FB214CC6-2265-4078-9405-FEF5D909B227}")
    PROGID = "cptrade.CmeOrder.1"


class CmeBalance(ICpTdDib, ITdDibEvents):
    CLSID = IID("{DEAC8F35-DD30-4C02-B105-9F558863D797}")
    PROGID = "cptrade.CmeBalance.1"


class CmeConclusion(ICpTdDib, ITdDibEvents):
    CLSID = IID("{F415CACE-CCFF-4F7A-8ACD-4C3045DDD2D1}")
    PROGID = "CpTrade.CmeConclusion.1"


class CmeNoConclusion(ICpTdDib, ITdDibEvents):
    CLSID = IID("{6C242F93-DE5E-4039-961F-4C116D74BE66}")
    PROGID = "CpTrade.CmeNoConclusion.1"


class EurexBalance(ICpTdDib, ITdDibEvents):
    CLSID = IID("{1D18474B-29CA-45B5-A3A5-A75B3593888B}")
    PROGID = "CpTrade.EurexBalance.1"


class EurexConclusion(ICpTdDib, ITdDibEvents):
    CLSID = IID("{47FA1A84-D56E-4AC7-A176-D9A2BCF01C72}")
    PROGID = "CpTrade.EurexConclusion.1"


class EurexNoConclusion(ICpTdDib, ITdDibEvents):
    CLSID = IID("{C822BB56-2BB3-412F-BFD7-9DE5E42E2A48}")
    PROGID = "CpTrade.EurexNoConclusion.1"


class EurexOrder(ICpTdDib, ITdDibEvents):
    CLSID = IID("{62055D8A-2A2C-482A-AB61-4B6808A6B95F}")
    PROGID = "cptrade.EurexOrder.1"


class CmeConclusionDay(ICpTdDib, ITdDibEvents):
    CLSID = IID("{2E24A4D5-749A-4E08-98B7-081897BF6612}")
    PROGID = "cptrade.CmeConclusionDay.1"


class EurexConclusionDay(ICpTdDib, ITdDibEvents):
    CLSID = IID("{81C12AD3-D154-4908-81FF-01C6D65A052E}")
    PROGID = "cptrade.EurexConclusionDay.1"


class CmeEurexProfitLoss(ICpTdDib, ITdDibEvents):
    CLSID = IID("{7163F543-C48D-4BF4-8CB9-723D1160C03A}")
    PROGID = "CpTrade.CmeEurexProfitLoss.1"


class CpTd9197(ICpTdDib, ITdDibEvents):
    CLSID = IID("{8BA40942-F695-44D4-A159-BBD40E92F35C}")
    PROGID = "CpTrade.CpTd9197.1"


class CpTd0711AtmAll(ICpTdDib, ITdDibEvents):
    CLSID = IID("{DED73E82-8BC5-44CF-8B68-6D4D0A629D4F}")
    PROGID = "cptrade.CpTd0711AtmAll.1"


class CpTd6128C(ICpTdDib, ITdDibEvents):
    CLSID = IID("{BB483629-435C-4852-AF05-7B37A80F7661}")
    PROGID = "cptrade.CpTd6128C.1"


class CpTd6128A(ICpTdDib, ITdDibEvents):
    CLSID = IID("{86551C2A-9893-4DB6-A917-AF2D048BA13A}")
    PROGID = "cptrade.CpTd6128A.1"


class CpTd6126(ICpTdDib, ITdDibEvents):
    CLSID = IID("{8D794BED-A116-471A-8298-AAB673C3CC58}")
    PROGID = "cptrade.CpTd6126.1"


class CpTd2034(ICpTdDib, ITdDibEvents):
    CLSID = IID("{8F3408DA-8936-4902-AA2D-13AFBEB2561A}")
    PROGID = "cptrade.CpTd2034.1"


class CpTd6032(ICpTdDib, ITdDibEvents):
    CLSID = IID("{F93732D1-FC68-4C04-A0F2-4A66971D581B}")
    PROGID = "cptrade.CpTd6032.1"
