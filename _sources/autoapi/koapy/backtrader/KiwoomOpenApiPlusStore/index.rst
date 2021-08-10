:py:mod:`koapy.backtrader.KiwoomOpenApiPlusStore`
=================================================

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




.. py:exception:: KiwoomOpenApiPlusJsonError(code, message=None)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusError.KiwoomOpenApiPlusNegativeReturnCodeError`

   Common base class for all non-exit exceptions.

   .. py:method:: error_response(self, description=None)



.. py:exception:: KiwoomOpenApiPlusTimeFrameError

   Bases: :py:obj:`KiwoomOpenApiPlusJsonError`

   Common base class for all non-exit exceptions.


.. py:class:: HistoricalPriceRecord

   Bases: :py:obj:`collections.namedtuple`\ (\ :py:obj:`'HistoricalPriceRecord'`\ , [\ :py:obj:`'time'`\ , :py:obj:`'open'`\ , :py:obj:`'high'`\ , :py:obj:`'low'`\ , :py:obj:`'close'`\ , :py:obj:`'volume'`\ ]\ )

   docstring

   .. py:attribute:: __slots__
      :annotation: = []

      

   .. py:attribute:: _krx_timezone
      

      

   .. py:method:: from_tuple(cls, tup)
      :classmethod:


   .. py:method:: records_from_dataframe(cls, df)
      :classmethod:


   .. py:method:: dict_records_from_dataframe(cls, df)
      :classmethod:



.. py:class:: API(context)

   .. py:attribute:: _krx_timezone
      

      

   .. py:method:: __getattr__(self, name)


   .. py:method:: get_instruments_original(self, account, instruments)


   .. py:method:: get_instruments(self, account, instruments)


   .. py:method:: get_history(self, trcode, inputs, dtbegin=None, dtend=None)


   .. py:method:: get_positions(self, account)


   .. py:method:: get_account(self, account)


   .. py:method:: create_order(self, account, **kwargs)


   .. py:method:: close_order(self, account, oid, size, dataname)


   .. py:method:: get_today_quotes_by_code(self, codes=None)



.. py:class:: MetaSingleton(cls, clsname, bases, dct)

   Bases: :py:obj:`backtrader.metabase.MetaParams`

   .. py:method:: __call__(cls, *args, **kwargs)



.. py:class:: MetaKiwoomOpenApiPlusStore(cls, clsname, bases, dct)

   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`MetaSingleton`


.. py:class:: KiwoomOpenApiPlusStore(context=None)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:attribute:: BrokerCls
      

      

   .. py:attribute:: DataCls
      

      

   .. py:attribute:: params
      :annotation: = [['account', ''], ['account_tmout', 60.0]]

      

   .. py:attribute:: _DTEPOCH
      

      

   .. py:attribute:: _GRANULARITIES
      

      

   .. py:attribute:: _ORDEREXECS
      

      

   .. py:attribute:: _OIDSINGLE
      :annotation: = ['orderOpened', 'tradeOpened', 'tradeReduced']

      

   .. py:attribute:: _OIDMULTIPLE
      :annotation: = ['tradesClosed']

      

   .. py:attribute:: _X_ORDER_CREATE
      :annotation: = ['STOP_ORDER_CREATE', 'LIMIT_ORDER_CREATE', 'MARKET_IF_TOUCHED_ORDER_CREATE']

      

   .. py:attribute:: _X_ORDER_FILLED
      :annotation: = ['MARKET_ORDER_CREATE', 'ORDER_FILLED', 'TAKE_PROFIT_FILLED', 'STOP_LOSS_FILLED', 'TRAILING_STOP_FILLED']

      

   .. py:method:: getdata(cls, *args, **kwargs)
      :classmethod:


   .. py:method:: getbroker(cls, *args, **kwargs)
      :classmethod:


   .. py:method:: start(self, data=None, broker=None)


   .. py:method:: initial_today_historical_msg(self, data=None)


   .. py:method:: stop(self)


   .. py:method:: put_notification(self, msg, *args, **kwargs)


   .. py:method:: get_notifications(self)


   .. py:method:: timeoffset(self)


   .. py:method:: get_granularity(self, timeframe, compression, default=None)


   .. py:method:: get_instrument(self, dataname)


   .. py:method:: streaming_events(self, tmout=None)


   .. py:method:: _t_streaming_listener(self, q, tmout=None)


   .. py:method:: _t_streaming_events(self, q, tmout=None)


   .. py:method:: candles(self, dataname, dtbegin, dtend, timeframe, compression)


   .. py:method:: _t_candles(self, dataname, dtbegin, dtend, timeframe, compression, q)


   .. py:method:: streaming_prices(self, dataname, tmout=None)


   .. py:method:: _t_streaming_prices(self, dataname, q, tmout)


   .. py:method:: get_cash(self)


   .. py:method:: get_value(self)


   .. py:method:: get_positions(self)


   .. py:method:: broker_threads(self)


   .. py:method:: _t_account(self)


   .. py:method:: order_create(self, order, stopside=None, takeside=None, **kwargs)


   .. py:method:: _t_order_create(self)


   .. py:method:: order_cancel(self, order)


   .. py:method:: _t_order_cancel(self)


   .. py:method:: _transaction(self, trans)


   .. py:method:: _process_transaction(self, oid, trans)



