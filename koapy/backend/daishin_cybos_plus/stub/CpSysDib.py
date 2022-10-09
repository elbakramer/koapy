from collections.abc import Iterator
from typing import Any, Callable, Union

from pythoncom import Empty, Missing
from pywintypes import IID, Time

from koapy.common import EventInstance


class ISysDib:
    CLSID = IID("{8146AC72-E93B-42A8-86A3-B9851AA15229}")

    def Request(self) -> None:
        ...

    def Subscribe(self) -> None:
        ...

    def Unsubscribe(self) -> None:
        ...

    def GetHeaderValue(self, _MIDL__ISysDib0000_: int) -> Any:
        ...

    def GetDataValue(self, _MIDL__ISysDib0001_: int, _MIDL__ISysDib0002_: int) -> Any:
        ...

    def GetInputValue(self, _MIDL__ISysDib0003_: int) -> Any:
        ...

    def SetInputValue(self, _MIDL__ISysDib0004_: int, newVal: Any) -> None:
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


class ISysDibEvents:
    CLSID = IID("{60D7702A-57BA-4869-AF3F-292FDC909D75}")

    @property
    def OnReceived(self) -> Union[EventInstance, Callable[[], None]]:
        ...


class ISysDibEventsHandler:
    CLSID = IID("{60D7702A-57BA-4869-AF3F-292FDC909D75}")

    def OnReceived(self) -> None:
        ...


class ICpField:
    CLSID = IID("{C9FAC560-BE19-4FB2-801D-54F89D3FBC0A}")

    @property
    def Name(self) -> str:
        ...

    @property
    def fid(self) -> int:
        ...


class ICpFields:
    CLSID = IID("{2A93E227-583D-427C-A430-2AB642C19E02}")

    def __call__(self, Index: int) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[Any]:
        ...


class CpField(ICpField):
    CLSID = IID("{BF085D15-ACE9-4E36-8E48-76BB29DA5584}")


class CpFields(ICpFields):
    CLSID = IID("{43733869-291F-43B0-B2EE-8019E7363B55}")


class ICpSys:
    CLSID = IID("{4BE681C3-67B8-4B6A-BC98-89FF0DF4238E}")

    def CpUnlock(self, code1: int, code2: int) -> None:
        ...


class CpSvrNew7224(ISysDib, ISysDibEvents):
    CLSID = IID("{E8931FA7-2E91-416F-85B8-F80351FD5C24}")
    PROGID = "CpSysDib.CpSvrNew7224.1"


class CpSvr3745(ISysDib, ISysDibEvents):
    CLSID = IID("{AF38F980-ABC8-4C99-8B95-19A1CC39ACB7}")
    PROGID = "CpSysDib.CpSvr3745.1"


class CpSvr7043(ISysDib, ISysDibEvents):
    CLSID = IID("{EA332802-B845-4C3D-8C3A-BBF6D0B11B79}")
    PROGID = "CpSysDib.CpSvr7043.1"


class CpSvr8548(ISysDib, ISysDibEvents):
    CLSID = IID("{DB6CADF4-515A-4845-BE7B-ECA2D93DAB26}")
    PROGID = "CpSysDib.CpSvr8548.1"


class CpSvrNew7221(ISysDib, ISysDibEvents):
    CLSID = IID("{942C11D6-2DA7-4119-8D4F-493F0623C1B7}")
    PROGID = "CpSysDib.CpSvrNew7221.1"


class CpSvrNew7221S(ISysDib, ISysDibEvents):
    CLSID = IID("{8A0FAF47-A6A1-4518-B66A-61B7143C389C}")
    PROGID = "CpSysDib.CpSvrNew7221S.1"


class CpSvrNew7216(ISysDib, ISysDibEvents):
    CLSID = IID("{6B0B7CB1-03BC-44CB-8768-79FFC699B41A}")
    PROGID = "CpSysDib.CpSvrNew7216.1"


class CpSvr8114(ISysDib, ISysDibEvents):
    CLSID = IID("{8DB220EA-04E0-4272-9AED-6B1550F6DBAB}")
    PROGID = "CpSysDib.CpSvr8114.1"


class CpSvr9842(ISysDib, ISysDibEvents):
    CLSID = IID("{79A10F99-442F-472D-8088-816B25F85523}")
    PROGID = "CpSysDib.CpSvr9842.1"


class CpSvr9842S(ISysDib, ISysDibEvents):
    CLSID = IID("{C6CE0564-B055-46AA-A406-DF1AF0A549C2}")
    PROGID = "CpSysDib.CpSvr9842S.1"


class CpMarketWatch(ISysDib, ISysDibEvents):
    CLSID = IID("{9FA37D6D-1E16-442C-8EDD-A3E423E8FEA1}")
    PROGID = "CpSysDib.CpMarketWatch.1"


class CpMarketWatchS(ISysDib, ISysDibEvents):
    CLSID = IID("{D6633FD4-D339-4782-B337-2A6C9ED3CA47}")
    PROGID = "CpSysDib.CpMarketWatchS.1"


class CpSvrNew7222(ISysDib, ISysDibEvents):
    CLSID = IID("{13173568-9547-4910-B040-9168A5DC950C}")
    PROGID = "CpSysDib.CpSvrNew7222.1"


class CpSvr7748(ISysDib, ISysDibEvents):
    CLSID = IID("{AF9498CB-FFBC-45FA-A5B5-3BE5E48146E5}")
    PROGID = "CpSysDib.CpSvr7748.1"


class ElwAll(ISysDib, ISysDibEvents):
    CLSID = IID("{061DCC2D-02E9-4F42-9090-3EACF821480B}")
    PROGID = "CpSysDib.ElwAll.1"


class Elw(ISysDib, ISysDibEvents):
    CLSID = IID("{49EC4E41-32D5-4994-8B0C-BC7AAB238E6A}")
    PROGID = "CpSysDib.Elw.1"


class ElwUnderCur(ISysDib, ISysDibEvents):
    CLSID = IID("{AE0BD6DB-C9C5-403B-AF49-7B953B362112}")
    PROGID = "CpSysDib.ElwUnderCur.1"


class ElwInvest(ISysDib, ISysDibEvents):
    CLSID = IID("{51BEC419-2C7F-456F-AF83-4E1E9C1F7543}")
    PROGID = "CpSysDib.ElwInvest.1"


class CpSvrNew7215A(ISysDib, ISysDibEvents):
    CLSID = IID("{4E793A3C-DFD4-499A-93F6-B2CEC3DC151B}")
    PROGID = "CpSysDib.CpSvrNew7215A.1"


class CpSvrNew7215B(ISysDib, ISysDibEvents):
    CLSID = IID("{BE5F7180-7E74-4F44-8C67-700811BAD363}")
    PROGID = "CpSysDib.CpSvrNew7215B.1"


class CpSvr7068(ISysDib, ISysDibEvents):
    CLSID = IID("{10674C56-4ACC-4104-BC8D-42F855EBA17D}")
    PROGID = "CpSysDib.CpSvr7068.1"


class CpSvr7063(ISysDib, ISysDibEvents):
    CLSID = IID("{C8C73E26-6C02-46CB-B8B6-1600E5A86A6B}")
    PROGID = "CpSysDib.CpSvr7063.1"


class ElwJpbid(ISysDib, ISysDibEvents):
    CLSID = IID("{75CCA696-16F2-459D-9F73-9EE5B92D60B3}")
    PROGID = "CpSysDib.ElwJpbid.1"


class ElwJpbid2(ISysDib, ISysDibEvents):
    CLSID = IID("{DAAF202A-393E-4353-A4EA-092733536C64}")
    PROGID = "CpSysDib.ElwJpbid2.1"


class CpSvr7066(ISysDib, ISysDibEvents):
    CLSID = IID("{42A23EE1-5CB9-4F9F-8467-208ED8602665}")
    PROGID = "CpSysDib.CpSvr7066.1"


class CpSvr7254(ISysDib, ISysDibEvents):
    CLSID = IID("{1B54A2E7-8F72-4825-B109-7E2DD61D6C8E}")
    PROGID = "CpSysDib.CpSvr7254.1"


class CpSvr3744(ISysDib, ISysDibEvents):
    CLSID = IID("{923667A7-245E-44E2-AB39-CB224F5B913E}")
    PROGID = "CpSysDib.CpSvr3744.1"


class StockAdj(ISysDib, ISysDibEvents):
    CLSID = IID("{EF251164-0FC9-4582-A6EE-7C6A3B981111}")
    PROGID = "CpSysDib.StockAdj.1"


class StockUniMst(ISysDib, ISysDibEvents):
    CLSID = IID("{7E291B7A-D229-4741-A8C1-C33B0DBBF6FB}")
    PROGID = "CpSysDib.StockUniMst.1"


class StockUniCur(ISysDib, ISysDibEvents):
    CLSID = IID("{DC573A7F-3301-47CE-B2F2-F36A1E5500B7}")
    PROGID = "CpSysDib.StockUniCur.1"


class StockUniJpBid(ISysDib, ISysDibEvents):
    CLSID = IID("{B7CC7EE7-C619-4D27-8EA9-03C2B0370ED0}")
    PROGID = "CpSysDib.StockUniJpBid.1"


class StockUniWeek(ISysDib, ISysDibEvents):
    CLSID = IID("{348306A3-8692-4758-AE08-883CF96B0B4C}")
    PROGID = "CpSysDib.StockUniWeek.1"


class StockUniBid(ISysDib, ISysDibEvents):
    CLSID = IID("{1C6B4381-B00C-4529-ABA1-FF705BFA342F}")
    PROGID = "CpSysDib.StockUniBid.1"


class OptionCurOnly(ISysDib, ISysDibEvents):
    CLSID = IID("{928A6FAF-3874-42D6-BCB6-74D65F758B35}")
    PROGID = "CpSysDib.OptionCurOnly.1"


class WorldCur(ISysDib, ISysDibEvents):
    CLSID = IID("{3D49364D-18D9-49A8-9B9F-7C5471EB129B}")
    PROGID = "CpSysDib.WorldCur.1"


class MarketEye(ISysDib, ISysDibEvents):
    CLSID = IID("{D71F9B56-85A0-49F8-B102-19C223ACF298}")
    PROGID = "CpSysDib.MarketEye.1"


class StockChart(ISysDib, ISysDibEvents):
    CLSID = IID("{4F5E5E9A-5BEA-409F-9828-B66A70B4B51B}")
    PROGID = "CpSysDib.StockChart.1"


class CpSvr7037(ISysDib, ISysDibEvents):
    CLSID = IID("{1AAC83CC-FA40-485F-952F-FB5667392E4F}")
    PROGID = "CpSysDib.CpSvr7037.1"


class K200Expect(ISysDib, ISysDibEvents):
    CLSID = IID("{39DADC73-104A-4C23-AC9B-9875B35EA194}")
    PROGID = "CpSysDib.K200Expect.1"


class FutOptChart(ISysDib, ISysDibEvents):
    CLSID = IID("{5337FA2B-B02E-42DC-A5A1-12BC4F36B6DA}")
    PROGID = "CpSysDib.FutOptChart.1"


class CpSvrNew7043(ISysDib, ISysDibEvents):
    CLSID = IID("{BC2B7C0D-8481-4067-B1A4-5D7BDCA9DCBA}")
    PROGID = "CpSysDib.CpSvrNew7043.1"


class CpSvrNew7212(ISysDib, ISysDibEvents):
    CLSID = IID("{DC43995C-F264-4ECA-B88A-20B4FD238DAF}")
    PROGID = "CpSysDib.CpSvrNew7212.1"


class CpSvr7726(ISysDib, ISysDibEvents):
    CLSID = IID("{23DEEA4C-FCF5-49B6-B1A8-07EF1D6D4AD4}")
    PROGID = "CpSysDib.CpSvr7726.1"


class CpFutOptTheoVal(ISysDib, ISysDibEvents):
    CLSID = IID("{FFE900B3-D906-492B-9AA1-C9411371C108}")
    PROGID = "CpSysDib.CpFutOptTheoVal.1"


class CpSvr7326(ISysDib, ISysDibEvents):
    CLSID = IID("{D9A23D4E-624D-43E8-9FDA-F9174A073209}")
    PROGID = "CpSysDib.CpSvr7326.1"


class StockOpenSb(ISysDib, ISysDibEvents):
    CLSID = IID("{F1AE467A-86BE-4F77-8A5C-F23D4883E3A7}")
    PROGID = "CpSysDib.StockOpenSb.1"


class CmeMst(ISysDib, ISysDibEvents):
    CLSID = IID("{9B08D6BE-4DE0-4F6A-B32A-22C9F0B182F7}")
    PROGID = "CpSysDib.CmeMst.1"


class CmeMo(ISysDib, ISysDibEvents):
    CLSID = IID("{8195B34A-E25A-4174-A41E-3283BFD0CBD6}")
    PROGID = "CpSysDib.CmeMo.1"


class CmeBid(ISysDib, ISysDibEvents):
    CLSID = IID("{E7FBCAA1-E01F-4CD5-B215-DB77D3AF5448}")
    PROGID = "CpSysDib.CmeBid.1"


class CmeDaily(ISysDib, ISysDibEvents):
    CLSID = IID("{09832FA6-1662-4EE3-9F91-6C8CD66EB3B2}")
    PROGID = "CpSysDib.CmeDaily.1"


class CmeBidOnly(ISysDib, ISysDibEvents):
    CLSID = IID("{2ADC5BB3-40A2-450C-A503-51084AD15D99}")
    PROGID = "CpSysDib.CmeBidOnly.1"


class CmeCurOnly(ISysDib, ISysDibEvents):
    CLSID = IID("{75FDB7F9-6B05-49E7-B7BD-80DA111FF3D5}")
    PROGID = "CpSysDib.CmeCurOnly.1"


class CmeCurr(ISysDib, ISysDibEvents):
    CLSID = IID("{70C14953-D33B-454B-856F-9464B7D7BAB5}")
    PROGID = "CpSysDib.CmeCurr.1"


class FutureJpBid(ISysDib, ISysDibEvents):
    CLSID = IID("{D14D1214-71D0-4207-9780-6DAC389EAE85}")
    PROGID = "CpSysDib.FutureJpBid.1"


class OptionJpBid(ISysDib, ISysDibEvents):
    CLSID = IID("{6D4EC009-130A-4C74-98D2-42B020889449}")
    PROGID = "CpSysDib.OptionJpBid.1"


class CWList(ISysDib, ISysDibEvents):
    CLSID = IID("{EDD5DE53-96D2-4F1D-BA3D-C6DF75154066}")
    PROGID = "CpSysDib.CWList.1"


class NStockMst(ISysDib, ISysDibEvents):
    CLSID = IID("{D3825EE2-C49F-4756-890D-530CDAA25EC5}")
    PROGID = "CpSysDib.NStockMst.1"


class NStockCur(ISysDib, ISysDibEvents):
    CLSID = IID("{3014C34B-46C3-4440-B6F5-93997817047B}")
    PROGID = "CpSysDib.NStockCur.1"


class BondMst(ISysDib, ISysDibEvents):
    CLSID = IID("{A0B46FA8-216D-47EB-A5DC-C500ACCEEA1A}")
    PROGID = "CpSysDib.BondMst.1"


class BondCur(ISysDib, ISysDibEvents):
    CLSID = IID("{3618D98B-BE61-4A46-9A2B-C6B38ECD2A09}")
    PROGID = "CpSysDib.BondCur.1"


class FOExpectCur(ISysDib, ISysDibEvents):
    CLSID = IID("{55D92823-F6CD-49FC-A3A8-9B4FAE025175}")
    PROGID = "CpSysDib.FOExpectCur.1"


class EurexBid(ISysDib, ISysDibEvents):
    CLSID = IID("{A45C67C3-53B6-4740-92AF-A04338D9215B}")
    PROGID = "CpSysDib.EurexBid.1"


class EurexDaily(ISysDib, ISysDibEvents):
    CLSID = IID("{A0696F58-8C6B-4E3B-8F7B-9EB4CC094EBB}")
    PROGID = "CpSysDib.EurexDaily.1"


class EurexCurOnly(ISysDib, ISysDibEvents):
    CLSID = IID("{3626A621-23F1-409F-BDD0-5AE10FF924E0}")
    PROGID = "CpSysDib.EurexCurOnly.1"


class EurexMst(ISysDib, ISysDibEvents):
    CLSID = IID("{65950801-9C94-4756-A92A-B20F319CDE2E}")
    PROGID = "CpSysDib.EurexMst.1"


class EurexJpbid(ISysDib, ISysDibEvents):
    CLSID = IID("{D07D7BAC-7FDD-4AA1-9FEB-156EC5344B8E}")
    PROGID = "CpSysDib.EurexJpbid.1"


class CpSvrNew7244S(ISysDib, ISysDibEvents):
    CLSID = IID("{5B6B6338-5843-4D9F-87BB-5C5BB40C579D}")
    PROGID = "CpSysDib.CpSvrNew7244S.1"


class CpSvrNew8300(ISysDib, ISysDibEvents):
    CLSID = IID("{D03AB487-0553-4F48-8DAA-C7A8C1549B11}")
    PROGID = "CpSysDib.CpSvrNew8300.1"


class CssStgList(ISysDib, ISysDibEvents):
    CLSID = IID("{B9CB3A84-F66B-4FB0-A481-C9CCC8B8AE1F}")
    PROGID = "CpSysDib.CssStgList.1"


class CssStgFind(ISysDib, ISysDibEvents):
    CLSID = IID("{60E404D1-AA50-4AC9-BC86-476626CBC983}")
    PROGID = "CpSysDib.CssStgFind.1"


class CssWatchStgControl(ISysDib, ISysDibEvents):
    CLSID = IID("{6F6615F0-DA4A-4E5F-8E74-F3597F9D6865}")
    PROGID = "CpSysDib.CssWatchStgControl.1"


