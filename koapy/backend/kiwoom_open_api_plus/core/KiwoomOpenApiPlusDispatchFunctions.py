class KiwoomOpenApiPlusDispatchFunctions:
    def CommConnect(self) -> int:
        """
        로그인 윈도우를 실행한다.

        수동 로그인 설정인 경우 로그인창을 출력.
        자동 로그인 설정인 경우 로그인창에서 자동으로 로그인을 시도합니다.

        로그인이 성공하거나 실패하는 경우 OnEventConnect() 이벤트가 발생하고 이벤트의
        인자 값으로 로그인 성공 여부를 알 수 있다.

        Returns:
            int: 에러코드, 성공하면 0 을, 실패하면 음수를 반환
        """
        ...

    def CommTerminate(self) -> None:
        """
        더 이상 지원하지 않는 함수.

        프로그램 종료없이 서버와의 접속만 단절시키는 함수입니다.
        ※ 함수 사용 후 사용자의 오해소지가 생기는 이유로 더 이상 사용할 수 없는 함수입니다.

        통신 연결 상태는 GetConnectState() 메소드로 알 수 있다.
        """
        ...

    def CommRqData(
        self, sRQName: str, sTrCode: str, nPrevNext: int, sScreenNo: str
    ) -> int:
        """
        통신 데이터를 서버로 전송한다.

        반환 코드 구분:
            - OP_ERR_NONE(0): 정상처리
            - OP_ERR_SISE_OVERFLOW(-200): 과도한 시세조회로 인한 통신불가
            - OP_ERR_RQ_STRUCT_FAIL(-201): 입력 구조체 생성 실패
            - OP_ERR_RQ_STRING_FAIL(-202): 요청전문 작성 실패

        Args:
            sRQName (str): 사용자 구분명 (임의로 지정, 한글 지원)
            sTrCode (str): 조회하려는 TR 코드
            nPrevNext (int): 연속조회 여부 (0:조회, 2:연속)
            sScreenNo (str): 화면번호 (4자리 숫자 임의로 지정)

        Returns:
            int: 에러코드, 성공하면 0 을, 실패하면 음수를 반환
        """
        ...

    def GetLoginInfo(self, sTag: str) -> str:
        """
        로그인한 사용자 정보를 반환한다.

        태그값 구분:
            - "ACCOUNT_CNT": 전체 보유계좌 개수를 반환합니다.
            - "ACCLIST" 또는 "ACCNO": 구분자 ';' 로 연결된 전체 보유계좌 목록을 반환합니다.
            - "USER_ID": 사용자 ID를 반환합니다.
            - "USER_NAME": 사용자 이름을 반환합니다.
            - "KEY_BSECGB": 키보드 보안 해지 여부를 반환합니다. (0:정상, 1:해지)
            - "FIREW_SECGB": 방화벽 설정 여부를 반환합니다. (0:미설정, 1:설정, 2:해지)
            - "GetServerGubun": 접속서버 구분을 반환합니다. (1:모의투자, 나머지:실거래서버)

        Args:
            sTag (str): 사용자 정보 구분 태그 값

        Returns:
            str: 태그값에 따른 데이터 반환
        """
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
        """
        주식 주문을 서버로 전송한다.

        서버에 주문을 전송하는 함수 입니다.
        9개 인자값을 가진 주식주문 함수이며 리턴값이 0이면 성공이며 나머지는 에러입니다.
        1초에 5회만 주문가능하며 그 이상 주문요청하면 에러 -308을 리턴합니다.

        ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK, 장전시간외, 장후시간외 주문시 주문가격은 0으로 입력합니다.
        ※ 취소 주문일때 주문가격은 0으로 입력합니다.

        거래 구분:
            - 00: 지정가
            - 03: 시장가
            - 05: 조건부지정가
            - 06: 최유리지정가
            - 07: 최우선지정가
            - 10: 지정가IOC
            - 13: 시장가IOC
            - 16: 최유리IOC
            - 20: 지정가FOK
            - 23: 시장가FOK
            - 26: 최유리FOK
            - 61: 장전시간외종가
            - 62: 시간외단일가매매
            - 81: 장후시간외종가

        ※ 모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

        정규장 외 주문:
            - 장전 동시호가 주문
                - 08:30 ~ 09:00.	거래구분 00:지정가/03:시장가 (일반주문처럼)
                - ※ 08:20 ~ 08:30 시간의 주문은 키움에서 대기하여 08:30 에 순서대로 거래소로 전송합니다.
            - 장전시간외 종가
                - 08:30 ~ 08:40. 	거래구분 61:장전시간외종가.  가격 0입력
                - ※ 전일 종가로 거래. 미체결시 자동취소되지 않음
            - 장마감 동시호가 주문
                - 15:20 ~ 15:30.	거래구분 00:지정가/03:시장가 (일반주문처럼)
            - 장후 시간외 종가
                - 15:40 ~ 16:00.	거래구분 81:장후시간외종가.  가격 0입력
                - ※ 당일 종가로 거래
            - 시간외 단일가
                - 16:00 ~ 18:00.	거래구분 62:시간외단일가.  가격 입력
                - ※ 10분 단위로 체결, 당일 종가대비 +-10% 가격으로 거래

        주문 유형:
            - 1: 신규매수
            - 2: 신규매도
            - 3: 매수취소
            - 4: 매도취소
            - 5: 매수정정
            - 6: 매도정정

        Args:
            sRQName (str): 사용자 구분 요청명
            sScreenNo (str): 화면번호 (4자리)
            sAccNo (str): 계좌번호 (10자리)
            nOrderType (int): 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
            sCode (str): 종목코드 (6자리)
            nQty (int): 주문수량
            nPrice (int): 주문단가
            sHogaGb (str): 거래구분 (혹은 호가구분)
            sOrgOrderNo (str): 원주문번호, 신규주문에는 공백 입력, 정정/취소시 입력합니다.

        Returns:
            int: 에러코드, 성공하면 0 을, 실패하면 음수를 반환
        """
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
        """
        선물/옵션 주문을 서버로 전송한다.

        서버에 주문을 전송하는 함수 입니다.
        코스피지수200 선물옵션 전용 주문함수입니다.

        거래 구분:
            - 1: 지정가
            - 2: 조건부지정가
            - 3: 시장가
            - 4: 최유리지정가
            - 5: 지정가(IOC)
            - 6: 지정가(FOK)
            - 7: 시장가(IOC)
            - 8: 시장가(FOK)
            - 9: 최유리지정가(IOC)
            - A: 최유리지정가(FOK)

        ※ 장종료 후 시간외 주문은 지정가 선택

        Args:
            sRQName (str): 사용자 구분명
            sScreenNo (str): 화면번호
            sAccNo (str): 계좌번호 (10자리)
            sCode (str): 종목코드
            lOrdKind (int): 주문종류 (1:신규매매, 2:정정, 3:취소)
            sSlbyTp (str): 매매구분 (1:매도, 2:매수)
            sOrdTp (str): 거래구분
            lQty (int): 주문수량
            sPrice (str): 주문가격
            sOrgOrdNo (str): 원주문번호

        Returns:
            int: 에러코드, 성공하면 0 을, 실패하면 음수를 반환
        """
        ...

    def SetInputValue(self, sID: str, sValue: str) -> None:
        """
        TR 입력 값을 서버통신 전에 입력한다.

        조회요청시 TR의 Input값을 지정하는 함수입니다.
        CommRqData() 호출 전에 입력값들을 셋팅합니다.
        각 TR마다 Input 항목이 다릅니다. 순서에 맞게 Input 값들을 셋팅해야 합니다.

        Args:
            sID (str): TR에 명시된 Input 이름
            sValue (str): Input 이름으로 지정한 값
        """
        ...

    def SetOutputFID(self, sID: str) -> int:
        """
        1.0.0.1 버전 이후 사용하지 않음.
        """
        ...

    def CommGetData(
        self,
        sJongmokCode: str,
        sRealType: str,
        sFieldName: str,
        nIndex: int,
        sInnerFieldName: str,
    ) -> str:
        """
        이 함수는 지원하지 않을 것이므로 용도에 맞는 전용 함수를 사용할 것. (비고참고)

        일부 TR에서 사용상 제약이 있으므로 이 함수 대신 GetCommData() 함수를 사용하시기 바랍니다.

        비고:
            - 조회 정보 요청: GetCommData(strTrCode: str, strRecordName: str, nIndex: int, strItemName: str)
            - 실시간 정보 요청: GetCommRealData(sTrCode: str, nFid: int)
            - 체결 정보 요청: GetChejanData(nFid: int)
        """
        ...

    def DisconnectRealData(self, sScnNo: str) -> None:
        """
        화면 내 모든 리얼데이터 요청을 제거한다.

        시세데이터를 요청할때 사용된 화면번호를 이용하여
        해당 화면번호로 등록되어져 있는 종목의 실시간시세를 서버에 등록해지 요청합니다.
        이후 해당 종목의 실시간시세는 수신되지 않습니다.
        단, 해당 종목이 또다른 화면번호로 실시간 등록되어 있는 경우 해당종목에대한 실시간시세 데이터는 계속 수신됩니다.

        화면을 종료할 때 반드시 위 함수를 호출해야 한다.

        Args:
            sScnNo: 화면번호 (4자리)
        """
        ...

    def GetRepeatCnt(self, sTrCode: str, sRecordName: str) -> int:
        """
        레코드 반복횟수를 반환한다.

        데이터 수신시 멀티데이터의 갯수(반복수)를 얻을수 있습니다.
        예를 들어 차트조회는 한번에 최대 900개 데이터를 수신할 수 있는데
        이렇게 수신한 데이터갯수를 얻을때 사용합니다.
        이 함수는 OnReceiveTRData() 이벤트가 발생될때 그 안에서 사용해야 합니다.

        Args:
            sTrCode (str): TR 이름
            sRecordName (str): 레코드 이름

        Returns:
            int: 레코드의 반복횟수
        """
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
        """
        복수종목조회 요청을 서버로 송신한다.

        한번에 100종목까지 조회할 수 있는 복수종목 조회함수 입니다.
        함수인자로 사용하는 종목코드 리스트는 조회하려는 종목코드 사이에 구분자 ';' 를 추가해서 만들면 됩니다.
        수신되는 데이터는 TR목록에서 복수종목정보요청(OPTKWFID) Output을 참고하시면 됩니다.

        ※ OPTKWFID TR은 CommKwRqData() 함수 전용으로, CommRqData 로는 사용할 수 없습니다.
        ※ OPTKWFID TR은 영웅문4 HTS의 관심종목과는 무관합니다.

        반환 코드 구분:
            - OP_ERR_NONE(0): 정상처리
            - OP_ERR_SISE_OVERFLOW(-200): 과도한 시세조회로 인한 통신불가
            - OP_ERR_RQ_STRUCT_FAIL(-201): 입력 구조체 생성 실패
            - OP_ERR_RQ_STRING_FAIL(-202): 요청전문 작성 실패

        Args:
            sArrCode (str): 종목리스트
            bNext (int): 연속조회 여부 (0:기본값, 1:연속조회(지원안함))
            nCodeCount (int): 종목개수
            nTypeFlag (int): 조회구분 (0:주식 종목, 3:선물옵션 종목)
            sRQName (str): 사용자 구분명
            sScreenNo (str): 화면번호 (4자리)

        Returns:
            int: 에러코드, 성공하면 0 을, 실패하면 음수를 반환
        """
        ...

    def GetAPIModulePath(self) -> str:
        """
        OpenAPI 모듈의 경로를 반환한다.

        Returns:
            str: OpenAPI 모듈의 설치 경로
        """
        ...

    def GetCodeListByMarket(self, sMarket: str) -> str:
        """
        시장구분에 따른 종목코드를 반환한다.

        주식 시장별 종목코드 리스트를 ';' 로 구분해서 전달합니다.
        시장구분값을 "" 공백으로 하면 전체시장 코드리스트를 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        시장 구분:
            - 0: 장내
            - 3: ELW
            - 4: 뮤추얼펀드
            - 5: 신주인수권
            - 6: 리츠
            - 8: ETF
            - 9: 하이일드펀드
            - 10: 코스닥
            - 30: K-OTC
            - 50: 코넥스 (KONEX)

        Args:
            sMarket (str): 시장 구분값

        Returns:
            str: 종목코드 리스트, 종목간 구분은 ';' 이다.
        """
        ...

    def GetConnectState(self) -> int:
        """
        현재 접속상태를 반환한다.

        서버와 현재 접속 상태를 알려줍니다.

        Returns:
            int: 접속상태, 1:연결, 0:연결안됨
        """
        ...

    def GetMasterCodeName(self, sTrCode: str) -> str:
        """
        종목코드의 한글명을 반환한다.

        종목코드에 해당하는 종목명을 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        장내외, 지수선옵, 주식선옵 검색 가능.

        Args:
            sTrCode (str): 종목코드 (4자리)

        Returns:
            str: 종목 한글명
        """
        ...

    def GetMasterListedStockCnt(self, sTrCode: str) -> int:
        """
        종목코드의 상장주식수를 반환한다.

        입력한 종목코드에 해당하는 종목 상장주식수를 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        Args:
            sTrCode (str): 종목코드 (4자리)

        Returns:
            int: 상장주식수
        """
        ...

    def GetMasterConstruction(self, sTrCode: str) -> str:
        """
        종목코드의 감리구분을 반환한다.

        입력한 종목코드에 해당하는 종목의 감리구분을 전달합니다.
        (정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목)

        로그인 한 후에 사용할 수 있는 함수입니다.

        감리 구분:
            - 정상
            - 투자주의
            - 투자경고
            - 투자위험
            - 투자주의환기종목

        Args:
            sTrCode (str): 종목코드 (4자리)

        Returns:
            str: 감리구분 (정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목)
        """
        ...

    def GetMasterListedStockDate(self, sTrCode: str) -> str:
        """
        종목코드의 상장일을 반환한다.

        입력한 종목의 상장일을 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        Args:
            sTrCode (str): 종목코드 (4자리)

        Returns:
            str: 상장일 (8자리, YYYYMMDD)
        """
        ...

    def GetMasterLastPrice(self, sTrCode: str) -> str:
        """
        종목코드의 전일가를 반환한다.

        입력한 종목의 당일 기준가를 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        Args:
            sTrCode (str): 종목코드 (4자리)

        Returns:
            str: 전일가
        """
        ...

    def GetMasterStockState(self, sTrCode: str) -> str:
        """
        종목코드의 종목상태를 반환한다.

        입력한 종목의 증거금 비율, 거래정지, 관리종목, 감리종목, 투자유의종목, 담보대출, 액면분할, 신용가능 여부를 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        Args:
            sTrCode (str): 종목코드 (4자리)

        Returns:
            str: 종목상태 (정상, 증거금N%, 거래정지, 관리종목, 감리종목, 투자유의종목, 담보대출, 액면분할, 신용가능)
        """
        ...

    def GetDataCount(self, strRecordName: str) -> int:
        """
        레코드의 반복개수를 반환한다.

        ※ 문서상으로만 존재하고 KOAStudio 에서는 확인 안되는 것으로 보아 일반적인 상황에선
        해당 함수 대신 GetRepeatCnt() 를 사용하는게 더 바람직할 듯

        Args:
            strRecordName (str): 레코드 명

        Returns:
            str: 레코드 반복개수
        """
        ...

    def GetOutputValue(self, strRecordName: str, nRepeatIdx: int, nItemIdx: int) -> str:
        """
        레코드의 반복순서와 아이템의 출력순서에 따라 수신데이터를 반환한다.

        ※ 문서상으로만 존재하고 KOAStudio 에서는 확인 안되는 것으로 보아 일반적인 상황에선
        해당 함수 대신 GetCommData() 를 사용하는게 더 바람직할 듯

        Args:
            strRecordName (str): 레코드 명
            nRepeatIdx (int): 반복 순서
            nItemIdx (int): 아이템 순서

        Returns:
            str: 수신 데이터
        """
        ...

    def GetCommData(
        self, strTrCode: str, strRecordName: str, nIndex: int, strItemName: str
    ) -> str:
        """
        수신 데이터를 반환한다.

        OnReceiveTRData() 이벤트가 발생될때 수신한 데이터를 얻어오는 함수입니다.
        이 함수는 OnReceiveTRData() 이벤트가 발생될때 그 안에서 사용해야 합니다.

        Args:
            strTrCode (str): TR코드
            strRecordName (str): 레코드명
            nIndex (int): 복수데이터 인덱스
            strItemName (str): 아이템명 (TR별 출력항목 이름)

        Returns:
            str: 수신 데이터
        """
        ...

    def GetCommRealData(self, sTrCode: str, nFid: int) -> str:
        """
        실시간 시세 데이터를 반환한다.

        실시간시세 데이터 수신 이벤트인 OnReceiveRealData() 가 발생될때 실시간데이터를 얻어오는 함수입니다.
        이 함수는 OnReceiveRealData() 이벤트가 발생될때 그 안에서 사용해야 합니다.
        FID 값은 KOAStudio 의 "실시간목록" 탭에서 확인할 수 있습니다.

        일반적으로 strTrCode 는 OnReceiveRealData() 이벤트 함수의 첫번째 매개변수를 사용한다.

        Args:
            strTrCode (str): TR코드
            nFid (int): 실시간 아이템

        Returns:
            str: 수신 데이터
        """
        ...

    def GetChejanData(self, nFid: int) -> str:
        """
        체결잔고 데이터를 반환한다.

        OnReceiveChejan() 이벤트가 발생될때 FID 에 해당되는 값을 구하는 함수입니다.
        이 함수는 OnReceiveChejan() 이벤트 안에서 사용해야 합니다.
        Ex) 체결가 = GetChejanData(910)

        Args:
            nFid (int): 체결잔고 아이템

        Returns:
            str: 수신 데이터
        """
        ...

    def GetThemeGroupList(self, nType: int) -> str:
        """
        테마코드와 테마명을 반환한다.

        반환값의 코드와 코드명 구분은 '|', 코드의 구분은 ';'
        Ex) 100|태양광_폴리실리콘;152|합성섬유

        Args:
            nType (int): 정렬순서 (0:코드순, 1:테마순)

        Returns:
            str: 코드와 코드명 리스트
        """
        ...

    def GetThemeGroupCode(self, strThemeCode: str) -> str:
        """
        테마코드에 소속된 종목코드를 반환한다.

        반환값의 종목코드간 구분은 ';'
        Ex) A000660;A005930

        Args:
            strThemeCode (str): 테마코드

        Returns:
            str: 종목코드 리스트
        """
        ...

    def GetFutureList(self) -> str:
        """
        지수선물 리스트를 반환한다.

        지수선물 종목코드 리스트를 ';'로 구분해서 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        반환값의 종목코드간 구분은 ';'
        Ex) 101J9000;101JC000

        Returns:
            str: 종목코드 리스트
        """
        ...

    def GetFutureCodeByIndex(self, nIndex: int) -> str:
        """
        지수선물 코드를 반환한다.

        Ex) 최근월선물 = GetFutureCodeByIndex(0)
            최근월스프레드 = GetFutureCodeByIndex(4)

        Args:
            nIndex (int): 0 ~ 3: 지수선물코드, 4 ~ 7: 지수스프레드

        Returns:
            str: 종목코드
        """
        ...

    def GetActPriceList(self) -> str:
        """
        지수옵션 행사가 리스트를 반환한다.

        지수옵션 행사가에 100을 곱해서 소수점이 없는 값을 ';' 로 구분해서 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        ※ PDF 문서상의 예시에서는 소수점 아래가 존재하는 예시지만, KOAStudio 의 설명과 예시에서는 그렇지 않음.
        아마도 KOAStudio 의 설명을 따르는게 더 바람직할 듯.

        Returns:
            str: 행사가
        """
        ...

    def GetMonthList(self) -> str:
        """
        지수옵션 월물 리스트를 반환한다.

        지수옵션 월물정보를 ';' 로 구분해서 전달하는데 순서는 콜 11월물 ~ 콜 최근월물 풋 최근월물 ~ 풋 최근월물가 됩니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        반환값의 월물간 구분은 ';'
        Ex) 201412;201409;201408;201407;201407;201408;201409;201412

        Returns:
            str: 월물 (YYYYMM;YYYYMM;...)
        """
        ...

    def GetOptionCode(self, strActPrice: str, nCp: int, strMonth: str) -> str:
        """
        행사가와 월물 콜풋으로 종목코드를 구한다.

        인자로 지정한 지수옵션 코드를 전달합니다.

        로그인 한 후에 사용할 수 있는 함수입니다.

        Args:
            strActPrice (str): 행사가 (소수점 포함)
            nCp (int): 콜/풋 구분 (2:콜, 3:풋)
            strMonth (str): 월물 (6자리, YYYYMM)

        Returns:
            str: 종목코드

        Examples:
            >>> GetOptionCode("260.00", 2, "201407")
        """
        ...

    def GetOptionCodeByMonth(self, sTrCode: str, nCp: int, strMonth: str) -> str:
        """
        입력된 종목코드와 동일한 행사가의 코드중 입력한 월물의 코드를 구한다.

        Args:
            sTrCode (str): 종목코드
            nCp (int): 콜/풋 구분 (2:콜, 3:풋)
            strMonth (str): 월물 (6자리, YYYYMM)

        Returns:
            str: 종목코드

        Examples:
            >>> GetOptionCodeByMonth("201J7260", 2, "201412")
            "201JC260"
        """
        ...

    def GetOptionCodeByActPrice(self, sTrCode: str, nCp: int, nTick: int) -> str:
        """
        입력된 종목코드와 동일한 월물의 코드중 입력한 틱만큼 벌어진 코드를 구한다.

        Args:
            sTrCode (str): 종목코드
            nCp (int): 콜/풋 구분 (2:콜, 3:풋)
            nTick (int): 행사가 틱

        Returns:
            str: 종목코드

        Examples:
            >>> GetOptionCodeByActPrice("201J7260", 2, -1)
            "201J7262"
        """
        ...

    def GetSFutureList(self, strBaseAssetCode: str) -> str:
        """
        주식선물 코드 리스트를 반환한다.

        출력값의 코드간 구분은 ';' 이다.

        Args:
            strBaseAssetCode (str): 기초자산코드

        Return:
            str: 종목코드 리스트
        """
        ...

    def GetSFutureCodeByIndex(self, strBaseAssetCode: str, nIndex: int) -> str:
        """
        주식선물 코드를 반환한다.

        Args:
            strBaseAssetCode (str): 기초자산코드
            nIndex (int): 0 ~ 3: 지수선물코드, 4 ~ 7: 지수스프레드, 8 ~ 11: 스타 선물, 12 ~ : 스타 스프레드

        Return:
            str: 종목코드 리스트

        Examples:
            >>> GetSFutureCodeByIndex("11", 0)
        """
        ...

    def GetSActPriceList(self, strBaseAssetGb: str) -> str:
        """
        주식옵션 행사가 리스트를 반환한다.

        Args:
            strBaseAssetGb (str): 기초자산코드구분

        Return:
            str: 행사가 리스트, 행사가간 구분은 ';'

        Examples:
            >>> GetSActPriceList("11")
        """
        ...

    def GetSMonthList(self, strBaseAssetGb: str) -> str:
        """
        주식옵션 월물 리스트를 반환한다.

        Args:
            strBaseAssetGb (str): 기초자산코드구분

        Return:
            str: 월물 리스트, 월물간 구분은 ';'

        Examples:
            >>> GetSMonthList("11")
        """
        ...

    def GetSOptionCode(
        self, strBaseAssetGb: str, strActPrice: str, nCp: int, strMonth: str
    ) -> str:
        """
        주식옵션 코드를 반환한다.

        Args:
            strBaseAssetGb (str): 기초자산코드구분
            strActPrice (str): 행사가 (소수점 포함)
            nCp (int): 콜/풋 구분 (2:콜, 3:풋)
            strMonth (str): 월물 (6자리, YYYYMM)

        Returns:
            str: 주식옵션 코드

        Examples:
            >>> GetSOptionCode("11", "1300000", 2, "1412")
        """
        ...

    def GetSOptionCodeByMonth(
        self, strBaseAssetGb: str, sTrCode: str, nCp: int, strMonth: str
    ) -> str:
        """
        입력한 주식옵션 코드에서 월물만 변경하여 반환한다.

        Args:
            strBaseAssetGb (str): 기초자산코드구분
            sTrCode (str): 종목코드
            nCp (int): 콜/풋 구분 (2:콜, 3:풋)
            strMonth (str): 월물 (6자리, YYYYMM)

        Returns:
            str: 주식옵션 코드

        Examples:
            >>> GetSOptionCodeByMonth("11", "211J8045", 2, "1412")
        """
        ...

    def GetSOptionCodeByActPrice(
        self, strBaseAssetGb: str, sTrCode: str, nCp: int, nTick: int
    ) -> str:
        """
        입력한 주식옵션 코드에서 행사가만 변경하여 반환한다.

        Args:
            strBaseAssetGb (str): 기초자산코드구분
            sTrCode (str): 종목코드
            nCp (int): 콜/풋 구분 (2:콜, 3:풋)
            nTick (int): 행사가 틱

        Returns:
            str: 주식옵션 코드

        Examples:
            >>> GetSOptionCodeByActPrice("11", "211J8045", 2, 4);
        """
        ...

    def GetSFOBasisAssetList(self) -> str:
        """
        주식선옵 기초자산코드/종목명을 반환한다.

        Returns:
            str: 기초자산코드/종목명, 코드와 종목명 구분은 '|', 코드간 구분은 ';'
        """
        ...

    def GetOptionATM(self) -> str:
        """
        지수옵션 ATM을 반환한다.

        Returns:
            str: ATM
        """
        ...

    def GetSOptionATM(self, strBaseAssetGb: str) -> str:
        """
        주식옵션 ATM을 반환한다.

        Returns:
            str: ATM
        """
        ...

    def GetBranchCodeName(self) -> str:
        """
        회원사 코드와 이름을 반환합니다.

        Returns:
            str: 회원사코드/회원사명, 코드와 이름 구분은 '|', 코드간 구분은 ';' (회원사코드|회원사명;회원사코드|회원사명;...)
        """
        ...

    def CommInvestRqData(self, sMarketGb: str, sRQName: str, sScreenNo: str) -> int:
        """
        지원하지 않는 함수.

        시장 구분:
            - 001: 코스피
            - 002: 코스닥
            - 003: 선물
            - 004: 콜옵션
            - 005: 풋옵션
            - 006: 스타선물
            - 007: 주식선물
            - 008: 3년국채
            - 009: 5년국채
            - 010: 10년국채
            - 011: 달러선물
            - 012: 엔선물
            - 013: 유로선물
            - 014: 미니금선물
            - 015: 금선물
            - 016: 돈육선물
            - 017: 달러콜옵션
            - 018: 달러풋옵션

        Args:
            sMarketGb (str): 시장구분
            sRQName (str): 사용자 구분값
            sScreenNo (str): 화면번호 (4자리)

        Returns:
            str: 통신결과

        Examples:
            >>> CommInvestRqData("T00108;T00109", 0, 2, "RQ_1", "0101")
        """
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
        """
        신용주식 주문을 서버로 전송한다.

        서버에 주문을 전송하는 함수 입니다.
        국내주식 신용주문 전용함수입니다. 대주거래는 지원하지 않습니다.

        거래 구분:
            - 00: 지정가
            - 03: 시장가
            - 05: 조건부지정가
            - 06: 최유리지정가
            - 07: 최우선지정가
            - 10: 지정가IOC
            - 13: 시장가IOC
            - 16: 최유리IOC
            - 20: 지정가FOK
            - 23: 시장가FOK
            - 26: 최유리FOK
            - 61: 장전시간외종가
            - 62: 시간외단일가매매
            - 81: 장후시간외종가

        ※ 모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

        신용거래 구분:
            - 03: 신용매수 주문 \\- 자기융자
                - 대출일은 공백 입력
            - 33: 신용매도 융자상환 주문 \\- 자기융자
                - 대출일은 종목별 대출일 입력
                - OPW00005/OPW00004 TR조회로 대출일 조회
            - 99: 신용매도 자기융자 합
                - 대출일은 "99991231" 입력
                - 단, 신용잔고 5개 까지만 융자합 주문 가능

        대출일은 YYYYMMDD 형식입니다.
        신용매도 - 자기융자 일때는 종목별 대출일을 입력하고 신용매도 - 융자합이면 "99991231"을 입력합니다.

        Args:
            sRQName (str): 사용자 구분 요청명
            sScreenNo (str): 화면번호 (4자리)
            sAccNo (str): 계좌번호 (10자리)
            nOrderType (int): 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정)
            sCode (str): 종목코드 (6자리)
            nQty (int): 주문수량
            nPrice (int): 주문단가
            sHogaGb (str): 거래구분
            sCreditGb (str): 신용구분
            sLoanDate (str): 대출일 (8자리, YYYYMMDD)
            sOrgOrderNo (str): 원주문번호

        Returns:
            int: 에러코드, 성공하면 0 을, 실패하면 음수를 반환
        """
        ...

    def KOA_Functions(self, sFunctionName: str, sParam: str) -> str:
        """
        OpenAPI 기본 기능 이외의 기능들을 제공하는 헬퍼 함수.

        KOA_Function() 함수는 OpenAPI 기본 기능 이외의 기능을 사용하기 쉽도록 만든 함수입니다.
        두 개의 인자값을 사용합니다.

        기능 목록:

            1. 계좌 비밀번호 입력창 출력

            >>> KOA_Functions("ShowAccountWindow", "")

            2. 접속 서버 확인 (1:모의투자, 나머지:실서버)

            >>> KOA_Functions("GetServerGubun", "")

            3. 주식종목 시장구분, 종목분류등 정보제공 (구분자는 '|' 와 ';')
            호출결과는 입력한 종목에 대한 대분류, 중분류, 업종구분값을 구분자로 연결한 문자열입니다.

            >>> KOA_Functions("GetMasterStockInfo", "039490")
            "시장구분0|거래소;시장구분1|중형주;업종구분|금융업;"

            4. 조건검색 종목코드와 현재가 수신 (실시간 조건검색은 사용할 수 없음)
            조건검색결과에 종목코드와 그 종목의 현재가를 함께 수신하는 방법이며 실시간 조건검색에서는 사용할 수 없고 오직 조건검색에만 사용할수 있습니다.

            >>> KOA_Functions("SetConditionSearchFlag", "AddPrice") # 현재가 포함하도록 설정

            현재가 포함으로 설정시 OnReceiveTrCondition() 이벤트에 "종목코드1^현재가1;종목코드2^현재가2;...종목코드n^현재가n" 형식으로 전달됨.

            >>> KOA_Functions("SetConditionSearchFlag", "DelPrice") # 현재가 미포함 (원래 상태로 전환)

            현재가 미포함시 기존처럼 "종목코드1^종목코드2...종목코드n" 형식으로 전달므로 설정에 따라 수신데이터 처리방법이 달라져야 하므로 주의하셔야 합니다.

            5. 업종코드목록 획득

            >>> KOA_Functions("GetUpjongCode", "0")

            두번째 인자로 사용할 수 있는 값은 0, 1, 2, 4, 7 입니다.
            0:코스피, 1: 코스닥, 2:KOSPI200, 4:KOSPI100(KOSPI50), 7:KRX100

            함수반환값은 "시장구분값,업종코드,업종명|시장구분값,업종코드,업종명|...|시장구분값,업종코드,업종명" 형식입니다.
            즉 하나의 업종코드는 입력한 시장구분값과 업종코드 그리고 그 업종명이 쉼표(,)로 구분되며 각 업종코드는 '|'로 구분됩니다.

            6. 업종이름 획득

            >>> KOA_Functions("GetUpjongNameByCode", "업종코드입력")

            7. ETF 투자유의 종목 여부 (2020/09/17 적용)
            거래소 제도개선으로 ETF/ETN 종목 중 투자유의 종목을 매수주문하는 경우 경고 메세지 창이 출력되도록 기능이 추가 되었습니다.
            (경고 창 출력 시 주문을 중지/전송 선택 가능합니다.)
            주문 함수를 호출하기 전에 특정 종목이 투자유의종목인지 아래와 같은 방법으로 확인할 수 있습니다.

            >>> KOA_Functions("IsOrderWarningETF", "종목코드(6자리)")

            투자유의 종목인 경우 "1" 값이 리턴, 그렇지 않은 경우 "0" 값 리턴. (ETF가 아닌 종목을 입력시 "0" 값 리턴.)

            8. 주식 전종목대상 투자유의 종목 여부 (2020/11/26 적용)
            거래소 제도개선으로 주식 종목 중 정리매매/단기과열/투자위험/투자경고 종목을 매수주문하는 경우
            경고 메세지 창이 출력되도록 기능이 추가 되었습니다. (경고 창 출력 시 주문을 중지/전송 선택 가능합니다.)
            주문 함수를 호출하기 전에 특정 종목이 투자유의종목인지 아래와 같은 방법으로 확인할 수 있습니다.

            >>> KOA_Functions("IsOrderWarningStock", "종목코드(6자리)")

            리턴 값 - "0":해당없음, "2":정리매매, "3":단기과열, "4":투자위험, "5":투자경고

            9. 상장주식수 구하기 (2021/04/08 적용)
            상장주식수를 구하는 GetMasterListedStockCnt() 기존 함수 사용시 특정 종목 데이터가 long 형을 Overflow 하는 현상이 있습니다.
            이에, 상장주식수를 구하는 기능을 신규 추가 합니다. 사용법은 아래와 같습니다.

            >>> KOA_Functions("GetMasterListedStockCntEx", "종목코드(6자리)")

        Args:
            sFunctionName (str): 함수이름 혹은 기능이름
            sParam (str): 함수 매개변수

        Returns:
            str: 결과 데이터
        """
        ...

    def SetInfoData(self, sInfoData: str) -> int:
        """
        다수의 아이디로 자동로그인이 필요할 때 사용한다.

        Args:
            sInfoData (str): 아이디

        Returns:
            int: 통신결과

        Examples:
            >>> SetInfoData("UserID")
        """
        ...

    def SetRealReg(
        self, strScreenNo: str, strCodeList: str, strFidList: str, strOptType: str
    ) -> int:
        """
        실시간 등록을 한다.

        종목코드와 FID 리스트를 이용해서 실시간 시세를 등록하는 함수입니다.
        한번에 등록가능한 종목과 FID갯수는 100종목, 100개 입니다.
        실시간 등록타입을 0으로 설정하면 등록한 종목들은 실시간 해지되고 등록한 종목만 실시간 시세가 등록됩니다.
        실시간 등록타입을 1로 설정하면 먼저 등록한 종목들과 함께 실시간 시세가 등록됩니다

        strOptType 이 "0" 으로 하면 같은 화면에서 다른 종목 코드로 실시간 등록을 하게 되면
        마지막에 사용한 종목코드만 실시간 등록이 되고 기존에 있던 종목은 실시간이 자동 해지됨.
        "1" 로 하면 같은 화면에서 다른 종목들을 추가하게 되면 기존에 등록한 종목도 함께 실시간 시세를 받을 수 있음.
        꼭 같은 화면이여야 하고 최초 실시간 등록은 "0" 으로 하고 이후부터 "1" 로 등록해야함.

        Args:
            strScreenNo (str): 화면번호 (4자리)
            strCodeList (str): 종목코드 (복수종목가능, ';' 구분자)
            strFidList (str): FID (';' 구분자)
            strOptType (str): 등록타입 (0:최초 등록시, 혹은 기존 등록된 종목 해지하고 등록 1:기존 등록된 종목 유지하고 등록)

        Returns:
            int: 통신결과
        """
        ...

    def GetConditionLoad(self) -> int:
        """
        서버에 저장된 사용자 조건식을 조회해서 임시로 파일에 저장.

        서버에 저장된 사용자 조건검색 목록을 요청합니다.
        조건검색 목록을 모두 수신하면 OnReceiveConditionVer() 이벤트가 발생됩니다.
        조건검색 목록 요청을 성공하면 1, 아니면 0을 리턴합니다.

        System 폴더에 아이디_NewSaveIndex.dat 파일로 저장된다. OCX 가 종료되면 삭제시킨다.
        조건검색 사용시 이 함수를 최소 한번은 호출해야 조건검색을 할 수 있다.
        영웅문에서 사용자 조건을 수정 및 추가하였을 경우에도 최신의 사용자 조건을 받고 싶으면 다시
        조회해야한다.

        Returns:
            int: 성공하면 1, 아니면 0을 반환
        """
        ...

    def GetConditionNameList(self) -> str:
        """
        조건검색 조건명 리스트를 받아온다.

        서버에서 수신한 사용자 조건식을 조건식의 고유번호와 조건식 이름을 한 쌍으로 하는 문자열들로 전달합니다.
        조건식 하나는 조건식의 고유번호와 조건식 이름이 구분자 '^' 로 나뉘어져 있으며 각 조건식은 ';' 로 나뉘어져 있습니다.
        이 함수는 OnReceiveConditionVer() 이벤트에서 사용해야 합니다.

        Returns:
            str: 조건명 리스트 문자열

        Examples:
            >>> GetConditionNameList()
            "1^내조건식1;2^내조건식2;5^내조건식3;..."
        """
        ...

    def SendCondition(
        self, strScrNo: str, strConditionName: str, nIndex: int, nSearch: int
    ) -> int:
        """
        조건검색 종목조회TR을 송신한다.

        서버에 조건검색을 요청하는 함수입니다.
        마지막 인자값으로 조건검색만 할것인지 실시간 조건검색도 수신할 것인지를 지정할 수 있습니다.
        GetConditionNameList() 함수로 얻은 조건식 이름과 고유번호의 쌍을 맞춰서 사용해야 합니다.
        리턴값 1이면 성공이며, 0이면 실패입니다.
        요청한 조건식이 없거나 조건 고유번호와 조건명이 서로 안맞거나 조회횟수를 초과하는 경우 실패하게 됩니다.

        단순 조건식에 맞는 종목을 조회하기 위해서는 조회구분을 0으로 하고,
        실시간 조건검색을 하기 위해서는 조회구분을 1로 한다.
        OnReceiveTrCondition() 으로 결과값이 온다.
        연속조회가 필요한 경우에는 응답받는 곳에서 연속조회 여부에 따라 연속조회를 송신하면된다.

        Args:
            strScrNo (str): 화면번호
            strConditionName (str): 조건식 이름
            nIndex (int): 조건식 인덱스
            nSearch (int): 조회구분 (0:일반조회, 1:실시간조회 (최초 일반조회 + 이후 실시간조회), 2:연속조회)

        Returns:
            int: 성공하면 1, 아니면 0을 반환
        """
        ...

    def SendConditionStop(
        self, strScrNo: str, strConditionName: str, nIndex: int
    ) -> None:
        """
        조건검색 실시간 중지TR을 송신한다.

        실시간 조건검색을 중지할 때 사용하는 함수입니다.
        조건식 조회할때 얻는 조건식 이름과 고유번호의 쌍을 맞춰서 사용해야 합니다.

        해당 조건명의 실시간 조건검색을 중지하거나,
        다른 조건명으로 바꿀 때 이전 조건명으로 실시간 조건검색을 반드시 중지해야한다.
        화면 종료시에도 실시간 조건검색을 한 조건명으로 전부 중지해줘야 한다.

        Args:
            strScrNo (str): 화면번호
            strConditionName (str): 조건식 이름
            nIndex (int): 조건식 인덱스

        Returns:
            None
        """
        ...

    def GetCommDataEx(self, strTrCode: str, strRecordName: str):
        """
        차트 조회 데이터를 배열로 받아온다.

        조회 수신데이터 크기가 큰 차트데이터를 한번에 가져올 목적으로 만든 차트조회 전용함수입니다.

        조회 데이터가 많은 차트 경우 GetCommData()로 항목당 하나씩 받아오는 것 보다
        한번에 데이터 전부를 받아서 사용자가 처리할 수 있도록 배열로 받는다.

        ※ Qt 기준으로 QVariant 타입의 배열을 반환하지만 PySide2 에서는 완전히 똑같이 지원하진 않습니다.

        Args:
            strTrCode (str): TR코드
            strRecordName (str): 레코드명

        Returns:
            QVariant: 조회 데이터 배열
        """
        ...

    def SetRealRemove(self, strScrNo: str, strDelCode: str) -> None:
        """
        종목별 실시간 해제.

        실시간시세 해지 함수이며 화면번호와 종목코드를 이용해서 상세하게 설정할 수 있습니다.

        ※ A종목에 대한 실시간이 여러 화면번호로 중복 등록되어 있는 경우 특정 화면번호를 이용한
        SetRealRemove() 함수호출시 A종목의 실시간시세는 해지되지 않습니다.

        SetRealReg() 함수로 실시간 등록한 종목만 실시간 해제 할 수 있다.

        Args:
            strScrNo (str): 화면번호 (4자리) 또는 "ALL"
            strDelCode (str): 종목코드 또는 "ALL"

        Returns:
            None
        """
        ...

    def GetMarketType(self, sTrCode: str) -> int:
        """
        주어진 종목코드의 시장구분값을 가져온다.

        시장 구분:
            - 0: 장내
            - 3: ELW
            - 4: 뮤추얼펀드
            - 5: 신주인수권
            - 6: 리츠
            - 8: ETF
            - 9: 하이일드펀드
            - 10: 코스닥
            - 30: K-OTC
            - 50: 코넥스 (KONEX)

        Args:
            sTrCode (str): 종목코드

        Returns:
            int: 시장 구분값
        """
        ...
