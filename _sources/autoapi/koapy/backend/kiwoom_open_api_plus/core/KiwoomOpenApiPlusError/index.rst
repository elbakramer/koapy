:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError`
========================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError


Module Contents
---------------

.. py:exception:: KiwoomOpenApiPlusError(message=None)

   Bases: :py:obj:`Exception`

   Common base class for all non-exit exceptions.

   .. py:method:: message(self)
      :property:


   .. py:method:: try_or_raise(cls, arg, message=None)
      :classmethod:


   .. py:method:: try_or_raise_boolean(cls, arg, message)
      :classmethod:


   .. py:method:: get_error_message_by_code(cls, code, default=None)
      :classmethod:



.. py:exception:: KiwoomOpenApiPlusNegativeReturnCodeError(code, message=None)

   Bases: :py:obj:`KiwoomOpenApiPlusError`

   Common base class for all non-exit exceptions.

   .. py:attribute:: OP_ERR_NONE
      :annotation: = 0

      

   .. py:attribute:: OP_ERR_FAIL
      

      

   .. py:attribute:: OP_ERR_COND_NOTFOUND
      

      

   .. py:attribute:: OP_ERR_COND_MISMATCH
      

      

   .. py:attribute:: OP_ERR_COND_OVERFLOW
      

      

   .. py:attribute:: OP_ERR_TR_FAIL
      

      

   .. py:attribute:: OP_ERR_LOGIN
      

      

   .. py:attribute:: OP_ERR_CONNECT
      

      

   .. py:attribute:: OP_ERR_VERSION
      

      

   .. py:attribute:: OP_ERR_FIREWALL
      

      

   .. py:attribute:: OP_ERR_MEMORY
      

      

   .. py:attribute:: OP_ERR_INPUT
      

      

   .. py:attribute:: OP_ERR_SOCKET_CLOSED
      

      

   .. py:attribute:: OP_ERR_SISE_OVERFLOW
      

      

   .. py:attribute:: OP_ERR_RQ_STRUCT_FAIL
      

      

   .. py:attribute:: OP_ERR_RQ_STRING_FAIL
      

      

   .. py:attribute:: OP_ERR_NO_DATA
      

      

   .. py:attribute:: OP_ERR_OVER_MAX_DATA
      

      

   .. py:attribute:: OP_ERR_DATA_RCV_FAIL
      

      

   .. py:attribute:: OP_ERR_OVER_MAX_FID
      

      

   .. py:attribute:: OP_ERR_REAL_CANCEL
      

      

   .. py:attribute:: OP_ERR_ORD_WRONG_INPUT
      

      

   .. py:attribute:: OP_ERR_ORD_WRONG_ACCTNO
      

      

   .. py:attribute:: OP_ERR_OTHER_ACC_USE
      

      

   .. py:attribute:: OP_ERR_MIS_2BILL_EXC
      

      

   .. py:attribute:: OP_ERR_MIS_5BILL_EXC
      

      

   .. py:attribute:: OP_ERR_MIS_1PER_EXC
      

      

   .. py:attribute:: OP_ERR_MIS_3PER_EXC
      

      

   .. py:attribute:: OP_ERR_SEND_FAIL
      

      

   .. py:attribute:: OP_ERR_ORD_OVERFLOW
      

      

   .. py:attribute:: OP_ERR_ORD_OVERFLOW2
      

      

   .. py:attribute:: OP_ERR_MIS_300CNT_EXC
      

      

   .. py:attribute:: OP_ERR_MIS_500CNT_EXC
      

      

   .. py:attribute:: OP_ERR_ORD_WRONG_ACCTINFO
      

      

   .. py:attribute:: OP_ERR_ORD_SYMCODE_EMPTY
      

      

   .. py:attribute:: MSG_ERR_NONE
      :annotation: = 정상처리

      

   .. py:attribute:: MSG_ERR_FAIL
      :annotation: = 실패

      

   .. py:attribute:: MSG_ERR_COND_NOTFOUND
      :annotation: = 조건번호 없음

      

   .. py:attribute:: MSG_ERR_COND_MISMATCH
      :annotation: = 조건번호와 조건식 틀림

      

   .. py:attribute:: MSG_ERR_COND_OVERFLOW
      :annotation: = 조건검색 조회요청 초과

      

   .. py:attribute:: MSG_ERR_TR_FAIL
      :annotation: = 전문 처리 실패

      

   .. py:attribute:: MSG_ERR_LOGIN
      :annotation: = 사용자정보 교환 실패

      

   .. py:attribute:: MSG_ERR_CONNECT
      :annotation: = 서버접속 실패

      

   .. py:attribute:: MSG_ERR_VERSION
      :annotation: = 버전처리 실패

      

   .. py:attribute:: MSG_ERR_FIREWALL
      :annotation: = 개인방화벽 실패

      

   .. py:attribute:: MSG_ERR_MEMORY
      :annotation: = 메모리보호 실패

      

   .. py:attribute:: MSG_ERR_INPUT
      :annotation: = 함수입력값 오류

      

   .. py:attribute:: MSG_ERR_SOCKET_CLOSED
      :annotation: = 통신 연결종료

      

   .. py:attribute:: MSG_ERR_SISE_OVERFLOW
      :annotation: = 시세조회 과부하

      

   .. py:attribute:: MSG_ERR_RQ_STRUCT_FAIL
      :annotation: = 전문작성 초기화 실패

      

   .. py:attribute:: MSG_ERR_RQ_STRING_FAIL
      :annotation: = 전문작성 입력값 오류

      

   .. py:attribute:: MSG_ERR_NO_DATA
      :annotation: = 데이터 없음

      

   .. py:attribute:: MSG_ERR_OVER_MAX_DATA
      :annotation: = 조회 가능한 종목수 초과

      

   .. py:attribute:: MSG_ERR_DATA_RCV_FAIL
      :annotation: = 데이터수신 실패

      

   .. py:attribute:: MSG_ERR_OVER_MAX_FID
      :annotation: = 조회 가능한 FID수 초과

      

   .. py:attribute:: MSG_ERR_REAL_CANCEL
      :annotation: = 실시간 해제 오류

      

   .. py:attribute:: MSG_ERR_ORD_WRONG_INPUT
      :annotation: = 입력값 오류

      

   .. py:attribute:: MSG_ERR_ORD_WRONG_ACCTNO
      :annotation: = 계좌 비밀번호 없음

      

   .. py:attribute:: MSG_ERR_OTHER_ACC_USE
      :annotation: = 타인계좌사용 오류

      

   .. py:attribute:: MSG_ERR_MIS_2BILL_EXC
      :annotation: = 주문가격이 20억원을 초과

      

   .. py:attribute:: MSG_ERR_MIS_5BILL_EXC
      :annotation: = 주문가격이 50억원을 초과

      

   .. py:attribute:: MSG_ERR_MIS_1PER_EXC
      :annotation: = 주문수량이 총발행주수의 1%초과오류

      

   .. py:attribute:: MSG_ERR_MIS_3PER_EXC
      :annotation: = 주문수량이 총발행주수의 3%초과오류

      

   .. py:attribute:: MSG_ERR_SEND_FAIL
      :annotation: = 주문전송 실패

      

   .. py:attribute:: MSG_ERR_ORD_OVERFLOW
      :annotation: = 주문전송 과부하

      

   .. py:attribute:: MSG_ERR_ORD_OVERFLOW2
      :annotation: = 주문전송 과부하

      

   .. py:attribute:: MSG_ERR_MIS_300CNT_EXC
      :annotation: = 주문수량 300계약 초과

      

   .. py:attribute:: MSG_ERR_MIS_500CNT_EXC
      :annotation: = 주문수량 500계약 초과

      

   .. py:attribute:: MSG_ERR_ORD_WRONG_ACCTINFO
      :annotation: = 계좌정보없음

      

   .. py:attribute:: MSG_ERR_ORD_SYMCODE_EMPTY
      :annotation: = 종목코드없음

      

   .. py:attribute:: ERROR_MESSAGE_BY_CODE
      

      

   .. py:method:: get_error_message_by_code(cls, code, default=None)
      :classmethod:


   .. py:method:: check_code_or_raise(cls, code)
      :classmethod:


   .. py:method:: wrap_to_check_code_or_raise(cls, func)
      :classmethod:


   .. py:method:: try_or_raise(cls, arg, message=None)
      :classmethod:


   .. py:method:: __str__(self)

      Return str(self).


   .. py:method:: __repr__(self)

      Return repr(self).


   .. py:method:: code(self)
      :property:



.. py:exception:: KiwoomOpenApiPlusBooleanReturnCodeError(code, message=None)

   Bases: :py:obj:`KiwoomOpenApiPlusError`

   Common base class for all non-exit exceptions.

   .. py:attribute:: OP_ERR_SUCCESS
      :annotation: = 1

      

   .. py:attribute:: OP_ERR_FAILURE
      :annotation: = 0

      

   .. py:method:: check_code_or_raise(cls, code, message=None)
      :classmethod:


   .. py:method:: wrap_to_check_code_or_raise(cls, func, message=None)
      :classmethod:


   .. py:method:: try_or_raise(cls, arg, message=None)
      :classmethod:


   .. py:method:: __str__(self)

      Return str(self).


   .. py:method:: __repr__(self)

      Return repr(self).


   .. py:method:: code(self)
      :property:



