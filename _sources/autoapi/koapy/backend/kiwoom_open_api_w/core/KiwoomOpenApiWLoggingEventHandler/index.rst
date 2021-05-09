:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWLoggingEventHandler`
=============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWLoggingEventHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWLoggingEventHandler.KiwoomOpenApiWLoggingEventHandler




.. class:: KiwoomOpenApiWLoggingEventHandler(control)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandler.KiwoomOpenApiWEventHandler`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext)


   .. method:: OnReceiveRealData(self, code, realtype, realdata)


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)


   .. method:: OnEventConnect(self, errcode)



