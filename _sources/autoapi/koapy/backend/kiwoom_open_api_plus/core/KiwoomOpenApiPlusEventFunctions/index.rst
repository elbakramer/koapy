:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventFunctions`
=================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventFunctions


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventFunctions.KiwoomOpenApiPlusEventFunctions




.. py:class:: KiwoomOpenApiPlusEventFunctions

   .. py:method:: OnReceiveTrData(self, sScrNo: str, sRQName: str, sTrCode: str, sRecordName: str, sPrevNext: str, nDataLength: int, sErrorCode: str, sMessage: str, sSplmMsg: str) -> None

      서버통신 후 데이터를 받은 시점을 알려준다.

      요청했던 조회데이터를 수신했을때 발생됩니다.
      수신된 데이터는 이 이벤트내부에서 GetCommData() 함수를 이용해서 얻어올 수 있습니다.

      파라미터 매핑:
          - sRQName = CommRqData() 의 sRQName과 매핑되는 이름이다.
          - sTrCode = CommRqData() 의 sTrCode과 매핑되는 이름이다.

      :param sScrNo: 화면번호
      :type sScrNo: str
      :param sRQName: 사용자 구분명
      :type sRQName: str
      :param sTrCode: TR 코드
      :type sTrCode: str
      :param sRecordName: 레코드 명
      :type sRecordName: str
      :param sPrevNext: 연속조회 유무 (0:추가조회 데이터 없음, 2:추가조회 데이터 있음)
      :type sPrevNext: str
      :param nDataLength: 사용안함
      :type nDataLength: str
      :param sErrorCode: 사용안함
      :type sErrorCode: str
      :param sMessage: 사용안함
      :type sMessage: str
      :param sSplmMsg: 사용안함
      :type sSplmMsg: str

      :returns: None


   .. py:method:: OnReceiveRealData(self, sRealKey: str, sRealType: str, sRealData: str) -> None

      실시간데이터를 받은 시점을 알려준다.

      실시간시세 데이터가 수신될때마다 종목단위로 발생됩니다.
      SetRealReg() 함수로 등록한 실시간 데이터도 이 이벤트로 전달됩니다.
      GetCommRealData() 함수를 이용해서 수신된 데이터를 얻을수 있습니다.

      :param sRealKey: 종목코드
      :type sRealKey: str
      :param sRealType: 실시간 타입
      :type sRealType: str
      :param sRealData: 실시간 데이터전문 (사용불가)
      :type sRealData: str

      :returns: None


   .. py:method:: OnReceiveMsg(self, sScrNo: str, sRQName: str, sTrCode: str, sMsg: str) -> None

      서버통신 후 메시지를 받은 시점을 알려준다.

      주문전송 또는 데이터 조회요청 후 서버 메시지가 수신됩니다.
      ※ 메시지에 포함된 6자리 코드번호는 변경될 수 있으니, 여기에 수신된 코드번호를 특정 용도로 사용하지 마시기 바랍니다.

      파라미터 매핑:
          - sScrNo = CommRqData() 의 sScrNo와 매핑된다.
          - sRQName = CommRqData() 의 sRQName 와 매핑된다.
          - sTrCode = CommRqData() 의 sTrCode 와 매핑된다.

      메시지 예시:
          - "조회가 완료되었습니다."
          - "증거금 부족으로 주문이 거부되었습니다."
          - "정정할 원주문 내역이 없습니다."
          - "비밀번호 입력을 확인해주시기 바랍니다."

      :param sScrNo: str, sRQName: str, sTrCode: str, sMsg: str

      :returns: None


   .. py:method:: OnReceiveChejanData(self, sGubun: str, nItemCnt: int, sFIdList: str) -> None

      체결데이터를 받은 시점을 알려준다.

      주문전송 후 주문접수, 체결통보, 잔고통보를 수신할 때 마다 발생됩니다.
      GetChejanData() 함수를 이용해서 FID 항목별 값을 얻을수 있습니다.

      :param sGubun: 체결구분 (0:주문체결통보, 1:국내주식 잔고통보, 4:파생상품 잔고통보)
      :type sGubun: str
      :param nItemCnt: 아이템 개수
      :type nItemCnt: int
      :param sFIdList: 데이터 리스트 (';' 구분자)
      :type sFIdList: str

      :returns: None


   .. py:method:: OnEventConnect(self, nErrCode: int) -> None

      서버 접속 관련 이벤트.

      로그인 처리 이벤트입니다. 성공이면 인자값 nErrCode가 0이며 에러는 다음과 같은 값이 전달됩니다.

      에러코드 구분:
          - OP_ERR_LOGIN(-100): 사용자 정보교환 실패
          - OP_ERR_CONNECT(-101): 서버접속 실패
          - OP_ERR_VERSION(-102): 버전처리 실패

      :param nErrCode: 에러코드 (0:로그인 성공, 음수:실패)
      :type nErrCode: int

      :returns: None


   .. py:method:: OnReceiveInvestRealData(self, sRealKey: str) -> None

      더 이상 지원하지 않는 함수.


   .. py:method:: OnReceiveRealCondition(self, sTrCode: str, strType: str, strConditionName: str, strConditionIndex: str) -> None

      조건검색 실시간 편입,이탈 종목을 받을 시점을 알려준다.

      실시간 조건검색 요청으로 신규종목이 편입되거나 기존 종목이 이탈될때 마다 발생됩니다.
      ※ 편입되었다가 순간적으로 다시 이탈되는 종목에대한 신호는 조건검색 서버마다 차이가 발생할 수 있습니다.

      strConditionName 에 해당하는 종목이 실시간으로 들어옴.
      strType 으로 편입된 종목인지 이탈된 종목인지 구분한다.

      :param sTrCode: 종목코드
      :type sTrCode: str
      :param strType: 편입/이탈 구분 (I:편입, D:이탈)
      :type strType: str
      :param strConditionName: 조건식 이름
      :type strConditionName: str
      :param strConditionIndex: 조건식 인덱스
      :type strConditionIndex: str

      :returns: None


   .. py:method:: OnReceiveTrCondition(self, sScrNo: str, strCodeList: str, strConditionName: str, nIndex: int, nNext: int) -> None

      조건검색 조회응답으로 종목리스트를 받는 시점.

      조건검색 요청에대한 서버 응답 수신시 발생하는 이벤트입니다.
      종목코드 리스트는 각 종목코드가 ';' 로 구분되서 전달됩니다.

      :param sScrNo: 화면번호
      :type sScrNo: str
      :param strCodeList: 종목리스트 (';' 구분자)
      :type strCodeList: str
      :param strConditionName: 조건식 이름
      :type strConditionName: str
      :param nIndex: 조건식 인덱스
      :type nIndex: int
      :param nNext: 연속조회 여부 (2:연속조회, 0:연속조회 없음)
      :type nNext: int

      :returns: None


   .. py:method:: OnReceiveConditionVer(self, lRet: int, sMsg: str) -> None

      로컬에 사용자 조건식 저장 성공 여부를 확인하는 시점.

      저장된 사용자 조건식 불러오기 요청에 대한 응답 수신시 발생되는 이벤트입니다.

      :param lRet: 사용자 조건식 저장 성공여부 (1:성공, 나머지:실패)
      :type lRet: int
      :param sMsg: 호출결과 메시지
      :type sMsg: str

      :returns: None



