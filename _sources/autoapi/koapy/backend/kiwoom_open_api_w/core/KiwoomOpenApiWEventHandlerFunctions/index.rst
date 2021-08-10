:py:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandlerFunctions`
==================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandlerFunctions


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWEventHandlerFunctions.KiwoomOpenApiWEventHandlerFunctions




.. py:class:: KiwoomOpenApiWEventHandlerFunctions

   .. py:method:: OnEventConnect(self, errcode)
      :abstractmethod:


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)
      :abstractmethod:


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext)
      :abstractmethod:


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)
      :abstractmethod:


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)
      :abstractmethod:



