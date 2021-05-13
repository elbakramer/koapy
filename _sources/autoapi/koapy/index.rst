:mod:`koapy`
============

.. py:module:: koapy

.. autoapi-nested-parse::

   Top-level package for KOAPY.



Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   backend/index.rst
   backtrader/index.rst
   compat/index.rst
   utils/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   cli/index.rst
   config/index.rst


Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.CybosPlusEntrypoint
   koapy.CybosPlusEntrypointProxy
   koapy.KiwoomOpenApiPlusEntrypoint
   koapy.KiwoomOpenApiPlusQAxWidget
   koapy.KiwoomOpenApiPlusRealType
   koapy.KiwoomOpenApiPlusScreenManager
   koapy.KiwoomOpenApiPlusTrInfo
   koapy.KiwoomOpenApiPlusVersionUpdater
   koapy.KiwoomOpenApiPlusTrayApplication




Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.__author__
   koapy.__email__
   koapy.__version__


.. data:: __author__
   :annotation: = Yunseong Hwang

   

.. data:: __email__
   :annotation: = kika1492@gmail.com

   

.. data:: __version__
   :annotation: = 0.4.0

   

.. class:: CybosPlusEntrypoint


   Bases: :py:obj:`koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin.CybosPlusEntrypointMixin`

   http://cybosplus.github.io/

   .. method:: __getattr__(self, name)



.. exception:: CybosPlusError


   Bases: :py:obj:`Exception`

   Common base class for all non-exit exceptions.


.. exception:: CybosPlusRequestError(code, message=None)


   Bases: :py:obj:`CybosPlusError`

   아래 문서에서 [BlockRequest/Blockrequest2/Request의 리턴값] 내용 참조
   http://cybosplus.github.io/cputil_rtf_1_/cybosplus_interface.htm

   .. attribute:: ERROR_MESSAGE_BY_CODE
      

      

   .. method:: get_error_message_by_code(cls, code, default=None)
      :classmethod:


   .. method:: check_code_or_raise(cls, code)
      :classmethod:


   .. method:: wrap_to_check_code_or_raise(cls, func)
      :classmethod:


   .. method:: try_or_raise(cls, arg)
      :classmethod:


   .. method:: __str__(self)

      Return str(self).


   .. method:: __repr__(self)

      Return repr(self).


   .. method:: code(self)
      :property:


   .. method:: message(self)
      :property:



.. class:: CybosPlusEntrypointProxy(host=None, port=None)


   Bases: :py:obj:`koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin.CybosPlusEntrypointMixin`

   .. method:: __getattr__(self, name)



.. class:: KiwoomOpenApiPlusEntrypoint(port=None, client_check_timeout=None, verbosity=None, log_level=None)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEntrypointMixin.KiwoomOpenApiPlusEntrypointMixin`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: __del__(self)


   .. method:: __enter__(self)


   .. method:: __exit__(self, exc_type, exc_value, traceback)


   .. method:: get_stub(self)


   .. method:: close_client(self)


   .. method:: close_server_proc(self)


   .. method:: close(self)


   .. method:: __getattr__(self, name)



.. exception:: KiwoomOpenApiPlusBooleanReturnCodeError(code, message=None)


   Bases: :py:obj:`KiwoomOpenApiPlusError`

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



.. exception:: KiwoomOpenApiPlusError(message=None)


   Bases: :py:obj:`Exception`

   Common base class for all non-exit exceptions.

   .. method:: message(self)
      :property:


   .. method:: try_or_raise(cls, arg, message=None)
      :classmethod:


   .. method:: try_or_raise_boolean(cls, arg, message)
      :classmethod:


   .. method:: get_error_message_by_code(cls, code, default=None)
      :classmethod:



.. exception:: KiwoomOpenApiPlusNegativeReturnCodeError(code, message=None)


   Bases: :py:obj:`KiwoomOpenApiPlusError`

   Common base class for all non-exit exceptions.

   .. attribute:: OP_ERR_NONE
      :annotation: = 0

      

   .. attribute:: OP_ERR_FAIL
      

      

   .. attribute:: OP_ERR_COND_NOTFOUND
      

      

   .. attribute:: OP_ERR_COND_MISMATCH
      

      

   .. attribute:: OP_ERR_COND_OVERFLOW
      

      

   .. attribute:: OP_ERR_TR_FAIL
      

      

   .. attribute:: OP_ERR_LOGIN
      

      

   .. attribute:: OP_ERR_CONNECT
      

      

   .. attribute:: OP_ERR_VERSION
      

      

   .. attribute:: OP_ERR_FIREWALL
      

      

   .. attribute:: OP_ERR_MEMORY
      

      

   .. attribute:: OP_ERR_INPUT
      

      

   .. attribute:: OP_ERR_SOCKET_CLOSED
      

      

   .. attribute:: OP_ERR_SISE_OVERFLOW
      

      

   .. attribute:: OP_ERR_RQ_STRUCT_FAIL
      

      

   .. attribute:: OP_ERR_RQ_STRING_FAIL
      

      

   .. attribute:: OP_ERR_NO_DATA
      

      

   .. attribute:: OP_ERR_OVER_MAX_DATA
      

      

   .. attribute:: OP_ERR_DATA_RCV_FAIL
      

      

   .. attribute:: OP_ERR_OVER_MAX_FID
      

      

   .. attribute:: OP_ERR_REAL_CANCEL
      

      

   .. attribute:: OP_ERR_ORD_WRONG_INPUT
      

      

   .. attribute:: OP_ERR_ORD_WRONG_ACCTNO
      

      

   .. attribute:: OP_ERR_OTHER_ACC_USE
      

      

   .. attribute:: OP_ERR_MIS_2BILL_EXC
      

      

   .. attribute:: OP_ERR_MIS_5BILL_EXC
      

      

   .. attribute:: OP_ERR_MIS_1PER_EXC
      

      

   .. attribute:: OP_ERR_MIS_3PER_EXC
      

      

   .. attribute:: OP_ERR_SEND_FAIL
      

      

   .. attribute:: OP_ERR_ORD_OVERFLOW
      

      

   .. attribute:: OP_ERR_ORD_OVERFLOW2
      

      

   .. attribute:: OP_ERR_MIS_300CNT_EXC
      

      

   .. attribute:: OP_ERR_MIS_500CNT_EXC
      

      

   .. attribute:: OP_ERR_ORD_WRONG_ACCTINFO
      

      

   .. attribute:: OP_ERR_ORD_SYMCODE_EMPTY
      

      

   .. attribute:: MSG_ERR_NONE
      :annotation: = 정상처리

      

   .. attribute:: MSG_ERR_FAIL
      :annotation: = 실패

      

   .. attribute:: MSG_ERR_COND_NOTFOUND
      :annotation: = 조건번호 없음

      

   .. attribute:: MSG_ERR_COND_MISMATCH
      :annotation: = 조건번호와 조건식 틀림

      

   .. attribute:: MSG_ERR_COND_OVERFLOW
      :annotation: = 조건검색 조회요청 초과

      

   .. attribute:: MSG_ERR_TR_FAIL
      :annotation: = 전문 처리 실패

      

   .. attribute:: MSG_ERR_LOGIN
      :annotation: = 사용자정보 교환 실패

      

   .. attribute:: MSG_ERR_CONNECT
      :annotation: = 서버접속 실패

      

   .. attribute:: MSG_ERR_VERSION
      :annotation: = 버전처리 실패

      

   .. attribute:: MSG_ERR_FIREWALL
      :annotation: = 개인방화벽 실패

      

   .. attribute:: MSG_ERR_MEMORY
      :annotation: = 메모리보호 실패

      

   .. attribute:: MSG_ERR_INPUT
      :annotation: = 함수입력값 오류

      

   .. attribute:: MSG_ERR_SOCKET_CLOSED
      :annotation: = 통신 연결종료

      

   .. attribute:: MSG_ERR_SISE_OVERFLOW
      :annotation: = 시세조회 과부하

      

   .. attribute:: MSG_ERR_RQ_STRUCT_FAIL
      :annotation: = 전문작성 초기화 실패

      

   .. attribute:: MSG_ERR_RQ_STRING_FAIL
      :annotation: = 전문작성 입력값 오류

      

   .. attribute:: MSG_ERR_NO_DATA
      :annotation: = 데이터 없음

      

   .. attribute:: MSG_ERR_OVER_MAX_DATA
      :annotation: = 조회 가능한 종목수 초과

      

   .. attribute:: MSG_ERR_DATA_RCV_FAIL
      :annotation: = 데이터수신 실패

      

   .. attribute:: MSG_ERR_OVER_MAX_FID
      :annotation: = 조회 가능한 FID수 초과

      

   .. attribute:: MSG_ERR_REAL_CANCEL
      :annotation: = 실시간 해제 오류

      

   .. attribute:: MSG_ERR_ORD_WRONG_INPUT
      :annotation: = 입력값 오류

      

   .. attribute:: MSG_ERR_ORD_WRONG_ACCTNO
      :annotation: = 계좌 비밀번호 없음

      

   .. attribute:: MSG_ERR_OTHER_ACC_USE
      :annotation: = 타인계좌사용 오류

      

   .. attribute:: MSG_ERR_MIS_2BILL_EXC
      :annotation: = 주문가격이 20억원을 초과

      

   .. attribute:: MSG_ERR_MIS_5BILL_EXC
      :annotation: = 주문가격이 50억원을 초과

      

   .. attribute:: MSG_ERR_MIS_1PER_EXC
      :annotation: = 주문수량이 총발행주수의 1%초과오류

      

   .. attribute:: MSG_ERR_MIS_3PER_EXC
      :annotation: = 주문수량이 총발행주수의 3%초과오류

      

   .. attribute:: MSG_ERR_SEND_FAIL
      :annotation: = 주문전송 실패

      

   .. attribute:: MSG_ERR_ORD_OVERFLOW
      :annotation: = 주문전송 과부하

      

   .. attribute:: MSG_ERR_ORD_OVERFLOW2
      :annotation: = 주문전송 과부하

      

   .. attribute:: MSG_ERR_MIS_300CNT_EXC
      :annotation: = 주문수량 300계약 초과

      

   .. attribute:: MSG_ERR_MIS_500CNT_EXC
      :annotation: = 주문수량 500계약 초과

      

   .. attribute:: MSG_ERR_ORD_WRONG_ACCTINFO
      :annotation: = 계좌정보없음

      

   .. attribute:: MSG_ERR_ORD_SYMCODE_EMPTY
      :annotation: = 종목코드없음

      

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



.. class:: KiwoomOpenApiPlusQAxWidget(*args, **kwargs)


   Bases: :py:obj:`koapy.compat.pyside2.QtWidgets.QWidget`, :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusQAxWidgetMixin`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: CLSID
      :annotation: = {A1574A0D-6BFA-4BD7-9020-DED88711818D}

      

   .. attribute:: PROGID
      :annotation: = KHOPENAPI.KHOpenApiCtrl.1

      

   .. attribute:: METHOD_NAMES
      

      

   .. attribute:: EVENT_NAMES
      

      

   .. method:: _onException(self, code, source, desc, help)


   .. method:: __getattr__(self, name)


   .. method:: changeEvent(self, event)


   .. method:: closeEvent(self, event)



