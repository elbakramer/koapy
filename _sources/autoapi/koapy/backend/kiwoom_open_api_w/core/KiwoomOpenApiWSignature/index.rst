:py:mod:`koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature`
======================================================================

.. py:module:: koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature.KiwoomOpenApiWSignature
   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature.KiwoomOpenApiWDispatchSignature
   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature.KiwoomOpenApiWEventHandlerSignature



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature.BuildOleItems
   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature.LoadDispatchSignatures
   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature.LoadEventHandlerSignatures



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature.DISPATCH_SIGNATURES_BY_NAME
   koapy.backend.kiwoom_open_api_w.core.KiwoomOpenApiWSignature.EVENT_HANDLER_SIGNATURES_BY_NAME


.. py:function:: BuildOleItems(clsid)


.. py:class:: KiwoomOpenApiWSignature(name, parameters=None, return_annotation=Signature.empty, entry=None)

   Bases: :py:obj:`inspect.Signature`

   A Signature object represents the overall signature of a function.
   It stores a Parameter object for each parameter accepted by the
   function, as well as information specific to the function itself.

   A Signature object has the following public attributes and methods:

   * parameters : OrderedDict
       An ordered mapping of parameters' names to the corresponding
       Parameter objects (keyword-only arguments are in the same order
       as listed in `code.co_varnames`).
   * return_annotation : object
       The annotation for the return type of the function if specified.
       If the function has no annotation for its return type, this
       attribute is set to `Signature.empty`.
   * bind(*args, **kwargs) -> BoundArguments
       Creates a mapping from positional and keyword arguments to
       parameters.
   * bind_partial(*args, **kwargs) -> BoundArguments
       Creates a partial mapping from positional and keyword arguments
       to parameters (simulating 'functools.partial' behavior.)

   .. py:attribute:: MODULE_CLSID
      :annotation: = {1F8A15ED-A979-488F-9694-1EDA98188FFC}

      

   .. py:attribute:: OLE_ITEMS
      

      

   .. py:attribute:: DISPATCH_CLSID
      :annotation: = {85B07632-4F84-4CEF-991D-C79DE781363D}

      

   .. py:attribute:: EVENT_CLSID
      :annotation: = {952B31F8-06FD-4D5A-A021-5FF57F5030AE}

      

   .. py:attribute:: PYTHONTYPE_TO_QTTYPE
      

      

   .. py:attribute:: COMTYPE_TO_PYTHONTYPE
      

      

   .. py:method:: name(self)
      :property:


   .. py:method:: to_pyside2_function_prototype(self)


   .. py:method:: to_pyside2_event_signal(self)



.. py:class:: KiwoomOpenApiWDispatchSignature(name, parameters=None, return_annotation=Signature.empty, entry=None)

   Bases: :py:obj:`KiwoomOpenApiWSignature`

   A Signature object represents the overall signature of a function.
   It stores a Parameter object for each parameter accepted by the
   function, as well as information specific to the function itself.

   A Signature object has the following public attributes and methods:

   * parameters : OrderedDict
       An ordered mapping of parameters' names to the corresponding
       Parameter objects (keyword-only arguments are in the same order
       as listed in `code.co_varnames`).
   * return_annotation : object
       The annotation for the return type of the function if specified.
       If the function has no annotation for its return type, this
       attribute is set to `Signature.empty`.
   * bind(*args, **kwargs) -> BoundArguments
       Creates a mapping from positional and keyword arguments to
       parameters.
   * bind_partial(*args, **kwargs) -> BoundArguments
       Creates a partial mapping from positional and keyword arguments
       to parameters (simulating 'functools.partial' behavior.)

   .. py:attribute:: DISPATCH_SIGNATURES_BY_NAME
      

      

   .. py:method:: from_name(cls, name)
      :classmethod:


   .. py:method:: names(cls)
      :classmethod:



.. py:function:: LoadDispatchSignatures(oleItems, clsId)


.. py:data:: DISPATCH_SIGNATURES_BY_NAME
   

   

.. py:class:: KiwoomOpenApiWEventHandlerSignature(name, parameters=None, return_annotation=Signature.empty, entry=None)

   Bases: :py:obj:`KiwoomOpenApiWSignature`

   A Signature object represents the overall signature of a function.
   It stores a Parameter object for each parameter accepted by the
   function, as well as information specific to the function itself.

   A Signature object has the following public attributes and methods:

   * parameters : OrderedDict
       An ordered mapping of parameters' names to the corresponding
       Parameter objects (keyword-only arguments are in the same order
       as listed in `code.co_varnames`).
   * return_annotation : object
       The annotation for the return type of the function if specified.
       If the function has no annotation for its return type, this
       attribute is set to `Signature.empty`.
   * bind(*args, **kwargs) -> BoundArguments
       Creates a mapping from positional and keyword arguments to
       parameters.
   * bind_partial(*args, **kwargs) -> BoundArguments
       Creates a partial mapping from positional and keyword arguments
       to parameters (simulating 'functools.partial' behavior.)

   .. py:attribute:: EVENT_HANDLER_SIGNATURES_BY_NAME
      

      

   .. py:method:: from_name(cls, name)
      :classmethod:


   .. py:method:: names(cls)
      :classmethod:



.. py:function:: LoadEventHandlerSignatures(oleItems, clsId)


.. py:data:: EVENT_HANDLER_SIGNATURES_BY_NAME
   

   

