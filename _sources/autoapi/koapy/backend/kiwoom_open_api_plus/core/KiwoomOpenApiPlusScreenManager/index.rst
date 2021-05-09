:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager`
=============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager.KiwoomOpenApiPlusScreenManager




.. class:: KiwoomOpenApiPlusScreenManager(control=None)


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: _maximum_num
      :annotation: = 200

      

   .. method:: _number_to_screen_no(number)
      :staticmethod:


   .. method:: _screen_no_to_number(screen_no)
      :staticmethod:


   .. method:: is_inuse(self, screen_no)


   .. method:: get_single_free_screen(self, exclude=None)


   .. method:: get_multiple_free_screens(self, count)


   .. method:: get_free_screen(self, count=None)


   .. method:: borrow_screen(self, screen_no=None, reuse=True, pop=True)


   .. method:: return_screen(self, screen_no)



