:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget`
=========================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget.QWidgetWithLoggingMeta
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidget.KiwoomOpenApiPlusQAxWidget




.. class:: QWidgetWithLoggingMeta(cls, clsname, bases, dct)


   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`type`\ (\ :py:obj:`QWidget`\ )


.. class:: KiwoomOpenApiPlusQAxWidget(*args, **kwargs)


   Bases: :py:obj:`koapy.compat.pyside2.QtWidgets.QWidget`, :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusQAxWidgetMixin.KiwoomOpenApiPlusQAxWidgetMixin`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: CLSID
      :annotation: = {A1574A0D-6BFA-4BD7-9020-DED88711818D}

      

   .. attribute:: PROGID
      :annotation: = KHOPENAPI.KHOpenApiCtrl.1

      

   .. attribute:: METHOD_NAMES
      

      

   .. attribute:: EVENT_NAMES
      

      

   .. method:: _onException(self, code, source, desc, help)


   .. method:: __getattr__(self, name)


   .. method:: changeEvent(self, event)


   .. method:: closeEvent(self, event)



