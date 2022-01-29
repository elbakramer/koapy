:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager`
================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusScreenManager.KiwoomOpenApiPlusScreenManager




.. py:class:: KiwoomOpenApiPlusScreenManager(control: Optional[koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDispatchFunctions.KiwoomOpenApiPlusDispatchFunctions] = None)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:attribute:: MAXIMUM_NUMBER_OF_SCREENS
      :annotation: = 200

      

   .. py:method:: number_to_screen_no(number: int) -> str
      :staticmethod:


   .. py:method:: screen_no_to_number(screen_no: str) -> int
      :staticmethod:


   .. py:method:: is_inuse(self, screen_no: str) -> bool


   .. py:method:: get_single_free_screen(self, exclude: Optional[Collection[str]] = None) -> str


   .. py:method:: get_multiple_free_screens(self, count: int) -> List[str]


   .. py:method:: get_free_screen(self, count: Optional[int] = None) -> Union[str, List[str]]


   .. py:method:: borrow_screen(self, screen_no: Optional[str] = None, reuse: bool = True, pop: bool = True) -> str


   .. py:method:: return_screen(self, screen_no: str) -> bool



