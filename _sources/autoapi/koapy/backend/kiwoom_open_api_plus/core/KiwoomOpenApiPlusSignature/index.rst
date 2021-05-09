:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature`
=========================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.KiwoomOpenApiPlusSignature
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.KiwoomOpenApiPlusDispatchSignature
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.KiwoomOpenApiPlusEventHandlerSignature



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.BuildOleItems
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.LoadDispatchSignatures
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.LoadEventHandlerSignatures



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.DISPATCH_SIGNATURES_BY_NAME
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.EVENT_HANDLER_SIGNATURES_BY_NAME


.. function:: BuildOleItems(clsid)


.. class:: KiwoomOpenApiPlusSignature(name, parameters=None, return_annotation=Signature.empty, entry=None)


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

   .. attribute:: MODULE_CLSID
      :annotation: = {6D8C2B4D-EF41-4750-8AD4-C299033833FB}

      

   .. attribute:: OLE_ITEMS
      

      

   .. attribute:: DISPATCH_CLSID
      :annotation: = {CF20FBB6-EDD4-4BE5-A473-FEF91977DEB6}

      

   .. attribute:: EVENT_CLSID
      :annotation: = {7335F12D-8973-4BD5-B7F0-12DF03D175B7}

      

   .. attribute:: PYTHONTYPE_TO_QTTYPE
      

      

   .. attribute:: COMTYPE_TO_PYTHONTYPE
      

      

   .. method:: name(self)
      :property:


   .. method:: _pythontype_to_qttype(cls, typ)
      :classmethod:


   .. method:: to_pyside2_function_prototype(self)


   .. method:: to_pyside2_event_signal(self)


   .. method:: _comtype_to_pythontype(cls, typ)
      :classmethod:


   .. method:: _from_entry(cls, name, entry)
      :classmethod:



.. class:: KiwoomOpenApiPlusDispatchSignature(name, parameters=None, return_annotation=Signature.empty, entry=None)


   Bases: :py:obj:`KiwoomOpenApiPlusSignature`

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

   .. attribute:: DISPATCH_SIGNATURES_BY_NAME
      

      

   .. method:: from_name(cls, name)
      :classmethod:


   .. method:: names(cls)
      :classmethod:



.. function:: LoadDispatchSignatures(oleItems, clsId)


.. data:: DISPATCH_SIGNATURES_BY_NAME
   

   

.. class:: KiwoomOpenApiPlusEventHandlerSignature(name, parameters=None, return_annotation=Signature.empty, entry=None)


   Bases: :py:obj:`KiwoomOpenApiPlusSignature`

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

   .. attribute:: EVENT_HANDLER_SIGNATURES_BY_NAME
      

      

   .. method:: from_name(cls, name)
      :classmethod:


   .. method:: names(cls)
      :classmethod:



.. function:: LoadEventHandlerSignatures(oleItems, clsId)


.. data:: EVENT_HANDLER_SIGNATURES_BY_NAME
   

   

