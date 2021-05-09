:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWError`
===============================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWError


Module Contents
---------------

.. exception:: KiwoomOpenApiWError(message=None)


   Bases: :py:obj:`Exception`

   Common base class for all non-exit exceptions.

   .. method:: message(self)
      :property:


   .. method:: try_or_raise(cls, arg, message=None)
      :classmethod:


   .. method:: try_or_raise_boolean(cls, arg, message)
      :classmethod:



.. exception:: KiwoomOpenApiWNegativeReturnCodeError(code, message=None)


   Bases: :py:obj:`KiwoomOpenApiWError`

   Common base class for all non-exit exceptions.

   .. attribute:: OP_ERR_NONE
      :annotation: = 0

      

   .. attribute:: OP_ERR_NO_LOGIN
      

      

   .. attribute:: OP_ERR_LOGIN
      

      

   .. attribute:: OP_ERR_CONNECT
      

      

   .. attribute:: OP_ERR_VERSION
      

      

   .. attribute:: OP_ERR_TRCODE
      

      

   .. attribute:: OP_ERR_NO_REGOPENAPI
      

      

   .. attribute:: OP_ERR_SISE_OVERFLOW
      

      

   .. attribute:: OP_ERR_ORDER_OVERFLOW
      

      

   .. attribute:: OP_ERR_RQ_WRONG_INPUT
      

      

   .. attribute:: OP_ERR_ORD_WRONG_INPUT
      

      

   .. attribute:: OP_ERR_ORD_WRONG_ACCPWD
      

      

   .. attribute:: OP_ERR_ORD_WRONG_ACCNO
      

      

   .. attribute:: OP_ERR_ORD_WRONG_QTY200
      

      

   .. attribute:: OP_ERR_ORD_WRONG_QTY400
      

      

   .. attribute:: MSG_ERR_NONE
      :annotation: = 정상처리

      

   .. attribute:: MSG_ERR_NO_LOGIN
      :annotation: = 미접속상태

      

   .. attribute:: MSG_ERR_LOGIN
      :annotation: = 로그인시 접속 실패 (아이피 오류 또는 접속정보 오류)

      

   .. attribute:: MSG_ERR_CONNECT
      :annotation: = 서버 접속 실패

      

   .. attribute:: MSG_ERR_VERSION
      :annotation: = 버전처리가 실패하였습니다.

      

   .. attribute:: MSG_ERR_TRCODE
      :annotation: = TrCode 가 존재하지 않습니다.

      

   .. attribute:: MSG_ERR_NO_REGOPENAPI
      :annotation: = 해외OpenAPI 미신청

      

   .. attribute:: MSG_ERR_SISE_OVERFLOW
      :annotation: = 조회과부화

      

   .. attribute:: MSG_ERR_ORDER_OVERFLOW
      :annotation: = 주문과부화

      

   .. attribute:: MSG_ERR_RQ_WRONG_INPUT
      :annotation: = 조회입력값(명칭/누락) 오류

      

   .. attribute:: MSG_ERR_ORD_WRONG_INPUT
      :annotation: = 주문입력갑 오류

      

   .. attribute:: MSG_ERR_ORD_WRONG_ACCPWD
      :annotation: = 계좌비밀번호를 입력하십시오.

      

   .. attribute:: MSG_ERR_ORD_WRONG_ACCNO
      :annotation: = 타인 계좌를 사용할 수 없습니다.

      

   .. attribute:: MSG_ERR_ORD_WRONG_QTY200
      :annotation: = 경고-주문수량 200개 초과

      

   .. attribute:: MSG_ERR_ORD_WRONG_QTY400
      :annotation: = 제한-주문수량 400개 초과

      

   .. attribute:: ERROR_MESSAGE_BY_CODE
      

      

   .. method:: get_error_message_by_code(cls, code, default=None)
      :classmethod:


   .. method:: check_code_or_raise(cls, code)
      :classmethod:


   .. method:: wrap_to_check_code_or_raise(cls, func)
      :classmethod:


   .. method:: try_or_raise(cls, arg, message=None)
      :classmethod:


   .. method:: __str__(self)

      Return str(self).


   .. method:: __repr__(self)

      Return repr(self).


   .. method:: code(self)
      :property:



.. exception:: KiwoomOpenApiWBooleanReturnCodeError(code, message=None)


   Bases: :py:obj:`KiwoomOpenApiWError`

   Common base class for all non-exit exceptions.

   .. attribute:: OP_ERR_SUCCESS
      :annotation: = 1

      

   .. attribute:: OP_ERR_FAILURE
      :annotation: = 0

      

   .. method:: check_code_or_raise(cls, code, message=None)
      :classmethod:


   .. method:: wrap_to_check_code_or_raise(cls, func, message=None)
      :classmethod:


   .. method:: try_or_raise(cls, arg, message=None)
      :classmethod:


   .. method:: __str__(self)

      Return str(self).


   .. method:: __repr__(self)

      Return repr(self).


   .. method:: code(self)
      :property:



