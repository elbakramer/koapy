:py:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidget`
======================================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidget


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidget.QWidgetWithLoggingMeta
   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidget.KiwoomOpenApiWQAxWidget




.. py:class:: QWidgetWithLoggingMeta(cls, clsname, bases, dct)

   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`type`\ (\ :py:obj:`QWidget`\ )


.. py:class:: KiwoomOpenApiWQAxWidget(*args, **kwargs)

   Bases: :py:obj:`koapy.compat.pyside2.QtWidgets.QWidget`, :py:obj:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWQAxWidgetMixin.KiwoomOpenApiWQAxWidgetMixin`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:attribute:: CLSID
      :annotation: = {D1ACAB7D-A3AF-49E4-9004-C9E98344E17A}

      

   .. py:attribute:: METHOD_NAMES
      

      

   .. py:attribute:: EVENT_NAMES
      

      

   .. py:method:: _onException(self, code, source, desc, help)


   .. py:method:: __getattr__(self, name)


   .. py:method:: changeEvent(self, event)


   .. py:method:: closeEvent(self, event)



