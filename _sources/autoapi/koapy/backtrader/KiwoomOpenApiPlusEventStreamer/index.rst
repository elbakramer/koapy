:py:mod:`koapy.backtrader.KiwoomOpenApiPlusEventStreamer`
=========================================================

.. py:module:: koapy.backtrader.KiwoomOpenApiPlusEventStreamer


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KiwoomOpenApiPlusEventStreamer.KiwoomOpenApiPlusPriceEventChannel
   koapy.backtrader.KiwoomOpenApiPlusEventStreamer.KiwoomOpenApiPlusOrderEventChannel
   koapy.backtrader.KiwoomOpenApiPlusEventStreamer.MetaKiwoomOpenApiPlusEventStreamer
   koapy.backtrader.KiwoomOpenApiPlusEventStreamer.KiwoomOpenApiPlusEventStreamer




.. py:class:: KiwoomOpenApiPlusPriceEventChannel(stub)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: close(self)


   .. py:method:: initialize(self)


   .. py:method:: register_code(self, code)


   .. py:method:: is_for_code(self, response, code)


   .. py:method:: filter_for_code(self, code)


   .. py:method:: is_valid_price_event(self, response)


   .. py:method:: filter_price_event(self)


   .. py:method:: time_to_timestamp(self, fid20)


   .. py:method:: event_to_dict(self, response)


   .. py:method:: convert_to_dict(self)


   .. py:method:: get_observable_for_code(self, code)



.. py:class:: KiwoomOpenApiPlusOrderEventChannel(stub)

   .. py:method:: close(self)


   .. py:method:: is_chejan_response(self, response)


   .. py:method:: filter_chejan_response(self)


   .. py:method:: event_to_dict(self, response)


   .. py:method:: convert_to_dict(self)


   .. py:method:: get_observable(self)



.. py:class:: MetaKiwoomOpenApiPlusEventStreamer(cls, clsname, bases, dct)

   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`type`\ (\ :py:obj:`Observer`\ )

   Metaclass for defining Abstract Base Classes (ABCs).

   Use this metaclass to create an ABC.  An ABC can be subclassed
   directly, and then acts as a mix-in class.  You can also register
   unrelated concrete classes (even built-in classes) and unrelated
   ABCs as 'virtual subclasses' -- these and their descendants will
   be considered subclasses of the registering ABC by the built-in
   issubclass() function, but the registering ABC won't show up in
   their MRO (Method Resolution Order) nor will method
   implementations defined by the registering ABC be callable (not
   even via super()).


.. py:class:: KiwoomOpenApiPlusEventStreamer(stub, queue)

   Bases: :py:obj:`rx.core.typing.Observer`, :py:obj:`koapy.utils.logging.Logging.Logging`

   Observer abstract base class

   An Observer is the entity that receives all emissions of a subscribed
   Observable.

   .. py:method:: on_next(self, value)

      Notifies the observer of a new element in the sequence.

      :param value: The received element.


   .. py:method:: on_error(self, error)

      Notifies the observer that an exception has occurred.

      :param error: The error that has occurred.


   .. py:method:: on_completed(self)

      Notifies the observer of the end of the sequence.


   .. py:method:: rates(self, code)


   .. py:method:: events(self)



