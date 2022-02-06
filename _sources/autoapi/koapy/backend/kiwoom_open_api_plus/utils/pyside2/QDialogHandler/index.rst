:py:mod:`koapy.backend.kiwoom_open_api_plus.utils.pyside2.QDialogHandler`
=========================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.pyside2.QDialogHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.pyside2.QDialogHandler.QDialogHandler




.. py:class:: QDialogHandler(specifications: Optional[Sequence[koapy.compat.pywinauto.WindowSpecification]] = None, parent: Optional[koapy.compat.pyside2.QtCore.QObject] = None)

   Bases: :py:obj:`koapy.utils.logging.pyside2.QThreadLogging.QThreadLogging`

   .. py:attribute:: readyDialog
      

      

   .. py:attribute:: notReadyDialog
      

      

   .. py:method:: from_titles(cls, titles: Sequence[str], allow_magic_lookup: bool = False)
      :classmethod:


   .. py:method:: get_text_of_dialog(self, dialog: koapy.compat.pywinauto.WindowSpecification, default: Optional[str] = None)


   .. py:method:: run(self)


   .. py:method:: stop(self)


   .. py:method:: wait_for_termination(self, timeout=None)



