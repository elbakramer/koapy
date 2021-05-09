:mod:`koapy.backtrader.KiwoomOpenApiPlusStore`
==============================================

.. py:module:: koapy.backtrader.KiwoomOpenApiPlusStore


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KiwoomOpenApiPlusStore.HistoricalPriceRecord
   koapy.backtrader.KiwoomOpenApiPlusStore.API
   koapy.backtrader.KiwoomOpenApiPlusStore.MetaSingleton
   koapy.backtrader.KiwoomOpenApiPlusStore.MetaKiwoomOpenApiPlusStore
   koapy.backtrader.KiwoomOpenApiPlusStore.KiwoomOpenApiPlusStore




.. exception:: KiwoomOpenApiPlusJsonError(code, message=None)


   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError.KiwoomOpenApiPlusNegativeReturnCodeError`

   Common base class for all non-exit exceptions.

   .. method:: error_response(self, description=None)



.. exception:: KiwoomOpenApiPlusTimeFrameError


   Bases: :py:obj:`KiwoomOpenApiPlusJsonError`

   Common base class for all non-exit exceptions.


.. class:: HistoricalPriceRecord


   Bases: :py:obj:`collections.namedtuple`\ (\ :py:obj:`'HistoricalPriceRecord'`\ , [\ :py:obj:`'time'`\ , :py:obj:`'open'`\ , :py:obj:`'high'`\ , :py:obj:`'low'`\ , :py:obj:`'close'`\ , :py:obj:`'volume'`\ ]\ )

   docstring

   .. attribute:: __slots__
      :annotation: = []

      

   .. attribute:: _krx_timezone
      

      

   .. method:: from_tuple(cls, tup)
      :classmethod:


   .. method:: records_from_dataframe(cls, df)
      :classmethod:


   .. method:: dict_records_from_dataframe(cls, df)
      :classmethod:



.. class:: API(context)


   .. attribute:: _krx_timezone
      

      

   .. method:: __getattr__(self, name)


   .. method:: get_instruments_original(self, account, instruments)


   .. method:: get_instruments(self, account, instruments)


   .. method:: get_history(self, trcode, inputs, dtbegin=None, dtend=None)


   .. method:: get_positions(self, account)


   .. method:: get_account(self, account)


   .. method:: create_order(self, account, **kwargs)


   .. method:: close_order(self, account, oid, size, dataname)


   .. method:: get_today_quotes_by_code(self, codes=None)



.. class:: MetaSingleton(cls, clsname, bases, dct)


   Bases: :py:obj:`backtrader.metabase.MetaParams`

   .. method:: __call__(cls, *args, **kwargs)



.. class:: MetaKiwoomOpenApiPlusStore(cls, clsname, bases, dct)


   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`MetaSingleton`


.. class:: KiwoomOpenApiPlusStore(context=None)


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: BrokerCls
      

      

   .. attribute:: DataCls
      

      

   .. attribute:: params
      :annotation: = [['account', ''], ['account_tmout', 60.0]]

      

   .. attribute:: _DTEPOCH
      

      

   .. attribute:: _GRANULARITIES
      

      

   .. attribute:: _ORDEREXECS
      

      

   .. attribute:: _OIDSINGLE
      :annotation: = ['orderOpened', 'tradeOpened', 'tradeReduced']

      

   .. attribute:: _OIDMULTIPLE
      :annotation: = ['tradesClosed']

      

   .. attribute:: _X_ORDER_CREATE
      :annotation: = ['STOP_ORDER_CREATE', 'LIMIT_ORDER_CREATE', 'MARKET_IF_TOUCHED_ORDER_CREATE']

      

   .. attribute:: _X_ORDER_FILLED
      :annotation: = ['MARKET_ORDER_CREATE', 'ORDER_FILLED', 'TAKE_PROFIT_FILLED', 'STOP_LOSS_FILLED', 'TRAILING_STOP_FILLED']

      

   .. method:: getdata(cls, *args, **kwargs)
      :classmethod:


   .. method:: getbroker(cls, *args, **kwargs)
      :classmethod:


   .. method:: start(self, data=None, broker=None)


   .. method:: initial_today_historical_msg(self, data=None)


   .. method:: stop(self)


   .. method:: put_notification(self, msg, *args, **kwargs)


   .. method:: get_notifications(self)


   .. method:: timeoffset(self)


   .. method:: get_granularity(self, timeframe, compression, default=None)


   .. method:: get_instrument(self, dataname)


   .. method:: streaming_events(self, tmout=None)


   .. method:: _t_streaming_listener(self, q, tmout=None)


   .. method:: _t_streaming_events(self, q, tmout=None)


   .. method:: candles(self, dataname, dtbegin, dtend, timeframe, compression)


   .. method:: _t_candles(self, dataname, dtbegin, dtend, timeframe, compression, q)


   .. method:: streaming_prices(self, dataname, tmout=None)


   .. method:: _t_streaming_prices(self, dataname, q, tmout)


   .. method:: get_cash(self)


   .. method:: get_value(self)


   .. method:: get_positions(self)


   .. method:: broker_threads(self)


   .. method:: _t_account(self)


   .. method:: order_create(self, order, stopside=None, takeside=None, **kwargs)


   .. method:: _t_order_create(self)


   .. method:: order_cancel(self, order)


   .. method:: _t_order_cancel(self)


   .. method:: _transaction(self, trans)


   .. method:: _process_transaction(self, oid, trans)