.. class:: KiwoomOpenApiPlusRealType(gidc=None, desc=None, nfid=None, fids=None)


   Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

   .. class:: Fid(fid=None, name=None)


      Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

      .. attribute:: __outer_class__
         

         

      .. attribute:: _FID_DUMP_FILENAME
         :annotation: = fid.xlsx

         

      .. attribute:: _NAME_BY_FID
         

         

      .. method:: __repr__(self)

         Return repr(self).


      .. method:: name_by_fid_from_dump_file(cls, dump_file=None)
         :classmethod:


      .. method:: load_from_dump_file(cls, dump_file=None)
         :classmethod:


      .. method:: get_name_by_fid(cls, fid, default=None)
         :classmethod:



   .. attribute:: _REALTYPE_BY_DESC_DUMP_FILENAME
      :annotation: = realtype_by_desc.json

      

   .. attribute:: _REALTYPE_BY_DESC
      

      

   .. method:: __repr__(self)

      Return repr(self).


   .. method:: get_realtype_info_by_realtype_name(cls, realtype)
      :classmethod:


   .. method:: get_fids_by_realtype_name(cls, realtype)
      :classmethod:


   .. method:: get_fids_by_realtype_name_as_string(cls, realtype)
      :classmethod:


   .. method:: get_field_names_by_realtype_name(cls, realtype)
      :classmethod:


   .. method:: realtypes_from_datfile(cls, dat_file=None, encoding=None, module_path=None)
      :classmethod:


   .. method:: realtype_by_desc_from_datfile(cls, dat_file=None)
      :classmethod:


   .. method:: dump_realtype_by_desc(cls, dump_file=None, dat_file=None)
      :classmethod:


   .. method:: realtype_by_desc_from_dump_file(cls, dump_file=None)
      :classmethod:


   .. method:: load_from_dump_file(cls, dump_file=None)
      :classmethod:



.. class:: KiwoomOpenApiPlusScreenManager(control=None)


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: _maximum_num
      :annotation: = 200

      

   .. method:: _number_to_screen_no(number)
      :staticmethod:


   .. method:: _screen_no_to_number(screen_no)
      :staticmethod:


   .. method:: is_inuse(self, screen_no)


   .. method:: get_single_free_screen(self, exclude=None)


   .. method:: get_multiple_free_screens(self, count)


   .. method:: get_free_screen(self, count=None)


   .. method:: borrow_screen(self, screen_no=None, reuse=True, pop=True)


   .. method:: return_screen(self, screen_no)



