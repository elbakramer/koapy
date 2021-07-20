:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater`
==============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater.KiwoomOpenApiPlusVersionUpdater




.. class:: KiwoomOpenApiPlusVersionUpdater(credential)


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: disable_autologin_impl(cls)
      :classmethod:


   .. method:: disable_autologin(self)


   .. method:: open_login_window_impl(cls)
      :classmethod:


   .. method:: open_login_window(self)


   .. method:: show_account_window_impl(cls)
      :classmethod:


   .. method:: show_account_window(self)


   .. method:: enable_autologin_using_pywinauto(cls, account_passwords)
      :classmethod:


   .. method:: login_using_pywinauto(cls, credential)
      :classmethod:


   .. method:: enable_autologin(self)


   .. method:: try_version_update_using_pywinauto(self)


   .. method:: update_version_if_necessary(self)



