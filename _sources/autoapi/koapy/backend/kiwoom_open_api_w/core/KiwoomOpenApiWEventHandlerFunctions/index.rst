:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandlerFunctions`
===============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandlerFunctions


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandlerFunctions.KiwoomOpenApiWEventHandlerFunctions




.. class:: KiwoomOpenApiWEventHandlerFunctions

   .. method:: OnEventConnect(self, errcode)
      :abstractmethod:


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)
      :abstractmethod:


   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext)
      :abstractmethod:


   .. method:: OnReceiveRealData(self, code, realtype, realdata)
      :abstractmethod:


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)
      :abstractmethod:



