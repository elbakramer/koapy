from collections.abc import Iterator
from typing import Any, Callable, Union

from pythoncom import Empty, Missing
from pywintypes import IID, Time

from koapy.common import EventInstance


class IDib:
    CLSID = IID("{33518A10-0931-11D4-8231-00105A7C4F8C}")

    def Request(self) -> None:
        ...

    def Subscribe(self) -> None:
        ...

    def Unsubscribe(self) -> None:
        ...

    def GetHeaderValue(self, _MIDL__IDib0000_: int) -> Any:
        ...

    def GetDataValue(self, _MIDL__IDib0001_: int, _MIDL__IDib0002_: int) -> Any:
        ...

    def GetInputValue(self, _MIDL__IDib0003_: int) -> Any:
        ...

    def SetInputValue(self, _MIDL__IDib0004_: int, newVal: Any) -> None:
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


class IDibEvents:
    CLSID = IID("{B8944520-09C3-11D4-8232-00105A7C4F8C}")

    @property
    def OnReceived(self) -> Union[EventInstance, Callable[[], None]]:
        ...


class IDibEventsHandler:
    CLSID = IID("{B8944520-09C3-11D4-8232-00105A7C4F8C}")

    def OnReceived(self) -> None:
        ...


class ICpField:
    CLSID = IID("{85934404-08FD-11D4-8231-00105A7C4F8C}")

    @property
    def Name(self) -> str:
        ...

    @property
    def fid(self) -> int:
        ...


class ICpFields:
    CLSID = IID("{55D0C6E4-0966-11D4-8232-00105A7C4F8C}")

    def __call__(self, Index: int) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[Any]:
        ...


class CpField(ICpField):
    CLSID = IID("{85934405-08FD-11D4-8231-00105A7C4F8C}")


class CpFields(ICpFields):
    CLSID = IID("{55D0C6E5-0966-11D4-8232-00105A7C4F8C}")


class StockMst(IDib, IDibEvents):
    CLSID = IID("{9FF543E2-FB11-11D3-8224-00105A7C4F8C}")
    PROGID = "Dscbo1.StockMst.1"


class StockCur(IDib, IDibEvents):
    CLSID = IID("{55D0C6E7-0966-11D4-8232-00105A7C4F8C}")
    PROGID = "Dscbo1.StockCur.1"


class StockBid(IDib, IDibEvents):
    CLSID = IID("{D6122124-0B4C-11D4-8234-00105A7C4F8C}")
    PROGID = "Dscbo1.StockBid.1"


class StockFrnord(IDib, IDibEvents):
    CLSID = IID("{48096137-0B62-11D4-8234-00105A7C4F8C}")
    PROGID = "Dscbo1.StockFrnord.1"


class StockJpbid(IDib, IDibEvents):
    CLSID = IID("{4809613A-0B62-11D4-8234-00105A7C4F8C}")
    PROGID = "Dscbo1.StockJpbid.1"


class StockJpbid2(IDib, IDibEvents):
    CLSID = IID("{4809613F-0B62-11D4-8234-00105A7C4F8C}")
    PROGID = "Dscbo1.StockJpbid2.1"


class StockCbchk(IDib, IDibEvents):
    CLSID = IID("{5B886BA4-0B8E-11D4-8235-00105A7C4F8C}")
    PROGID = "Dscbo1.StockCbchk.1"


class StockMember(IDib, IDibEvents):
    CLSID = IID("{02CAF55C-0C31-11D4-8236-00105A7C4F8C}")
    PROGID = "Dscbo1.StockMember.1"


class StockMember1(IDib, IDibEvents):
    CLSID = IID("{02CAF560-0C31-11D4-8236-00105A7C4F8C}")
    PROGID = "Dscbo1.StockMember1.1"


class StockWeek(IDib, IDibEvents):
    CLSID = IID("{7C79B1F6-0E74-11D4-823A-00105A7C4F8C}")
    PROGID = "Dscbo1.StockWeek.1"


class CbGraph1(IDib, IDibEvents):
    CLSID = IID("{8A1D75A5-0F42-11D4-823D-00105A7C4F8C}")
    PROGID = "Dscbo1.CbGraph1.1"


class FutureMst(IDib, IDibEvents):
    CLSID = IID("{1583EA45-B4D3-4B3A-8018-A0FDF8334619}")
    PROGID = "Dscbo1.FutureMst.1"


class FutureCurr(IDib, IDibEvents):
    CLSID = IID("{8F101465-F973-4601-ABF6-7B281A79C93C}")
    PROGID = "Dscbo1.FutureCurr.1"