class CssWatchStgSubscribe(ISysDib, ISysDibEvents):
    CLSID = IID("{7F5AF5D2-2C13-4E84-92E4-9298F1436756}")
    PROGID = "CpSysDib.CssWatchStgSubscribe.1"


class CssAlert(ISysDib, ISysDibEvents):
    CLSID = IID("{37001E74-5FAA-4502-94FA-3AE9FC102DEB}")
    PROGID = "CpSysDib.CssAlert.1"


class CpSvr7921(ISysDib, ISysDibEvents):
    CLSID = IID("{435AC599-969D-46A0-B119-6D7C4C7F5AB7}")
    PROGID = "CpSysDib.CpSvr7921.1"


class CpSvr8119S(ISysDib, ISysDibEvents):
    CLSID = IID("{02762DC2-93FA-48CA-897C-DAE7D68514AB}")
    PROGID = "CpSysDib.CpSvr8119S.1"


class CpSvr9619S(ISysDib, ISysDibEvents):
    CLSID = IID("{772812D7-6F16-41C5-9E4A-95955F9203DC}")
    PROGID = "CpSysDib.CpSvr9619S.1"


class CpSvr7033(ISysDib, ISysDibEvents):
    CLSID = IID("{EF88BBDC-8403-41C7-9FA1-2E0B5D52FEB4}")
    PROGID = "CpSysDib.CpSvr7033.1"


class CpSvr7034(ISysDib, ISysDibEvents):
    CLSID = IID("{AAFD418D-0D1A-41C1-9E70-E91962002932}")
    PROGID = "CpSysDib.CpSvr7034.1"


class CpSvr7236(ISysDib, ISysDibEvents):
    CLSID = IID("{100A7E1E-1B72-4622-A4CF-FFBA1336A30C}")
    PROGID = "CpSysDib.CpSvr7236.1"


class CpSvr2221(ISysDib, ISysDibEvents):
    CLSID = IID("{C3DE1C2F-54FE-4B1E-B433-4F42A4929618}")
    PROGID = "CpSysDib.CpSvr2221.1"


class CpSvr7238(ISysDib, ISysDibEvents):
    CLSID = IID("{62FBF818-C088-40C1-9B6E-D7CBA632405C}")
    PROGID = "CpSysDib.CpSvr7238.1"


class CpSvr7151(ISysDib, ISysDibEvents):
    CLSID = IID("{250EDB54-764B-4015-979A-2B1819C8F4BA}")
    PROGID = "CpSysDib.CpSvr7151.1"


class CpSvr7240(ISysDib, ISysDibEvents):
    CLSID = IID("{3438271B-2E14-4DCB-B64A-CAD75B5016C5}")
    PROGID = "CpSysDib.CpSvr7240.1"


class CpSvr7210d(ISysDib, ISysDibEvents):
    CLSID = IID("{A92FDBCE-E9F7-425D-8FB7-3ACCDE09264F}")
    PROGID = "CpSysDib.CpSvr7210d.1"


class CpSvr7210T(ISysDib, ISysDibEvents):
    CLSID = IID("{249A0E5B-2FB1-4762-96DE-D7D0C7927796}")
    PROGID = "CpSysDib.CpSvr7210T.1"


class CpSvr8241(ISysDib, ISysDibEvents):
    CLSID = IID("{0F5B7F6F-A5B6-4296-94DB-98373EEE1598}")
    PROGID = "CpSysDib.CpSvr8241.1"


class CpSvr7049(ISysDib, ISysDibEvents):
    CLSID = IID("{D44D2789-F23F-4E3D-959C-E6A399413492}")
    PROGID = "CpSysDib.CpSvr7049.1"


class FutStockMst(ISysDib, ISysDibEvents):
    CLSID = IID("{302903C9-49D8-4D47-9A3F-A2FA150350E7}")
    PROGID = "CpSysDib.FutStockMst.1"


class FutStockCurS(ISysDib, ISysDibEvents):
    CLSID = IID("{0651A2B7-0F47-4233-ACBF-DDEFA06C57E9}")
    PROGID = "CpSysDib.FutStockCurS.1"


class FutStockWeek(ISysDib, ISysDibEvents):
    CLSID = IID("{C8F097B8-BF52-419B-8430-084B596B4AD3}")
    PROGID = "CpSysDib.FutStockWeek.1"


class CpSvr9841(ISysDib, ISysDibEvents):
    CLSID = IID("{5A7EB1B7-BDB3-45E6-9CAA-A75F8C534685}")
    PROGID = "CpSysDib.CpSvr9841.1"
