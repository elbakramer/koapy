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




.. py:class:: KiwoomOpenApiPlusDynamicCallableRunnable(future: concurrent.futures.Future, fn: Callable[Ellipsis, Any], args: Union[Tuple[Any], List[Any]])

   .. py:method:: run(self)


   .. py:method:: cancel(self)



.. py:class:: KiwoomOpenApiPlusDynamicCallable(control, name, parent=None)

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QObject`

   .. py:attribute:: readyRunnable
      

      

   .. py:method:: bind_dynamic_call_args(self, *args, **kwargs)


   .. py:method:: is_valid_return_type(self, result)


   .. py:method:: check_return_value(self, result)


   .. py:method:: dynamic_call(self, args)


   .. py:method:: dynamic_call_and_check(self, args)


   .. py:method:: call(self, *args, **kwargs)


   .. py:method:: async_call(self, *args, **kwargs)


   .. py:method:: onReadyRunnable(self, runnable)


   .. py:method:: __call__(self, *args, **kwargs)



