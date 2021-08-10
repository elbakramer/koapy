:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager`
================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager.KiwoomOpenApiPlusScreenManager




.. py:class:: KiwoomOpenApiPlusScreenManager(control=None)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:attribute:: _maximum_num
      :annotation: = 200

      

   .. py:method:: _number_to_screen_no(number)
      :staticmethod:


   .. py:method:: _screen_no_to_number(screen_no)
      :staticmethod:


   .. py:method:: is_inuse(self, screen_no)


   .. py:method:: get_single_free_screen(self, exclude=None)


   .. py:method:: get_multiple_free_screens(self, count)


   .. py:method:: get_free_screen(self, count=None)


   .. py:method:: borrow_screen(self, screen_no=None, reuse=True, pop=True)


   .. py:method:: return_screen(self, screen_no)



