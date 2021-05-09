:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType`
========================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType.KiwoomOpenApiPlusRealType



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType.main



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType.__outer_class__


.. class:: KiwoomOpenApiPlusRealType(gidc=None, desc=None, nfid=None, fids=None)


   Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

   .. class:: Fid(fid=None, name=None)


      Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

      .. attribute:: __outer_class__
         

         

      .. attribute:: _FID_DUMP_FILENAME
         :annotation: = fid.xlsx

         

      .. attribute:: _NAME_BY_FID
         

         

      .. method:: __repr__(self)

         Return repr(self).


      .. method:: name_by_fid_from_dump_file(cls, dump_file=None)
         :classmethod:


      .. method:: load_from_dump_file(cls, dump_file=None)
         :classmethod:


      .. method:: get_name_by_fid(cls, fid, default=None)
         :classmethod:



   .. attribute:: _REALTYPE_BY_DESC_DUMP_FILENAME
      :annotation: = realtype_by_desc.json

      

   .. attribute:: _REALTYPE_BY_DESC
      

      

   .. method:: __repr__(self)

      Return repr(self).


   .. method:: get_realtype_info_by_realtype_name(cls, realtype)
      :classmethod:


   .. method:: get_fids_by_realtype_name(cls, realtype)
      :classmethod:


   .. method:: get_fids_by_realtype_name_as_string(cls, realtype)
      :classmethod:


   .. method:: get_field_names_by_realtype_name(cls, realtype)
      :classmethod:


   .. method:: realtypes_from_datfile(cls, dat_file=None, encoding=None, module_path=None)
      :classmethod:


   .. method:: realtype_by_desc_from_datfile(cls, dat_file=None)
      :classmethod:


   .. method:: dump_realtype_by_desc(cls, dump_file=None, dat_file=None)
      :classmethod:


   .. method:: realtype_by_desc_from_dump_file(cls, dump_file=None)
      :classmethod:


   .. method:: load_from_dump_file(cls, dump_file=None)
      :classmethod:



.. data:: __outer_class__
   

   

.. function:: main()