class FutureIndexi(IDib, IDibEvents):
    CLSID = IID("{B28635B1-FF2B-4E03-98CC-427D71AA5AC4}")
    PROGID = "Dscbo1.FutureIndexi.1"


class FutureWide(IDib, IDibEvents):
    CLSID = IID("{9D5B7EF6-30C3-43F7-B9F5-6AD9A3CE6A26}")
    PROGID = "Dscbo1.FutureWide.1"


class FutureMo1(IDib, IDibEvents):
    CLSID = IID("{8F86C563-8079-47FD-979E-6C4C7D647786}")
    PROGID = "Dscbo1.FutureMo1.1"


class OptionMst(IDib, IDibEvents):
    CLSID = IID("{B040FF23-27CD-46B2-BDC8-E7E793509C65}")
    PROGID = "Dscbo1.OptionMst.1"


class OptionCur(IDib, IDibEvents):
    CLSID = IID("{2A90886E-86C7-4E37-94BF-D66FD36426F9}")
    PROGID = "Dscbo1.OptionCur.1"


class OptionMo(IDib, IDibEvents):
    CLSID = IID("{505B3ED8-392F-482D-A0C4-6D40F9E7EA72}")
    PROGID = "Dscbo1.OptionMo.1"


class OptionGreek(IDib, IDibEvents):
    CLSID = IID("{F39298B4-74D1-4699-AE7D-82C2CC428E25}")
    PROGID = "Dscbo1.OptionGreek.1"


class OptionGen(IDib, IDibEvents):
    CLSID = IID("{309CFF13-AE6E-48BD-8BE0-13B75D33D3E7}")
    PROGID = "Dscbo1.OptionGen.1"


class OptionCallput(IDib, IDibEvents):
    CLSID = IID("{0E581B11-5E74-4A79-8609-AF117BDB88E0}")
    PROGID = "Dscbo1.OptionCallput.1"


class StockIndexir(IDib, IDibEvents):
    CLSID = IID("{1C95CC46-DDC7-4015-8D06-7028FACDE801}")
    PROGID = "Dscbo1.StockIndexir.1"


class StockIndexis(IDib, IDibEvents):
    CLSID = IID("{354E2635-A0AB-4511-BCD9-13C187A37C89}")
    PROGID = "Dscbo1.StockIndexis.1"


class FutureBid1(IDib, IDibEvents):
    CLSID = IID("{12A49893-A2E9-42A0-9DD4-C28851E597D0}")
    PROGID = "Dscbo1.FutureBid1.1"


class StockMstm(IDib, IDibEvents):
    CLSID = IID("{92372A60-C14C-4B8B-A656-1BB5C17F84AC}")
    PROGID = "Dscbo1.StockMstm.1"


class FutureIndexh(IDib, IDibEvents):
    CLSID = IID("{A8341025-9D81-467C-8D44-5F569BF37842}")
    PROGID = "Dscbo1.FutureIndexh.1"


class StockStu(IDib, IDibEvents):
    CLSID = IID("{1D9E7343-8C92-430A-9C8D-F8C6DCF3D635}")
    PROGID = "Dscbo1.StockStu.1"


class FutureFtu(IDib, IDibEvents):
    CLSID = IID("{CEE55BF3-DE0B-46B9-AD5E-108D875E54FE}")
    PROGID = "Dscbo1.FutureFtu.1"


class OptionFtu(IDib, IDibEvents):
    CLSID = IID("{70A9C960-FBFF-4981-A081-3F323B3A439F}")
    PROGID = "Dscbo1.OptionFtu.1"


class FutureGr1(IDib, IDibEvents):
    CLSID = IID("{1EF6F3EE-F43F-4FEC-845A-44D4CF769272}")
    PROGID = "Dscbo1.FutureGr1.1"


class OptionGr1(IDib, IDibEvents):
    CLSID = IID("{65735FE8-5B16-4285-A832-532E5FFC9B38}")
    PROGID = "Dscbo1.OptionGr1.1"


class CpSvr7225(IDib, IDibEvents):
    CLSID = IID("{C12D47E0-BACB-47AE-BC6C-4BD5744A8680}")
    PROGID = "Dscbo1.CpSvr7225.1"


class PgAtime8112(IDib, IDibEvents):
    CLSID = IID("{44F25C73-57E6-4BAA-9369-9B6F42CD5D55}")
    PROGID = "Dscbo1.PgAtime8112.1"


class StockAdS(IDib, IDibEvents):
    CLSID = IID("{5CBBF6AD-6896-40A2-BC7F-630C274627BE}")
    PROGID = "Dscbo1.StockAdS.1"


class StockAdR(IDib, IDibEvents):
    CLSID = IID("{7630F872-FDF8-4880-BE46-C7B912CA5CC1}")
    PROGID = "Dscbo1.StockAdR.1"


class CpConclusion(IDib, IDibEvents):
    CLSID = IID("{72FDAF04-F87B-47E1-9396-0A7C98F4E5C5}")
    PROGID = "Dscbo1.CpConclusion.1"


class StockAdkS(IDib, IDibEvents):
    CLSID = IID("{58172CD3-659D-45C7-8E5E-9C65049C8202}")
    PROGID = "Dscbo1.StockAdkS.1"


class StockAdkR(IDib, IDibEvents):
    CLSID = IID("{0D60B192-F361-4353-8B23-44514911FA6F}")
    PROGID = "Dscbo1.StockAdkR.1"


class CpFConclusion(IDib, IDibEvents):
    CLSID = IID("{F33F2A8E-A1F8-40C3-9F0D-8001E409B18A}")
    PROGID = "Dscbo1.CpFConclusion.1"


class FutureWeek1(IDib, IDibEvents):
    CLSID = IID("{0D4CDCEC-DD27-402B-8036-094CB9D18F3E}")
    PROGID = "Dscbo1.FutureWeek1.1"


class OptionBid(IDib, IDibEvents):
    CLSID = IID("{137C4125-1323-469D-86BC-962C2C9CAC11}")
    PROGID = "Dscbo1.OptionBid.1"


class FutureK200(IDib, IDibEvents):
    CLSID = IID("{52F1E791-07E5-49DD-ADBD-4F59CEE7E56D}")
    PROGID = "Dscbo1.FutureK200.1"


class OptionWeek(IDib, IDibEvents):
    CLSID = IID("{B946B892-D57E-4D7D-A8A2-D857EC54C419}")
    PROGID = "Dscbo1.OptionWeek.1"


class OptionInfo(IDib, IDibEvents):
    CLSID = IID("{F68D10E7-FEED-4FDE-BBAA-D1FF881771BA}")
    PROGID = "Dscbo1.OptionInfo.1"


class OptionTV(IDib, IDibEvents):
    CLSID = IID("{594BC899-B2DF-4C32-83DF-6E0AA542B8DC}")
    PROGID = "Dscbo1.OptionTV.1"


class CpSvr7223(IDib, IDibEvents):
    CLSID = IID("{1F1E0B94-8A20-4F9E-A89D-53C3E5C1EC56}")
    PROGID = "Dscbo1.CpSvr7223.1"


class CpSvr8092S(IDib, IDibEvents):
    CLSID = IID("{362648C3-A91F-4BD6-B65C-354FCE9FCC5E}")
    PROGID = "Dscbo1.CpSvr8092S.1"


class CpSvr8561(IDib, IDibEvents):
    CLSID = IID("{71A629F4-D2A8-4F0C-AD48-B2B6494FD0F8}")
    PROGID = "Dscbo1.CpSvr8561.1"


class CpSvr8561T(IDib, IDibEvents):
    CLSID = IID("{B76AB425-5D82-4A74-BE0F-B5FAC0453787}")
    PROGID = "Dscbo1.CpSvr8561T.1"


class CpSvr8562(IDib, IDibEvents):
    CLSID = IID("{BCBE0F92-D5A0-44CF-ACB1-572E5246F4C3}")
    PROGID = "Dscbo1.CpSvr8562.1"


class CpSvr8563(IDib, IDibEvents):
    CLSID = IID("{B40008F5-BE02-42D1-AF05-0A95713D9F5C}")
    PROGID = "Dscbo1.CpSvr8563.1"


class CpSvr8091(IDib, IDibEvents):
    CLSID = IID("{2A04F706-DFCD-4588-9130-CCBC2C6043C8}")
    PROGID = "Dscbo1.CpSvr8091.1"


class CpSvr8091S(IDib, IDibEvents):
    CLSID = IID("{FA8F5A92-82B3-45A5-957B-F052EDCE3556}")
    PROGID = "Dscbo1.CpSvr8091S.1"


class SoptionWeek(IDib, IDibEvents):
    CLSID = IID("{0D6CDFB5-78EF-472B-807E-6C994FE01830}")
    PROGID = "Dscbo1.SoptionWeek.1"


class SoptionMst(IDib, IDibEvents):
    CLSID = IID("{DEFA472E-99E2-4355-B2C7-B1894541CC3D}")
    PROGID = "Dscbo1.SoptionMst.1"


class SoptionCur(IDib, IDibEvents):
    CLSID = IID("{CB5D1FFE-52B0-415F-9D97-DF8261878A1A}")
    PROGID = "Dscbo1.SoptionCur.1"


class SoptionBid(IDib, IDibEvents):
    CLSID = IID("{B17A779E-1C22-46B9-81C9-F52A92DCBAA2}")
    PROGID = "Dscbo1.SoptionBid.1"


class SoptionCallput(IDib, IDibEvents):
    CLSID = IID("{1D98FA00-46A7-410D-BEEE-378BE2F232B4}")
    PROGID = "Dscbo1.SoptionCallput.1"


class CpSvr8081(IDib, IDibEvents):
    CLSID = IID("{9D163A76-6432-46D8-AC7E-0F998B7AE283}")
    PROGID = "Dscbo1.CpSvr8081.1"


class CpSvr8082(IDib, IDibEvents):
    CLSID = IID("{C375F210-E366-4CB4-9AE2-60D77D306FCF}")
    PROGID = "Dscbo1.CpSvr8082.1"


class CpSvr8083(IDib, IDibEvents):
    CLSID = IID("{46570098-CA2D-4CCE-A9B0-348728C96814}")
    PROGID = "Dscbo1.CpSvr8083.1"


class CpSvr8111(IDib, IDibEvents):
    CLSID = IID("{4BDD0A5C-CBD7-426A-A1B0-CD7BB6DA3EF7}")
    PROGID = "Dscbo1.CpSvr8111.1"


class CpSvr8111S(IDib, IDibEvents):
    CLSID = IID("{2D79A13E-79DA-41A2-B565-BD9AED15E84B}")
    PROGID = "Dscbo1.CpSvr8111S.1"


class CpSvr8111KS(IDib, IDibEvents):
    CLSID = IID("{91E94973-C856-4368-9402-E1707CE2146C}")
    PROGID = "Dscbo1.CpSvr8111KS.1"


class CpSvr8116(IDib, IDibEvents):
    CLSID = IID("{F17A78B1-7DE3-48AC-AB79-588869083989}")
    PROGID = "Dscbo1.CpSvr8116.1"


class CpSvr7818(IDib, IDibEvents):
    CLSID = IID("{757B16A4-9A6A-427D-9332-BD5ABBAA3083}")
    PROGID = "Dscbo1.CpSvr7818.1"


class CpSvr7818C(IDib, IDibEvents):
    CLSID = IID("{18457BCD-7EC0-4312-9245-0036DC2DDACE}")
    PROGID = "Dscbo1.CpSvr7818C.1"


class CpSvr7819(IDib, IDibEvents):
    CLSID = IID("{C2DCC501-49E9-4ADB-8353-294FE25E7428}")
    PROGID = "Dscbo1.CpSvr7819.1"


class CpSvr7819C(IDib, IDibEvents):
    CLSID = IID("{1481AECC-DCC7-4161-9829-91DFDD24E70B}")
    PROGID = "Dscbo1.CpSvr7819C.1"


class CpSvr8300(IDib, IDibEvents):
    CLSID = IID("{C517AF9D-F297-449F-BECA-7B59F1DB845B}")
    PROGID = "Dscbo1.CpSvr8300.1"


class CpFore8311(IDib, IDibEvents):
    CLSID = IID("{0049522C-26C0-4BCC-AB77-E7AEAD1A4620}")
    PROGID = "Dscbo1.CpFore8311.1"


class CpFore8312(IDib, IDibEvents):
    CLSID = IID("{C192C148-EDC1-400C-ADE8-48778BE42737}")
    PROGID = "Dscbo1.CpFore8312.1"


class StockMst2(IDib, IDibEvents):
    CLSID = IID("{EEA6A7D7-1E8C-4D90-8ACB-7BD391694978}")
    PROGID = "Dscbo1.StockMst2.1"


class StockOutMst(IDib, IDibEvents):
    CLSID = IID("{1D5575F8-D57A-443E-80E8-F2A26F8FC168}")
    PROGID = "Dscbo1.StockOutMst.1"


class StockOutCur(IDib, IDibEvents):
    CLSID = IID("{A58788CC-6F6D-4287-8194-D1D5EBFC13CE}")
    PROGID = "Dscbo1.StockOutCur.1"


class OptionAtm(IDib, IDibEvents):
    CLSID = IID("{7163F981-6552-49E9-84AF-EC1E62FEC867}")
    PROGID = "Dscbo1.OptionAtm.1"


class FutureOptionStat(IDib, IDibEvents):
    CLSID = IID("{76F545B3-CAD9-4474-BA39-F67352924174}")
    PROGID = "Dscbo1.FutureOptionStat.1"


