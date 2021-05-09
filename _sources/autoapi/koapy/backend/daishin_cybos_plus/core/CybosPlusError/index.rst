:mod:`koapy.backend.daishin_cybos_plus.core.CybosPlusError`
===========================================================

.. py:module:: koapy.backend.daishin_cybos_plus.core.CybosPlusError


Module Contents
---------------

.. exception:: CybosPlusError


   Bases: :py:obj:`Exception`

   Common base class for all non-exit exceptions.


.. exception:: CybosPlusRequestError(code, message=None)


   Bases: :py:obj:`CybosPlusError`

   아래 문서에서 [BlockRequest/Blockrequest2/Request의 리턴값] 내용 참조
   http://cybosplus.github.io/cputil_rtf_1_/cybosplus_interface.htm

   .. attribute:: ERROR_MESSAGE_BY_CODE
      

      

   .. method:: get_error_message_by_code(cls, code, default=None)
      :classmethod:


   .. method:: check_code_or_raise(cls, code)
      :classmethod:


   .. method:: wrap_to_check_code_or_raise(cls, func)
      :classmethod:


   .. method:: try_or_raise(cls, arg)
      :classmethod:


   .. method:: __str__(self)

      Return str(self).


   .. method:: __repr__(self)

      Return repr(self).


   .. method:: code(self)
      :property:


   .. method:: message(self)
      :property:



