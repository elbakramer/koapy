:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusRealType`
===========================================================================

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


.. py:class:: KiwoomOpenApiPlusRealType(gidc=None, desc=None, nfid=None, fids=None)

   Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:class:: Fid(fid=None, name=None)

      Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

      .. py:attribute:: __outer_class__
         

         

      .. py:attribute:: _FID_DUMP_FILEDIR
         

         

      .. py:attribute:: _FID_DUMP_FILENAME
         :annotation: = fid.xlsx

         

      .. py:attribute:: _FID_DUMP_FILEPATH
         

         

      .. py:attribute:: _NAME_BY_FID
         

         

      .. py:method:: __repr__(self)

         Return repr(self).


      .. py:method:: __eq__(self, other)

         Return self==value.


      .. py:method:: name_by_fid_from_dump_file(cls, dump_file=None)
         :classmethod:


      .. py:method:: load_from_dump_file(cls, dump_file=None)
         :classmethod:


      .. py:method:: get_name_by_fid(cls, fid, default=None)
         :classmethod:



   .. py:attribute:: _REALTYPE_BY_DESC_DUMP_FILEDIR
      

      

   .. py:attribute:: _REALTYPE_BY_DESC_DUMP_FILENAME
      :annotation: = realtype_by_desc.json

      

   .. py:attribute:: _REALTYPE_BY_DESC_DUMP_FILEPATH
      

      

   .. py:attribute:: _REALTYPE_BY_DESC
      

      

   .. py:method:: __repr__(self)

      Return repr(self).


   .. py:method:: __eq__(self, other)

      Return self==value.


   .. py:method:: get_realtype_info_by_realtype_name(cls, realtype)
      :classmethod:


   .. py:method:: get_fids_by_realtype_name(cls, realtype)
      :classmethod:


   .. py:method:: get_fids_by_realtype_name_as_string(cls, realtype)
      :classmethod:


   .. py:method:: get_field_names_by_realtype_name(cls, realtype)
      :classmethod:


   .. py:method:: realtypes_from_datfile(cls, dat_file=None, encoding=None, module_path=None)
      :classmethod:


   .. py:method:: realtype_by_desc_from_datfile(cls, dat_file=None)
      :classmethod:


   .. py:method:: dump_realtype_by_desc(cls, dump_file=None, dat_file=None)
      :classmethod:


   .. py:method:: realtype_by_desc_from_dump_file(cls, dump_file=None)
      :classmethod:


   .. py:method:: load_from_dump_file(cls, dump_file=None)
      :classmethod:


   .. py:method:: load_from_datfile(cls, dat_file=None)
      :classmethod:


   .. py:method:: load(cls)
      :classmethod:



.. py:data:: __outer_class__
   

   

.. py:function:: main()


