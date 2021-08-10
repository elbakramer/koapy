:py:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWLoggingEventHandler`
================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWLoggingEventHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWLoggingEventHandler.KiwoomOpenApiWLoggingEventHandler




.. py:class:: KiwoomOpenApiWLoggingEventHandler(control)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandler.KiwoomOpenApiWEventHandler`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext)


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. py:method:: OnEventConnect(self, errcode)



