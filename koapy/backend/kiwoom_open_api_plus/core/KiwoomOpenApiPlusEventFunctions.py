class KiwoomOpenApiPlusEventFunctions:
    def OnReceiveTrData(
        self,
        sScrNo: str,
        sRQName: str,
        sTrCode: str,
        sRecordName: str,
        sPrevNext: str,
        nDataLength: int,
        sErrorCode: str,
        sMessage: str,
        sSplmMsg: str,
    ) -> None:
        ...

    def OnReceiveRealData(self, sRealKey: str, sRealType: str, sRealData: str) -> None:
        ...

    def OnReceiveMsg(self, sScrNo: str, sRQName: str, sTrCode: str, sMsg: str) -> None:
        ...

    def OnReceiveChejanData(self, sGubun: str, nItemCnt: int, sFIdList: str) -> None:
        ...

    def OnEventConnect(self, nErrCode: int) -> None:
        ...

    def OnReceiveInvestRealData(self, sRealKey: str) -> None:
        ...

    def OnReceiveRealCondition(
        self, sTrCode: str, strType: str, strConditionName: str, strConditionIndex: str
    ) -> None:
        ...

    def OnReceiveTrCondition(
        self,
        sScrNo: str,
        strCodeList: str,
        strConditionName: str,
        nIndex: int,
        nNext: int,
    ) -> None:
        ...

    def OnReceiveConditionVer(self, lRet: int, sMsg: str) -> None:
        ...
