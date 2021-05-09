:mod:`koapy.backtrader.KiwoomOpenApiPlusEventStreamer`
======================================================

.. py:module:: koapy.backtrader.KiwoomOpenApiPlusEventStreamer


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KiwoomOpenApiPlusEventStreamer.KiwoomOpenApiPlusPriceEventChannel
   koapy.backtrader.KiwoomOpenApiPlusEventStreamer.KiwoomOpenApiPlusOrderEventChannel
   koapy.backtrader.KiwoomOpenApiPlusEventStreamer.KiwoomOpenApiPlusEventStreamer




.. class:: KiwoomOpenApiPlusPriceEventChannel(stub)


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: _krx_timezone
      

      

   .. method:: close(self)


   .. method:: __del__(self)


   .. method:: initialize(self)


   .. method:: register_code(self, code)


   .. method:: is_for_code(self, response, code)


   .. method:: filter_for_code(self, code)


   .. method:: is_valid_price_event(self, response)


   .. method:: filter_price_event(self)


   .. method:: time_to_timestamp(self, fid20)


   .. method:: event_to_dict(self, response)


   .. method:: convert_to_dict(self)


   .. method:: get_observable_for_code(self, code)



.. class:: KiwoomOpenApiPlusOrderEventChannel(stub)


   .. method:: close(self)


   .. method:: __del__(self)


   .. method:: is_chejan_response(self, response)


   .. method:: filter_chejan_response(self)


   .. method:: event_to_dict(self, response)


   .. method:: convert_to_dict(self)


   .. method:: get_observable(self)



.. class:: KiwoomOpenApiPlusEventStreamer(stub, queue)


   Bases: :py:obj:`rx.core.typing.Observer`, :py:obj:`koapy.utils.logging.Logging.Logging`

   Observer abstract base class

   An Observer is the entity that receives all emissions of a subscribed
   Observable.

   .. attribute:: _price_event_channels_by_stub
      

      

   .. attribute:: _order_event_channels_by_stub
      

      

   .. attribute:: _lock
      

      

   .. method:: on_next(self, value)

      Notifies the observer of a new element in the sequence.

      :param value: The received element.


   .. method:: on_error(self, error)

      Notifies the observer that an exception has occurred.

      :param error: The error that has occurred.


   .. method:: on_completed(self)

      Notifies the observer of the end of the sequence.


   .. method:: rates(self, code)


   .. method:: events(self)



