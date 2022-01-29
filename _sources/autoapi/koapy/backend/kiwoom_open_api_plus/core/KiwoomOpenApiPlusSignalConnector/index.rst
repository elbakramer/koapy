:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector`
==================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector.KiwoomOpenApiPlusSignalConnector




Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector.P
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector.R


.. py:data:: P
   

   

.. py:data:: R
   

   

.. py:class:: KiwoomOpenApiPlusSignalConnector(name: str)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`, :py:obj:`Generic`\ [\ :py:obj:`P`\ , :py:obj:`R`\ ]

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

   .. py:method:: is_valid_slot(self, slot: Callable[Ellipsis, Any]) -> bool


   .. py:method:: connect_to(self, control: koapy.compat.pyside2.QtAxContainer.QAxWidget)


   .. py:method:: disconnect_from(self, control: koapy.compat.pyside2.QtAxContainer.QAxWidget)


   .. py:method:: connect(self, slot: Callable[Ellipsis, Any])


   .. py:method:: disconnect(self, slot: Optional[Callable[Ellipsis, Any]] = None)


   .. py:method:: call(self, *args: P, **kwargs: P) -> R



