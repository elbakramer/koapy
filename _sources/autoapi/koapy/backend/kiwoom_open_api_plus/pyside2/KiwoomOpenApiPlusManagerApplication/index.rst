:py:mod:`koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication`
========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusServerApplicationProcess
   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusManagerApplication




.. py:class:: KiwoomOpenApiPlusServerApplicationProcess(args, parent=None)

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QProcess`

   .. py:method:: _onStarted(self)


   .. py:method:: _onFinished(self)



.. py:class:: KiwoomOpenApiPlusManagerApplication(args=())

   Bases: :py:obj:`koapy.utils.logging.pyside2.QObjectLogging.QObjectLogging`

   .. py:attribute:: shouldRestart
      

      

   .. py:method:: _createSystemTrayIcon(self)


   .. py:method:: _activate(self, reason)


   .. py:method:: _createIcon(self)


   .. py:method:: _createTooltip(self)


   .. py:method:: _createContextMenu(self)


   .. py:method:: _ensureConnectedAndThen(self, callback=None)


   .. py:method:: _connect(self)


   .. py:method:: _showAccountWindow(self)


   .. py:method:: _openOpenApiHome(self)


   .. py:method:: _openOpenApiDocument(self)


   .. py:method:: _openOpenApiQna(self)


   .. py:method:: _openGithub(self)


   .. py:method:: _openReadTheDocs(self)


   .. py:method:: _emitShouldRestart(self)


   .. py:method:: _closeClient(self)


   .. py:method:: _closeServerProcess(self)


   .. py:method:: _close(self)


   .. py:method:: close(self)


   .. py:method:: __del__(self)


   .. py:method:: __enter__(self)


   .. py:method:: __exit__(self, exc_type, exc_value, traceback)


   .. py:method:: _execContext(self)


   .. py:method:: _exec(self)


   .. py:method:: _exit(self, return_code=0)


   .. py:method:: _restart(self, code)


   .. py:method:: exec_(self)


   .. py:method:: exit(self, return_code=0)


   .. py:method:: restart(self)


   .. py:method:: execAndExit(self)


   .. py:method:: __getattr__(self, name)


   .. py:method:: main(cls, args=None)
      :classmethod:


   .. py:method:: _onSignal(self, signal, frame)


   .. py:method:: _tryReconnect(self)


   .. py:method:: _onEventConnect(self, errcode)