.. class:: KiwoomOpenApiPlusTrInfo(tr_code=None, name=None, tr_name=None, tr_names_svr=None, tr_type=None, gfid=None, inputs=None, single_outputs_name=None, single_outputs=None, multi_outputs_name=None, multi_outputs=None)


   Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. class:: Field(name=None, start=None, offset=None, fid=None)


      Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

      .. attribute:: __outer_class__
         

         

      .. method:: __repr__(self)

         Return repr(self).



   .. attribute:: _TRINFO_BY_CODE_DUMP_FILENAME
      :annotation: = trinfo_by_code.json

      

   .. attribute:: _TRINFO_BY_CODE
      

      

   .. attribute:: _SINGLE_TO_MULTI_TRCODES
      :annotation: = ['opt10075', 'opt10076', 'opt10085', 'optkwfid', 'optkwinv', 'optkwpro']

      

   .. method:: __repr__(self)

      Return repr(self).


   .. method:: to_dict(self)


   .. method:: from_dict(cls, dic)
      :classmethod:


   .. method:: get_input_names(self)


   .. method:: get_single_output_names(self)


   .. method:: get_multi_output_names(self)


   .. method:: get_trinfo_by_code(cls, trcode)
      :classmethod:


   .. method:: from_encfile(cls, f, tr_code=None)
      :classmethod:


   .. method:: infos_from_data_dir(cls, data_dir=None, encoding=None, module_path=None)
      :classmethod:


   .. method:: trinfo_by_code_from_data_dir(cls, data_dir=None)
      :classmethod:


   .. method:: dump_trinfo_by_code(cls, dump_file=None, data_dir=None)
      :classmethod:


   .. method:: _single_outputs_are_actually_multi_outputs(cls, item)
      :classmethod:


   .. method:: trinfo_by_code_from_dump_file(cls, dump_file=None)
      :classmethod:


   .. method:: load_from_dump_file(cls, dump_file=None)
      :classmethod:



.. class:: KiwoomOpenApiPlusVersionUpdater(credential)


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: disable_autologin_impl(cls)
      :classmethod:


   .. method:: disable_autologin(self)


   .. method:: open_login_window_impl(cls)
      :classmethod:


   .. method:: open_login_window(self)


   .. method:: show_account_window_impl(cls)
      :classmethod:


   .. method:: show_account_window(self)


   .. method:: enable_autologin_using_pywinauto(cls, account_passwords)
      :classmethod:


   .. method:: login_using_pywinauto(cls, credential)
      :classmethod:


   .. method:: enable_autologin(self)


   .. method:: try_version_update_using_pywinauto(self)


   .. method:: is_32bit(self)


   .. method:: is_admin(self)


   .. method:: update_version_if_necessary(self)



.. class:: KiwoomOpenApiPlusTrayApplication(args=())


   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QObject`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: _should_restart
      

      

   .. attribute:: _should_restart_exit_code
      :annotation: = 1

      

   .. method:: _checkAndWaitForMaintananceAndThen(self, callback=None, args=None, kwargs=None)

      # 시스템 점검 안내

      안녕하세요. 키움증권 입니다.
      시스템의 안정적인 운영을 위하여
      매일 시스템 점검을 하고 있습니다.
      점검시간은 월~토요일 (05:05 ~ 05:10)
                일요일    (04:00 ~ 04:30) 까지 입니다.
      따라서 해당 시간대에는 접속단절이 될 수 있습니다.
      참고하시기 바랍니다.


   .. method:: _onEventConnect(self, errcode)


   .. method:: _activate(self, reason)


   .. method:: _ensureConnectedAndThen(self, callback=None, args=None, kwargs=None)


   .. method:: _connect(self)


   .. method:: _showAccountWindow(self)


   .. method:: _configureAutoLogin(self)


   .. method:: _openOpenApiHome(self)


   .. method:: _openOpenApiDocument(self)


   .. method:: _openOpenApiQna(self)


   .. method:: _openGithub(self)


   .. method:: _openReadTheDocs(self)


   .. method:: _onSignal(self, signum, _frame)


   .. method:: _exec(self)


   .. method:: _exit(self, return_code=0)


   .. method:: _nextRestartTime(self)


   .. method:: _startRestartNotifier(self)


   .. method:: _exitForRestart(self)


   .. method:: __getattr__(self, name)


   .. method:: control(self)
      :property:


   .. method:: exec_(self)


   .. method:: exit(self, return_code=0)


   .. method:: execAndExit(self)


   .. method:: execAndExitWithAutomaticRestart(self)


   .. method:: main(cls, args)
      :classmethod:



