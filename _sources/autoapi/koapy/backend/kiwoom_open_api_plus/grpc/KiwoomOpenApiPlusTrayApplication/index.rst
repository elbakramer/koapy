:mod:`koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusTrayApplication`
===============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusTrayApplication


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusTrayApplication.QObjectWithLoggingMeta
   koapy.backend.kiwoom_open_api_plus.grpc.KiwoomOpenApiPlusTrayApplication.KiwoomOpenApiPlusTrayApplication




.. class:: QObjectWithLoggingMeta(cls, clsname, bases, dct)


   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`type`\ (\ :py:obj:`QObject`\ )


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



