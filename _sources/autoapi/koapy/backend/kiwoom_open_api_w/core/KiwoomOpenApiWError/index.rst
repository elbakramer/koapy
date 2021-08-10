:py:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWError`
==================================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWError


Module Contents
---------------

.. py:exception:: KiwoomOpenApiWError(message=None)

   Bases: :py:obj:`Exception`

   Common base class for all non-exit exceptions.

   .. py:method:: message(self)
      :property:


   .. py:method:: try_or_raise(cls, arg, message=None)
      :classmethod:


   .. py:method:: try_or_raise_boolean(cls, arg, message)
      :classmethod:



.. py:exception:: KiwoomOpenApiWNegativeReturnCodeError(code, message=None)

   Bases: :py:obj:`KiwoomOpenApiWError`

   Common base class for all non-exit exceptions.

   .. py:attribute:: OP_ERR_NONE
      :annotation: = 0

      

   .. py:attribute:: OP_ERR_NO_LOGIN
      

      

   .. py:attribute:: OP_ERR_LOGIN
      

      

   .. py:attribute:: OP_ERR_CONNECT
      

      

   .. py:attribute:: OP_ERR_VERSION
      

      

   .. py:attribute:: OP_ERR_TRCODE
      

      

   .. py:attribute:: OP_ERR_NO_REGOPENAPI
      

      

   .. py:attribute:: OP_ERR_SISE_OVERFLOW
      

      

   .. py:attribute:: OP_ERR_ORDER_OVERFLOW
      

      

   .. py:attribute:: OP_ERR_RQ_WRONG_INPUT
      

      

   .. py:attribute:: OP_ERR_ORD_WRONG_INPUT
      

      

   .. py:attribute:: OP_ERR_ORD_WRONG_ACCPWD
      

      

   .. py:attribute:: OP_ERR_ORD_WRONG_ACCNO
      

      

   .. py:attribute:: OP_ERR_ORD_WRONG_QTY200
      

      

   .. py:attribute:: OP_ERR_ORD_WRONG_QTY400
      

      

   .. py:attribute:: MSG_ERR_NONE
      :annotation: = 정상처리

      

   .. py:attribute:: MSG_ERR_NO_LOGIN
      :annotation: = 미접속상태

      

   .. py:attribute:: MSG_ERR_LOGIN
      :annotation: = 로그인시 접속 실패 (아이피 오류 또는 접속정보 오류)

      

   .. py:attribute:: MSG_ERR_CONNECT
      :annotation: = 서버 접속 실패

      

   .. py:attribute:: MSG_ERR_VERSION
      :annotation: = 버전처리가 실패하였습니다.

      

   .. py:attribute:: MSG_ERR_TRCODE
      :annotation: = TrCode 가 존재하지 않습니다.

      

   .. py:attribute:: MSG_ERR_NO_REGOPENAPI
      :annotation: = 해외OpenAPI 미신청

      

   .. py:attribute:: MSG_ERR_SISE_OVERFLOW
      :annotation: = 조회과부화

      

   .. py:attribute:: MSG_ERR_ORDER_OVERFLOW
      :annotation: = 주문과부화

      

   .. py:attribute:: MSG_ERR_RQ_WRONG_INPUT
      :annotation: = 조회입력값(명칭/누락) 오류

      

   .. py:attribute:: MSG_ERR_ORD_WRONG_INPUT
      :annotation: = 주문입력갑 오류

      

   .. py:attribute:: MSG_ERR_ORD_WRONG_ACCPWD
      :annotation: = 계좌비밀번호를 입력하십시오.

      

   .. py:attribute:: MSG_ERR_ORD_WRONG_ACCNO
      :annotation: = 타인 계좌를 사용할 수 없습니다.

      

   .. py:attribute:: MSG_ERR_ORD_WRONG_QTY200
      :annotation: = 경고-주문수량 200개 초과

      

   .. py:attribute:: MSG_ERR_ORD_WRONG_QTY400
      :annotation: = 제한-주문수량 400개 초과

      

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



.. py:exception:: KiwoomOpenApiWBooleanReturnCodeError(code, message=None)

   Bases: :py:obj:`KiwoomOpenApiWError`

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



