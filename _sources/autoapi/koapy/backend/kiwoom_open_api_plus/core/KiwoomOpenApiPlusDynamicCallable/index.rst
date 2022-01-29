:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDynamicCallable`
==================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDynamicCallable


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDynamicCallable.KiwoomOpenApiPlusDynamicCallableRunnable
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDynamicCallable.KiwoomOpenApiPlusDynamicCallable




Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDynamicCallable.P
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusDynamicCallable.R


.. py:data:: P
   

   

.. py:data:: R
   

   

.. py:class:: KiwoomOpenApiPlusDynamicCallableRunnable(future: concurrent.futures.Future, fn: Callable[Ellipsis, Any], args: Sequence[Any])

   .. py:method:: run(self)


   .. py:method:: cancel(self)



.. py:class:: KiwoomOpenApiPlusDynamicCallable(control: koapy.compat.pyside2.QtAxContainer.QAxWidget, name: str, parent: Optional[koapy.compat.pyside2.QtCore.QObject] = None)

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QObject`, :py:obj:`Generic`\ [\ :py:obj:`P`\ , :py:obj:`R`\ ]

   Abstract base class for generic types.

   A generic type is typically declared by inheriting from
   this class parameterized with one or more type variables.
   For example, a generic mapping type might be defined as::

     class Mapping(Generic[KT, VT]):
         def __getitem__(self, key: KT) -> VT:
             ...
         # Etc.

   This class can then be used as follows::

     def lookup_name(mapping: Mapping[KT, VT], key: KT, default: VT) -> VT:
         try:
             return mapping[key]
         except KeyError:
             return default

   .. py:attribute:: ready_runnable
      

      

   .. py:method:: bind_dynamic_call_args(self, *args, **kwargs) -> List[Any]


   .. py:method:: is_valid_return_type(self, result: Any) -> bool


   .. py:method:: check_return_value(self, result: Any)


   .. py:method:: dynamic_call(self, args: Sequence[Any]) -> R


   .. py:method:: dynamic_call_and_check(self, args: Sequence[Any]) -> R


   .. py:method:: call(self, *args: P, **kwargs: P) -> R


   .. py:method:: async_call(self, *args: P, **kwargs: P) -> concurrent.futures.Future


   .. py:method:: on_ready_runnable(self, runnable: KiwoomOpenApiPlusDynamicCallableRunnable)