class FutureOptionStatPB(IDib, IDibEvents):
    CLSID = IID("{2079F79D-798E-4C4D-9A0E-7BAC8FE294C3}")
    PROGID = "Dscbo1.FutureOptionStatPB.1"


class StockIndexiChart(IDib, IDibEvents):
    CLSID = IID("{3116500C-0DC1-4C63-B760-043903A463C5}")
    PROGID = "Dscbo1.StockIndexiChart.1"


class FutOptRest(IDib, IDibEvents):
    CLSID = IID("{4FF1F71F-0D95-46F1-80D2-C62E50D46995}")
    PROGID = "Dscbo1.FutOptRest.1"


class ExpectIndexR(IDib, IDibEvents):
    CLSID = IID("{A2570BF0-8BF3-4AB8-A4B9-200741A16A11}")
    PROGID = "Dscbo1.ExpectIndexR.1"


class ExpectIndexS(IDib, IDibEvents):
    CLSID = IID("{484427BE-E0C6-45DD-9368-DEF8DB3EFC9D}")
    PROGID = "Dscbo1.ExpectIndexS.1"


class FutureCurOnly(IDib, IDibEvents):
    CLSID = IID("{21123F9D-FFFC-49B2-ACC1-B89B4EE50A18}")
    PROGID = "Dscbo1.FutureCurOnly.1"


class CpSvrNew8300(IDib, IDibEvents):
    CLSID = IID("{35E4CB92-E022-4905-B006-519345316A80}")


class CmeConclusionRt(IDib, IDibEvents):
    CLSID = IID("{DC9ECD73-16FE-4AA3-BEC9-2A8D1E9A8B72}")
    PROGID = "DsCbo1.CmeConclusionRt.1"


class EurexConclusionRt(IDib, IDibEvents):
    CLSID = IID("{06CD6CE2-CC6E-46A3-B1DF-FB51DEA97A77}")
    PROGID = "DsCbo1.EurexConclusionRt.1"


class OptionCallput2(IDib, IDibEvents):
    CLSID = IID("{E530DD89-64A2-4DA4-BA1D-546A68BDD193}")
    PROGID = "Dscbo1.OptionCallput2.1"


class CpSvr8119(IDib, IDibEvents):
    CLSID = IID("{5D1F4780-250E-4D0D-873D-2D059454F5F1}")
    PROGID = "Dscbo1.CpSvr8119.1"


class CpSvr8412(IDib, IDibEvents):
    CLSID = IID("{E1017E1F-F779-4624-88FD-97381687E54F}")
    PROGID = "Dscbo1.CpSvr8412.1"


class CpSvrNew8119(IDib, IDibEvents):
    CLSID = IID("{8113D43D-FCCB-4521-A13D-B7CCA8EBF378}")
    PROGID = "Dscbo1.CpSvrNew8119.1"


class CpSvrNew8119Chart(IDib, IDibEvents):
    CLSID = IID("{FD0CCD4E-3E44-4288-A42C-606D9703373B}")
    PROGID = "Dscbo1.CpSvrNew8119Chart.1"


class CpSvr7244(IDib, IDibEvents):
    CLSID = IID("{F5075466-0FB5-45CC-85AA-D902F1D173C3}")
    PROGID = "DsCbo1.CpSvr7244.1"


class CpSvr7246(IDib, IDibEvents):
    CLSID = IID("{8CE1E3A6-F42C-4959-B747-287A06921D4A}")
    PROGID = "DsCbo1.CpSvr7246.1"


class CpSvr7718(IDib, IDibEvents):
    CLSID = IID("{5E64D7D7-D393-4326-95AD-3FCBA4A4BF46}")
    PROGID = "DsCbo1.CpSvr7718.1"


class CpSvr7719(IDib, IDibEvents):
    CLSID = IID("{8B4FF082-FB67-4A38-868B-B1583D0C5AD2}")
    PROGID = "DsCbo1.CpSvr7719.1"


class CpSvrNew8119Day(IDib, IDibEvents):
    CLSID = IID("{6F491767-5800-4E11-B454-E3270FCBBD17}")
    PROGID = "DsCbo1.CpSvrNew8119Day.1"


class CpSvr9027(IDib, IDibEvents):
    CLSID = IID("{55896A25-A1DF-4BBA-96BD-9598EF5AD9D6}")
    PROGID = "DsCbo1.CpSvr9027.1"


class UpjongDaily(IDib, IDibEvents):
    CLSID = IID("{3B532417-7AE8-4434-84F2-814AB8D6435B}")
    PROGID = "DsCbo1.UpjongDaily.1"
