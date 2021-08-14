:py:mod:`koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusTrayApplication`
=====================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusTrayApplication


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusTrayApplication.KiwoomOpenApiPlusTrayApplication




.. py:class:: KiwoomOpenApiPlusTrayApplication(args=())

   Bases: :py:obj:`koapy.utils.logging.pyside2.QObjectLogging.QObjectLogging`

   .. py:attribute:: shouldRestart
      

      

   .. py:method:: _initializeGrpcServer(self)


   .. py:method:: _startServer(self, ensure_connected=None)


   .. py:method:: _stopServer(self)


   .. py:method:: _deleteControl(self)


   .. py:method:: _stopAndTearDownGrpcServer(self)


   .. py:method:: _reinitializeGrpcServer(self)


   .. py:method:: _reinitializeAndStartGrpcServer(self, ensure_connected=None)


   .. py:method:: _checkAndWaitForMaintananceAndThen(self, callback=None)

      TITLE: 안녕하세요. 키움증권 입니다.
      TIME: 04:45
      BODY:
      안녕하세요. 키움증권 입니다.
      시스템의 안정적인 운영을 위하여
      매일 시스템 점검을 하고 있습니다.
      점검시간은 월~토요일 (05:05 ~ 05:10)
                일요일    (04:00 ~ 04:30) 까지 입니다.
      따라서 해당 시간대에는 접속단절이 될 수 있습니다.
      참고하시기 바랍니다.


   .. py:method:: _onEventConnect(self, errcode)


   .. py:method:: _activate(self, reason)


   .. py:method:: _ensureConnectedAndThen(self, callback=None)


   .. py:method:: _showAccountWindow(self)


   .. py:method:: _openOpenApiHome(self)


   .. py:method:: _openOpenApiDocument(self)


   .. py:method:: _openOpenApiQna(self)


   .. py:method:: _openGithub(self)


   .. py:method:: _openReadTheDocs(self)


   .. py:method:: _onSignal(self, signum, _frame)


   .. py:method:: _setSignalHandlers(self)


   .. py:method:: _restoreSignalHandlers(self)


   .. py:method:: _signalHandlersSet(self)


   .. py:method:: _serverStarted(self)


   .. py:method:: _exec(self)


   .. py:method:: _exit(self, return_code=0)


   .. py:method:: _nextRestartTime(self)

      TITLE: [HTS 재접속 안내]
      TIME: 06:50
      BODY:
      안녕하세요. 키움증권입니다.

      오전 6시 50분 이전에 접속하신 고객님께서는
      영웅문을 재접속하여 주시기 바랍니다.
      재접속을 하지 않을 경우 거래종목 정보, 전일 거래에
      대한 결제분 등이 반영되지 않아 실제 잔고와 차이가
      발생할 수 있습니다.
                             -키움증권-


   .. py:method:: _startRestartNotifier(self)


   .. py:method:: _onShouldRestart(self, code)


   .. py:method:: __getattr__(self, name)


   .. py:method:: control(self)
      :property:


   .. py:method:: exec_(self)


   .. py:method:: exit(self, return_code=0)


   .. py:method:: execAndExit(self)


   .. py:method:: main(cls, args)
      :classmethod:



