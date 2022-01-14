class KiwoomOpenApiPlusDispatchFunctions:
    def CommConnect(self) -> int:
        ...

    def CommTerminate(self) -> None:
        ...

    def CommRqData(
        self, sRQName: str, sTrCode: str, nPrevNext: int, sScreenNo: str
    ) -> int:
        ...

    def GetLoginInfo(self, sTag: str) -> str:
        ...

    def SendOrder(
        self,
        sRQName: str,
        sScreenNo: str,
        sAccNo: str,
        nOrderType: int,
        sCode: str,
        nQty: int,
        nPrice: int,
        sHogaGb: str,
        sOrgOrderNo: str,
    ) -> int:
        ...

    def SendOrderFO(
        self,
        sRQName: str,
        sScreenNo: str,
        sAccNo: str,
        sCode: str,
        lOrdKind: int,
        sSlbyTp: str,
        sOrdTp: str,
        lQty: int,
        sPrice: str,
        sOrgOrdNo: str,
    ) -> int:
        ...

    def SetInputValue(self, sID: str, sValue: str) -> None:
        ...

    def SetOutputFID(self, sID: str) -> int:
        ...

    def CommGetData(
        self,
        sJongmokCode: str,
        sRealType: str,
        sFieldName: str,
        nIndex: int,
        sInnerFieldName: str,
    ) -> str:
        ...

    def DisconnectRealData(self, sScnNo: str) -> None:
        ...

    def GetRepeatCnt(self, sTrCode: str, sRecordName: str) -> int:
        ...

    def CommKwRqData(
        self,
        sArrCode: str,
        bNext: int,
        nCodeCount: int,
        nTypeFlag: int,
        sRQName: str,
        sScreenNo: str,
    ) -> int:
        ...

    def GetAPIModulePath(self) -> str:
        ...

    def GetCodeListByMarket(self, sMarket: str) -> str:
        ...

    def GetConnectState(self) -> int:
        ...

    def GetMasterCodeName(self, sTrCode: str) -> str:
        ...

    def GetMasterListedStockCnt(self, sTrCode: str) -> int:
        ...

    def GetMasterConstruction(self, sTrCode: str) -> str:
        ...

    def GetMasterListedStockDate(self, sTrCode: str) -> str:
        ...

    def GetMasterLastPrice(self, sTrCode: str) -> str:
        ...

    def GetMasterStockState(self, sTrCode: str) -> str:
        ...

    def GetDataCount(self, strRecordName: str) -> int:
        ...

    def GetOutputValue(self, strRecordName: str, nRepeatIdx: int, nItemIdx: int) -> str:
        ...

    def GetCommData(
        self, strTrCode: str, strRecordName: str, nIndex: int, strItemName: str
    ) -> str:
        ...

    def GetCommRealData(self, sTrCode: str, nFid: int) -> str:
        ...

    def GetChejanData(self, nFid: int) -> str:
        ...

    def GetThemeGroupList(self, nType: int) -> str:
        ...

    def GetThemeGroupCode(self, strThemeCode: str) -> str:
        ...

    def GetFutureList(self) -> str:
        ...

    def GetFutureCodeByIndex(self, nIndex: int) -> str:
        ...

    def GetActPriceList(self) -> str:
        ...

    def GetMonthList(self) -> str:
        ...

    def GetOptionCode(self, strActPrice: str, nCp: int, strMonth: str) -> str:
        ...

    def GetOptionCodeByMonth(self, sTrCode: str, nCp: int, strMonth: str) -> str:
        ...

    def GetOptionCodeByActPrice(self, sTrCode: str, nCp: int, nTick: int) -> str:
        ...

    def GetSFutureList(self, strBaseAssetCode: str) -> str:
        ...

    def GetSFutureCodeByIndex(self, strBaseAssetCode: str, nIndex: int) -> str:
        ...

    def GetSActPriceList(self, strBaseAssetGb: str) -> str:
        ...

    def GetSMonthList(self, strBaseAssetGb: str) -> str:
        ...

    def GetSOptionCode(
        self, strBaseAssetGb: str, strActPrice: str, nCp: int, strMonth: str
    ) -> str:
        ...

    def GetSOptionCodeByMonth(
        self, strBaseAssetGb: str, sTrCode: str, nCp: int, strMonth: str
    ) -> str:
        ...

    def GetSOptionCodeByActPrice(
        self, strBaseAssetGb: str, sTrCode: str, nCp: int, nTick: int
    ) -> str:
        ...

    def GetSFOBasisAssetList(self) -> str:
        ...

    def GetOptionATM(self) -> str:
        ...

    def GetSOptionATM(self, strBaseAssetGb: str) -> str:
        ...

    def GetBranchCodeName(self) -> str:
        ...

    def CommInvestRqData(self, sMarketGb: str, sRQName: str, sScreenNo: str) -> int:
        ...

    def SendOrderCredit(
        self,
        sRQName: str,
        sScreenNo: str,
        sAccNo: str,
        nOrderType: int,
        sCode: str,
        nQty: int,
        nPrice: int,
        sHogaGb: str,
        sCreditGb: str,
        sLoanDate: str,
        sOrgOrderNo: str,
    ) -> int:
        ...

    def KOA_Functions(self, sFunctionName: str, sParam: str) -> str:
        ...

    def SetInfoData(self, sInfoData: str) -> int:
        ...

    def SetRealReg(
        self, strScreenNo: str, strCodeList: str, strFidList: str, strOptType: str
    ) -> int:
        ...

    def GetConditionLoad(self) -> int:
        ...

    def GetConditionNameList(self) -> str:
        ...

    def SendCondition(
        self, strScrNo: str, strConditionName: str, nIndex: int, nSearch: int
    ) -> int:
        ...

    def SendConditionStop(
        self, strScrNo: str, strConditionName: str, nIndex: int
    ) -> None:
        ...

    def GetCommDataEx(self, strTrCode: str, strRecordName: str) -> None:
        ...

    def SetRealRemove(self, strScrNo: str, strDelCode: str) -> None:
        ...

    def GetMarketType(self, sTrCode: str) -> int:
        ...
