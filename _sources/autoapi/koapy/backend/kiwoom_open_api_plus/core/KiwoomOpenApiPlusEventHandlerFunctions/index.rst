:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerFunctions`
=====================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerFunctions


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerFunctions.KiwoomOpenApiPlusEventHandlerFunctions




.. class:: KiwoomOpenApiPlusEventHandlerFunctions

   .. method:: OnEventConnect(self, errcode)
      :abstractmethod:


   .. method:: OnReceiveMsg(self, scrnno, rqname, trcode, msg)
      :abstractmethod:


   .. method:: OnReceiveTrData(self, scrnno, rqname, trcode, recordname, prevnext, datalength, errorcode, message, splmmsg)
      :abstractmethod:


   .. method:: OnReceiveRealData(self, code, realtype, realdata)
      :abstractmethod:


   .. method:: OnReceiveChejanData(self, gubun, itemcnt, fidlist)
      :abstractmethod:


   .. method:: OnReceiveConditionVer(self, ret, msg)
      :abstractmethod:


   .. method:: OnReceiveTrCondition(self, scrnno, codelist, condition_name, condition_index, prevnext)
      :abstractmethod:


   .. method:: OnReceiveRealCondition(self, code, condition_type, condition_name, condition_index)
      :abstractmethod:



