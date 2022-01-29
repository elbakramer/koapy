:py:mod:`koapy.utils.pywin32`
=============================

.. py:module:: koapy.utils.pywin32


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.pywin32.GetTypelibSpecs
   koapy.utils.pywin32.GetTypelibSpec
   koapy.utils.pywin32.LoadTypeLib
   koapy.utils.pywin32.BuildOleItems
   koapy.utils.pywin32.TryBuildOleItems



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.utils.pywin32.logger
   koapy.utils.pywin32.PyIID
   koapy.utils.pywin32.PyITypeLib


.. py:data:: logger
   

   

.. py:data:: PyIID
   :annotation: = PyIID

   

.. py:data:: PyITypeLib
   :annotation: = PyITypeLib

   

.. py:function:: GetTypelibSpecs(iid: Union[PyIID, str]) -> List[win32com.client.selecttlb.TypelibSpec]


.. py:function:: GetTypelibSpec(iid: Union[PyIID, str]) -> win32com.client.selecttlb.TypelibSpec


.. py:function:: LoadTypeLib(iid: Union[PyIID, str]) -> Tuple[PyITypeLib, win32com.client.selecttlb.TypelibSpec]


.. py:function:: BuildOleItems(iid: Union[PyIID, str]) -> Tuple[Dict[PyIID, win32com.client.genpy.DispatchItem], Dict[PyIID, win32com.client.genpy.EnumerationItem], Dict[PyIID, win32com.client.genpy.RecordItem], Dict[PyIID, win32com.client.genpy.VTableItem]]


.. py:function:: TryBuildOleItems(iid: Union[PyIID, str], error='coerce') -> Tuple[Dict[PyIID, win32com.client.genpy.DispatchItem], Dict[PyIID, win32com.client.genpy.EnumerationItem], Dict[PyIID, win32com.client.genpy.RecordItem], Dict[PyIID, win32com.client.genpy.VTableItem]]


