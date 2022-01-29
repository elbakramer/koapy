:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerSignature`
========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerSignature


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusEventHandlerSignature.KiwoomOpenApiPlusEventHandlerSignature




.. py:class:: KiwoomOpenApiPlusEventHandlerSignature(name: str, parameters: Dict[str, inspect.Parameter] = None, return_annotation=Signature.empty)

   Bases: :py:obj:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignature.KiwoomOpenApiPlusSignature`

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
      :annotation: :Dict[str, KiwoomOpenApiPlusEventHandlerSignature]

      

   .. py:method:: from_name(cls, name: str) -> KiwoomOpenApiPlusEventHandlerSignature
      :classmethod:


   .. py:method:: names(cls) -> List[str]
      :classmethod:



