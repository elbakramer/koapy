:py:mod:`koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusDialogHandler`
===================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusDialogHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusDialogHandler.DialogToHandle
   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusDialogHandler.KiwoomOpenApiPlusDialogToHandle
   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusDialogHandler.KiwoomOpenApiPlusDialogHandler




.. py:class:: DialogToHandle

   .. py:method:: should_handle(self, dialog: koapy.compat.pywinauto.WindowSpecification) -> bool


   .. py:method:: handle(self, dialog: koapy.compat.pywinauto.WindowSpecification)


   .. py:method:: handle_if_needed(self, dialog: koapy.compat.pywinauto.WindowSpecification)



.. py:class:: KiwoomOpenApiPlusDialogToHandle(title: Optional[str] = None, time: Optional[datetime.time] = None, body: Optional[str] = None, app: Optional[koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusManagerApplication] = None, restart_type: Optional[koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusManagerApplication.RestartType] = None)

   Bases: :py:obj:`DialogToHandle`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: should_handle_by_title(cls, dialog: koapy.compat.pywinauto.WindowSpecification, title: str)
      :classmethod:


   .. py:method:: handle_by_clicking_button(cls, dialog: koapy.compat.pywinauto.WindowSpecification)
      :classmethod:


   .. py:method:: handle_by_emiting_should_restart_signal(cls, app: koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusManagerApplication, restart_type: koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusManagerApplication.RestartType)
      :classmethod:


   .. py:method:: to_specification(self) -> koapy.compat.pywinauto.WindowSpecification


   .. py:method:: should_handle(self, dialog: koapy.compat.pywinauto.WindowSpecification) -> bool


   .. py:method:: handle(self, dialog: koapy.compat.pywinauto.WindowSpecification)


   .. py:method:: handle_if_needed(self, dialog: koapy.compat.pywinauto.WindowSpecification)



.. py:class:: KiwoomOpenApiPlusDialogHandler(app: koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusManagerApplication, parent: Optional[koapy.compat.pyside2.QtCore.QObject] = None)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.utils.pyside2.QDialogHandler.QDialogHandler`

   .. py:method:: onReadyDialog(self, dialog: koapy.compat.pywinauto.WindowSpecification)



