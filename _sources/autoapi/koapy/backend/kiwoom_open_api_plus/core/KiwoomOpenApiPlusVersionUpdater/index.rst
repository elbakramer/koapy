:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater`
=================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusVersionUpdater.KiwoomOpenApiPlusVersionUpdater




.. py:class:: KiwoomOpenApiPlusVersionUpdater(credentials)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: get_api_module_path(self)


   .. py:method:: get_autologin_dat(self)


   .. py:method:: is_autologin_enabled(self)


   .. py:method:: disable_autologin(self)


   .. py:method:: open_login_window_impl(cls)
      :classmethod:


   .. py:method:: open_login_window(self)


   .. py:method:: show_account_window_impl(cls)
      :classmethod:


   .. py:method:: show_account_window(self)


   .. py:method:: check_apply_simulation_window(cls)
      :classmethod:


   .. py:method:: login_using_pywinauto(cls, credentials)
      :classmethod:


   .. py:method:: enable_autologin_using_pywinauto(cls, credentials)
      :classmethod:


   .. py:method:: enable_autologin(self)


   .. py:method:: handle_version_upgrade_using_pywinauto(cls, pid)
      :classmethod:


   .. py:method:: try_version_update_using_pywinauto(self)


   .. py:method:: update_version_if_necessary(self)



