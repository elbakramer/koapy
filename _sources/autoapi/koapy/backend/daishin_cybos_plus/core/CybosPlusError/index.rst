:py:mod:`koapy.backend.daishin_cybos_plus.core.CybosPlusError`
==============================================================

.. py:module:: koapy.backend.daishin_cybos_plus.core.CybosPlusError


Module Contents
---------------

.. py:exception:: CybosPlusError

   Bases: :py:obj:`Exception`

   Common base class for all non-exit exceptions.


.. py:exception:: CybosPlusRequestError(code, message=None)

   Bases: :py:obj:`CybosPlusError`

   아래 문서에서 [BlockRequest/Blockrequest2/Request의 리턴값] 내용 참조
   http://cybosplus.github.io/cputil_rtf_1_/cybosplus_interface.htm

   .. py:attribute:: ERROR_MESSAGE_BY_CODE
      

      

   .. py:method:: get_error_message_by_code(cls, code, default=None)
      :classmethod:


   .. py:method:: check_code_or_raise(cls, code)
      :classmethod:


   .. py:method:: wrap_to_check_code_or_raise(cls, func)
      :classmethod:


   .. py:method:: try_or_raise(cls, arg)
      :classmethod:


   .. py:method:: code(self)
      :property:


   .. py:method:: message(self)
      :property:



