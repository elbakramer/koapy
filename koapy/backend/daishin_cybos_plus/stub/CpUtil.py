from collections.abc import Iterator
from typing import Any, Callable, Union

from pythoncom import Empty, Missing
from pywintypes import IID, Time

from koapy.common import EventInstance


class ICpUserInfo:
    CLSID = IID("{363AF9F5-0612-4E75-A563-211851B45A16}")

    def VerifyUserInfo(self, SocialNo: str, UserName: str) -> int:
        ...

    @property
    def ComID(self) -> str:
        ...


class CpUserInfo(ICpUserInfo):
    CLSID = IID("{DB656203-951A-4D6A-972E-0138DEBD6648}")
    PROGID = "CpUtil.CpUserInfo.1"


class ICpStockCode:
    CLSID = IID("{081AAEAA-DFAF-4B7F-A53A-0D1E4AC58584}")

    def CodeToName(self, code: str) -> str:
        ...

    def FullCodeToName(self, code: str) -> str:
        ...

    def GetCount(self) -> int:
        ...

    def GetData(self, type: int, index: int) -> Any:
        ...

    def CodeToFullCode(self, code: str) -> str:
        ...

    def FullCodeToCode(self, code: str) -> str:
        ...

    def NameToCode(self, name: str) -> str:
        ...

    def CodeToIndex(self, code: str) -> int:
        ...

    def GetPriceUnit(self, code: str, basePrice: int, directionUp: bool = True) -> int:
        ...


class CpStockCode(ICpStockCode):
    CLSID = IID("{2297F381-FFB1-45C6-AA80-4C6913F45E91}")
    PROGID = "CpUtil.CpStockCode.1"


class ICpFutureCode:
    CLSID = IID("{FDDF6F98-B0AE-4B86-8C62-CC4469075F65}")

    def GetCount(self) -> int:
        ...

    def GetData(self, type: int, index: int) -> Any:
        ...

    def CodeToName(self, code: str) -> str:
        ...


class CpFutureCode(ICpFutureCode):
    CLSID = IID("{15A37730-A973-47D7-9058-2686097642F8}")
    PROGID = "CpUtil.CpFutureCode.1"


class CpKFutureCode(ICpFutureCode):
    CLSID = IID("{E6BFF246-8B47-4833-AE20-F853BDAA3248}")
    PROGID = "CpUtil.CpKFutureCode.1"


class ICpOptionCode:
    CLSID = IID("{312ADE72-2C5C-4084-ADCE-9BBBAFEFAD56}")

    def GetCount(self) -> int:
        ...

    def GetData(self, type: int, index: int) -> Any:
        ...

    def CodeToName(self, code: str) -> str:
        ...


class CpOptionCode(ICpOptionCode):
    CLSID = IID("{7566755F-36AD-43EF-B388-4CC62CA94279}")
    PROGID = "CpUtil.CpOptionCode.1"


class ICpSoptionCode:
    CLSID = IID("{B41FB07E-3901-4FF8-9D66-1C06D50EC5FC}")

    def GetCount(self) -> int:
        ...

    def GetData(self, type: int, index: int) -> Any:
        ...

    def CodeToName(self, code: str) -> str:
        ...


class CpSoptionCode(ICpSoptionCode):
    CLSID = IID("{F23D75C0-A0AC-4988-865C-54B3B9D009B2}")
    PROGID = "CpUtil.CpSoptionCode.1"


class ICpCybos:
    CLSID = IID("{3722B490-A340-45C5-BDA5-3C736DDEB423}")

    def GetLimitRemainCount(self, limitType: int) -> int:
        ...

    def CreonPlusConnect(self, bstID: str, bstPWD: str, bstPKI: str) -> str:
        ...

    def CybosPlusConnect(self, bstID: str, bstPWD: str, bstPKI: str) -> str:
        ...

    def PlusDisconnect(self) -> None:
        ...

    def GetLimitRemainTime(self, limitType: int) -> int:
        ...

    @property
    def IsConnect(self) -> int:
        ...

    @property
    def ServerType(self) -> int:
        ...

    @property
    def LimitRequestRemainTime(self) -> int:
        ...


class ICpCybosEvents:
    CLSID = IID("{17F70631-56E5-40FC-B94F-44ADD3A850B1}")

    @property
    def OnDisconnect(self) -> Union[EventInstance, Callable[[], None]]:
        ...


class ICpCybosEventsHandler:
    CLSID = IID("{17F70631-56E5-40FC-B94F-44ADD3A850B1}")

    def OnDisconnect(self) -> int:
        ...


class CpCybos(ICpCybos, ICpCybosEvents):
    CLSID = IID("{19A11288-2B28-45C4-8CD4-3A12B60C3BD7}")
    PROGID = "CpUtil.CpCybos.1"


class ICpCodeMgr:
    CLSID = IID("{6893A6D3-03FD-46EB-BB0E-28A22D3AEC9B}")

    def GetGroupCodeList(self, GroupCode: int) -> Any:
        ...

    def CodeToName(self, code: str) -> str:
        ...

    def GetUsCodeList(self, type: int = 1) -> Any:
        ...

    def GetUsCodeName(self, code: str) -> str:
        ...

    def GetStockMarginRate(self, code: str) -> int:
        ...

    def GetStockMemeMin(self, code: str) -> int:
        ...

    def GetStockElwBasketCodeList(self, bstrCode: str) -> Any:
        ...

    def GetStockElwBasketCompList(self, bstrCode: str) -> Any:
        ...

    def GetMarketStartTime(self) -> int:
        ...

    def GetMarketEndTime(self) -> int:
        ...

    def GetStockIndustryCode(self, bstrCode: str) -> str:
        ...

    def GetStockMarketKind(self, bstrCode: str) -> int:
        ...

    def GetStockControlKind(self, bstrCode: str) -> int:
        ...

    def GetStockSupervisionKind(self, bstrCode: str) -> int:
        ...

    def GetStockCapital(self, bstrCode: str) -> int:
        ...

    def GetStockFiscalMonth(self, bstrCode: str) -> int:
        ...

    def GetStockGroupCode(self, bstrCode: str) -> int:
        ...

    def GetStockKospi200Kind(self, bstrCode: str) -> int:
        ...

    def GetStockStatusKind(self, bstrCode: str) -> int:
        ...

    def GetGroupList(self) -> Any:
        ...

    def GetGroupName(self, bstrCode: str) -> str:
        ...

    def GetIndustryList(self) -> Any:
        ...

    def GetKrxIndustryList(self) -> Any:
        ...

    def GetIndustryName(self, bstrCode: str) -> str:
        ...

    def GetMemberList(self) -> Any:
        ...

    def GetMemberName(self, bstrCode: str) -> str:
        ...

    def GetKosdaqIndustry1List(self) -> Any:
        ...

    def GetKosdaqIndustry2List(self) -> Any:
        ...

    def GetStockListByMarket(self, MarketKind: int) -> Any:
        ...

    def GetStockSectionKind(self, bstrCode: str) -> int:
        ...

    def GetStockLacKind(self, bstrCode: str) -> int:
        ...

    def GetStockCodeByName(self, bstrName: str) -> str:
        ...

    def GetStockListedDate(self, bstrName: str) -> int:
        ...

    def GetStockMaxPrice(self, bstrName: str) -> int:
        ...

    def GetStockMinPrice(self, bstrName: str) -> int:
        ...

    def GetStockParPrice(self, bstrName: str) -> int:
        ...

    def GetStockStdPrice(self, bstrName: str) -> int:
        ...

    def GetStockYdOpenPrice(self, bstrName: str) -> int:
        ...

    def GetStockYdHighPrice(self, bstrName: str) -> int:
        ...

    def GetStockYdLowPrice(self, bstrName: str) -> int:
        ...

    def GetStockYdClosePrice(self, bstrName: str) -> int:
        ...

    def GetStockParPriceChageType(self, bstrName: str) -> int:
        ...

    def IsStockCreditEnable(self, bstrName: str) -> int:
        ...

    def GetVentureKind(self, bstrName: str) -> int:
        ...

    def IsStockLoanEnable(self, bstrName: str) -> int:
        ...

    def GetStockEngName(self, bstrCode: str) -> str:
        ...

    def GetWorkDate(self) -> str:
        ...

    def IsSPAC(self, bstrName: str) -> int:
        ...

    def IsLendingStockEnable(self, bstrName: str) -> int:
        ...

    def GetMiniFutureList(self) -> Any:
        ...

    def GetMiniOptionList(self) -> Any:
        ...

    def ReLoadPortData(self) -> None:
        ...

    def GetTickUnit(self, bstrCode: str) -> float:
        ...

    def GetTickValue(self, bstrCode: str) -> float:
        ...

    def OvFutCodeToName(self, code: str) -> str:
        ...

    def OvFutGetAllCodeList(self) -> Any:
        ...

    def OvFutGetExchList(self) -> Any:
        ...

    def OvFutGetLastTradeDate(self, code: str) -> int:
        ...

    def OvFutGetExchCode(self, code: str) -> str:
        ...

    def OvFutGetProdCode(self, code: str) -> str:
        ...

    def IsBigListingStock(self, code: str) -> int:
        ...

    def IsTradeCondition(self, code: str) -> int:
        ...

    def GetStartTime(self, code: str) -> int:
        ...

    def GetEndTime(self, code: str) -> int:
        ...

    def IsFrnMember(self, code: str) -> int:
        ...

    def GetStockFutureList(self) -> Any:
        ...

    def GetStockFutureBaseList(self) -> Any:
        ...

    def GetStockFutureListByBaseCode(self, bstrCode: str) -> Any:
        ...

    def GetStockFutureBaseCode(self, bstrCode: str) -> str:
        ...

    def IsStockArrgSby(self, code: str) -> int:
        ...

    def IsStockIoi(self, code: str) -> int:
        ...

    def GetOverHeating(self, bstrCode: str) -> int:
        ...

    def IsStockLtgStkCnInsfItm(self, code: str) -> int:
        ...

    def GetKostarOptionList(self) -> Any:
        ...

    def GetFOTradeUnit(self, bstrCode: str) -> float:
        ...

    def GetKostarFutureList(self) -> Any:
        ...


class CpCodeMgr(ICpCodeMgr):
    CLSID = IID("{995B5ABE-ED4B-4D04-B46D-6238AB66EA71}")
    PROGID = "CpUtil.CpCodeMgr.1"


class ICpElwCode:
    CLSID = IID("{A162F0D1-894A-48D1-BDF4-E8589EA7607B}")

    def GetCount(self) -> int:
        ...

    def GetData(self, type: int, index: int) -> Any:
        ...

    def CodeToName(self, code: str) -> str:
        ...

    def GetStockElwBaseList(self) -> Any:
        ...

    def GetStockElwBaseCode(self, bstrCode: str) -> str:
        ...

    def GetStockElwBaseName(self, bstrCode: str) -> str:
        ...

    def GetStockElwIssuerList(self) -> Any:
        ...

    def GetStockElwLpCodeList(self, bstrCode: str) -> Any:
        ...

    def GetNameByStockElwLpCode(self, bstrLpCode: str) -> str:
        ...

    def GetStockElwBasketCodeList(self, bstrCode: str) -> Any:
        ...

    def GetStockElwBasketCompList(self, bstrCode: str) -> Any:
        ...

    def GetStockElwCodeListByBaseCode(self, bstrCode: str) -> Any:
        ...

    def GetStockElwCodeListByRightType(self, eRightType: int) -> Any:
        ...


class CpElwCode(ICpElwCode):
    CLSID = IID("{3AB3C774-9971-4BD3-9393-183641A5028D}")
    PROGID = "CpUtil.CpElwCode.1"


class ICpUsCode:
    CLSID = IID("{E1698433-8C49-4075-BDF8-0C0A23C61A2A}")

    def GetUsCodeList(self, USTYPE: int) -> Any:
        ...

    def GetNameByUsCode(self, bstrUsCode: str) -> str:
        ...


class CpUsCode(ICpUsCode):
    CLSID = IID("{03948751-CF92-443E-81D9-94351E0F51FF}")
    PROGID = "CpUtil.CpUsCode.1"


class ICpCalcOptGreeks:
    CLSID = IID("{AE72A9FD-E459-4678-B8CA-7417BEF26142}")

    def Calculate(self) -> None:
        ...

    @property
    def TV(self) -> float:
        ...

    @property
    def Delta(self) -> float:
        ...

    @property
    def Gamma(self) -> float:
        ...

    @property
    def Theta(self) -> float:
        ...

    @property
    def Vega(self) -> float:
        ...

    @property
    def Rho(self) -> float:
        ...

    @property
    def IV(self) -> float:
        ...

    @property
    def CallPutType(self) -> None:
        ...

    @CallPutType.setter
    def CallPutType(self, CallPutType: int) -> None:
        ...

    @property
    def Price(self) -> None:
        ...

    @Price.setter
    def Price(self, Price: float) -> None:
        ...

    @property
    def UnderPrice(self) -> None:
        ...

    @UnderPrice.setter
    def UnderPrice(self, UnderPrice: float) -> None:
        ...

    @property
    def ExerPrice(self) -> None:
        ...

    @ExerPrice.setter
    def ExerPrice(self, ExerPrice: float) -> None:
        ...

    @property
    def VolatilityType(self) -> None:
        ...

    @VolatilityType.setter
    def VolatilityType(self, VolatilityType: int) -> None:
        ...

    @property
    def Volatility(self) -> None:
        ...

    @Volatility.setter
    def Volatility(self, Volatility: float) -> None:
        ...

    @property
    def ExpirDays(self) -> None:
        ...

    @ExpirDays.setter
    def ExpirDays(self, ExpirDays: int) -> None:
        ...

    @property
    def RFInterRate(self) -> None:
        ...

    @RFInterRate.setter
    def RFInterRate(self, RFInterRate: float) -> None:
        ...

    @property
    def DividRate(self) -> None:
        ...

    @DividRate.setter
    def DividRate(self, DividRate: float) -> None:
        ...


class CpCalcOptGreeks(ICpCalcOptGreeks):
    CLSID = IID("{BA69760D-1698-4BC1-8947-E7F2D07F2173}")
    PROGID = "CpUtil.CpCalcOptGreeks.1"


class ICpBondCode:
    CLSID = IID("{D226367D-66EC-42FE-AED5-696F697AFB6D}")

    @property
    def code(self) -> str:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def type(self) -> int:
        ...

    @property
    def Remain(self) -> int:
        ...

    @property
    def Issue(self) -> int:
        ...

    @property
    def Interest(self) -> int:
        ...

    @property
    def IssueDate(self) -> int:
        ...

    @property
    def ExpirationDate(self) -> int:
        ...

    @property
    def Retail(self) -> int:
        ...

    @property
    def CouponRate(self) -> float:
        ...

    @property
    def InterestShortName(self) -> str:
        ...

    @property
    def InterestCycle(self) -> int:
        ...

    @property
    def RiskLevel(self) -> str:
        ...


class CpBondCode(ICpBondCode):
    CLSID = IID("{8B4B7EFD-7BE3-4C82-A3A7-1E741BB6A2B1}")


class ICpBondCodes:
    CLSID = IID("{C09E3D05-D1D5-41FE-9DCF-1900FCB69708}")

    def __call__(self, _MIDL__ICpBondCodes0000_: Any) -> Any:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[Any]:
        ...


class CpBondCodes(ICpBondCodes):
    CLSID = IID("{73E62CE2-EB0C-49B2-94B6-029527C9DADA}")
    PROGID = "CpUtil.CpBondCodes.1"
