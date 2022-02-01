:py:mod:`koapy.utils.pywin32`
=============================

.. py:module:: koapy.utils.pywin32


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.pywin32.IsPyIID
   koapy.utils.pywin32.IsPyITypeLib
   koapy.utils.pywin32.IsPyIIDLike
   koapy.utils.pywin32.GetTypelibSpecs
   koapy.utils.pywin32.GetLatestTypelibSpec
   koapy.utils.pywin32.LoadTypeLib
   koapy.utils.pywin32.BuildOleItems



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.utils.pywin32.PyIID
   koapy.utils.pywin32.PyITypeLib
   koapy.utils.pywin32.PyIIDLike


.. py:data:: PyIID
   

   

.. py:data:: PyITypeLib
   :annotation: = PyITypeLib

   

.. py:data:: PyIIDLike
   

   

.. py:function:: IsPyIID(value) -> TypeGuard[PyIID]


.. py:function:: IsPyITypeLib(value) -> TypeGuard[PyITypeLib]


.. py:function:: IsPyIIDLike(value) -> TypeGuard[PyIIDLike]


.. py:function:: GetTypelibSpecs(iid: PyIIDLike) -> List[win32com.client.selecttlb.TypelibSpec]


.. py:function:: GetLatestTypelibSpec(specs: Union[Sequence[win32com.client.selecttlb.TypelibSpec], PyIIDLike]) -> Optional[win32com.client.selecttlb.TypelibSpec]


.. py:function:: LoadTypeLib(spec: Union[win32com.client.selecttlb.TypelibSpec, PyIIDLike]) -> Optional[PyITypeLib]


.. py:function:: BuildOleItems(spec: Union[win32com.client.selecttlb.TypelibSpec, PyIIDLike], tlb: Optional[PyITypeLib] = None) -> Tuple[Dict[PyIID, win32com.client.genpy.DispatchItem], Dict[PyIID, win32com.client.genpy.EnumerationItem], Dict[PyIID, win32com.client.genpy.RecordItem], Dict[PyIID, win32com.client.genpy.VTableItem]]


