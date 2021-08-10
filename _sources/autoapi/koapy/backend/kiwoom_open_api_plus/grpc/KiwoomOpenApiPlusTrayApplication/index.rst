:py:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusTrayApplication`
==================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusTrayApplication


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusTrayApplication.QObjectWithLoggingMeta
   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusTrayApplication.KiwoomOpenApiPlusTrayApplication




.. py:class:: QObjectWithLoggingMeta(cls, clsname, bases, dct)

   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`type`\ (\ :py:obj:`QObject`\ )


.. py:class:: KiwoomOpenApiPlusTrayApplication(args=())

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QObject`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:attribute:: _should_restart
      

      

   .. py:attribute:: _should_restart_exit_code
      :annotation: = 1

      

   .. py:method:: _checkAndWaitForMaintananceAndThen(self, callback=None, args=None, kwargs=None)

      # 시스템 점검 안내

      안녕하세요. 키움증권 입니다.
      시스템의 안정적인 운영을 위하여
      매일 시스템 점검을 하고 있습니다.
      점검시간은 월~토요일 (05:05 ~ 05:10)
                일요일    (04:00 ~ 04:30) 까지 입니다.
      따라서 해당 시간대에는 접속단절이 될 수 있습니다.
      참고하시기 바랍니다.


   .. py:method:: _onEventConnect(self, errcode)


   .. py:method:: _activate(self, reason)


   .. py:method:: _ensureConnectedAndThen(self, callback=None, args=None, kwargs=None)


   .. py:method:: _connect(self)


   .. py:method:: _showAccountWindow(self)


   .. py:method:: _configureAutoLogin(self)


   .. py:method:: _openOpenApiHome(self)


   .. py:method:: _openOpenApiDocument(self)


   .. py:method:: _openOpenApiQna(self)


   .. py:method:: _openGithub(self)


   .. py:method:: _openReadTheDocs(self)


   .. py:method:: _onSignal(self, signum, _frame)


   .. py:method:: _exec(self)


   .. py:method:: _exit(self, return_code=0)


   .. py:method:: _nextRestartTime(self)


   .. py:method:: _startRestartNotifier(self)


   .. py:method:: _exitForRestart(self)


   .. py:method:: __getattr__(self, name)


   .. py:method:: control(self)
      :property:


   .. py:method:: exec_(self)


   .. py:method:: exit(self, return_code=0)


   .. py:method:: execAndExit(self)


   .. py:method:: execAndExitWithAutomaticRestart(self)


   .. py:method:: main(cls, args)
      :classmethod:



