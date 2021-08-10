:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerFunctions`
========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerFunctions


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerFunctions.KiwoomOpenApiPlusEventHandlerFunctions




.. py:class:: KiwoomOpenApiPlusEventHandlerFunctions

   .. py:method:: OnEventConnect(self, errcode)
      :abstractmethod:


   .. py:method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)
      :abstractmethod:


   .. py:method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)
      :abstractmethod:


   .. py:method:: OnReceiveRealData(self, code, realtype, realdata)
      :abstractmethod:


   .. py:method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)
      :abstractmethod:


   .. py:method:: OnReceiveConditionVer(self, ret, msg)
      :abstractmethod:


   .. py:method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)
      :abstractmethod:


   .. py:method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)
      :abstractmethod:



