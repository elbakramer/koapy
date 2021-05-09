:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidget`
===================================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidget


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidget.QWidgetWithLoggingMeta
   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidget.KiwoomOpenApiWQAxWidget




.. class:: QWidgetWithLoggingMeta(cls, clsname, bases, dct)


   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`type`\ (\ :py:obj:`QWidget`\ )


.. class:: KiwoomOpenApiWQAxWidget(*args, **kwargs)


   Bases: :py:obj:`koapy.compat.pyside2.QtWidgets.QWidget`, :py:obj:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidgetMixin.KiwoomOpenApiWQAxWidgetMixin`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: CLSID
      :annotation: = {D1ACAB7D-A3AF-49E4-9004-C9E98344E17A}

      

   .. attribute:: METHOD_NAMES
      

      

   .. attribute:: EVENT_NAMES
      

      

   .. method:: _onException(self, code, source, desc, help)


   .. method:: __getattr__(self, name)


   .. method:: changeEvent(self, event)


   .. method:: closeEvent(self, event)



