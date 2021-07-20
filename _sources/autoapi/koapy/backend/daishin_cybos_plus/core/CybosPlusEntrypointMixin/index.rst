:mod:`koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin`
=====================================================================

.. py:module:: koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin.CybosPlusEntrypointMixin




.. class:: CybosPlusEntrypointMixin

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: GetConnectState(self)


   .. method:: ConnectUsingPywinauto_Impl(cls, credential=None)
      :classmethod:

      https://github.com/ippoeyeslhw/cppy/blob/master/cp_luncher.py


   .. method:: ConnectUsingPywinauto_RunScriptInSubprocess(cls, credential=None)
      :classmethod:


   .. method:: ConnectUsingPywinauto(self, credential=None)


   .. method:: Connect(self, credential=None)


   .. method:: CommConnect(self, credential=None)


   .. method:: EnsureConnected(self, credential=None)


   .. method:: GetCodeListByMarketAsList(self, market)

      0: 구분없음
      1: 거래소
      2: 코스닥
      3: 프리보드
      4: KRX


   .. method:: GetKospiCodeList(self)


   .. method:: GetKosdaqCodeList(self)


   .. method:: GetGeneralCodeList(self, include_preferred_stock=False, include_etn=False, include_etf=False, include_mutual_fund=False, include_reits=False, include_kosdaq=False)


   .. method:: GetStockDataAsDataFrame(self, code, chart_type, interval, start_date=None, end_date=None, adjusted_price=False, adjustement_only=False)

      http://cybosplus.github.io/cpsysdib_rtf_1_/stockchart.htm


   .. method:: GetDailyStockDataAsDataFrame(self, code, start_date=None, end_date=None, adjusted_price=False)


   .. method:: GetMinuteStockDataAsDataFrame(self, code, interval, start_date=None, end_date=None, adjusted_price=False)


   .. method:: GetDailyAdjustmentRatioAsDataFrame(self, code, start_date=None, end_date=None)


   .. method:: GetCurrentStockDataAsDataFrame(self, codes)

      http://cybosplus.github.io/cpdib_rtf_1_/stockmst2.htm



