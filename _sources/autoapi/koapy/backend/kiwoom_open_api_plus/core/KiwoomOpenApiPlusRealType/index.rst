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



.. py:class:: KiwoomOpenApiPlusRealType(gidc: Optional[str] = None, desc: Optional[str] = None, nfid: Optional[int] = None, fids: Optional[List[int]] = None)

   Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:class:: Fid(fid: Optional[int] = None, name: Optional[str] = None)

      Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

      .. py:attribute:: FID_DUMP_FILEDIR
         

         

      .. py:attribute:: FID_DUMP_FILENAME
         :annotation: = fid.csv

         

      .. py:attribute:: FID_DUMP_FILEPATH
         

         

      .. py:attribute:: FID_DUMP_PROCESSOR
         

         

      .. py:attribute:: FID_BY_FID
         :annotation: :Dict[int, KiwoomOpenApiPlusRealType]

         

      .. py:attribute:: FID_BY_NAME
         :annotation: :Dict[str, KiwoomOpenApiPlusRealType]

         

      .. py:method:: fids_from_dump_file(cls, dump_file: Optional[Union[str, os.PathLike]] = None) -> Dict[int, str]
         :classmethod:


      .. py:method:: load_from_dump_file(cls, dump_file: Optional[Union[str, os.PathLike]] = None)
         :classmethod:


      .. py:method:: from_fid(cls, fid: Union[str, int]) -> Optional[KiwoomOpenApiPlusRealType]
         :classmethod:


      .. py:method:: from_name(cls, name: str) -> Optional[KiwoomOpenApiPlusRealType]
         :classmethod:


      .. py:method:: get_name_by_fid(cls, fid: Union[str, int], default: Optional[str] = None) -> Optional[str]
         :classmethod:



   .. py:attribute:: REALTYPE_BY_DESC_DUMP_FILEDIR
      

      

   .. py:attribute:: REALTYPE_BY_DESC_DUMP_FILENAME
      :annotation: = realtype_by_desc.json

      

   .. py:attribute:: REALTYPE_BY_DESC_DUMP_FILEPATH
      

      

   .. py:attribute:: REALTYPE_BY_DESC
      :annotation: :Dict[str, KiwoomOpenApiPlusRealType]

      

   .. py:method:: get_realtype_name_list(cls)
      :classmethod:


   .. py:method:: get_realtype_info_list(cls)
      :classmethod:


   .. py:method:: get_realtype_info_by_desc(cls, desc: str) -> Optional[KiwoomOpenApiPlusRealType]
      :classmethod:


   .. py:method:: get_realtype_info_by_name(cls, name: str) -> Optional[KiwoomOpenApiPlusRealType]
      :classmethod:


   .. py:method:: get_realtype_info_by_realtype_name(cls, name: str) -> Optional[KiwoomOpenApiPlusRealType]
      :classmethod:


   .. py:method:: from_name(cls, name: str) -> Optional[KiwoomOpenApiPlusRealType]
      :classmethod:


   .. py:method:: get_fids_by_realtype_name(cls, name: str) -> Optional[List[int]]
      :classmethod:


   .. py:method:: get_fids_by_realtype_name_as_string(cls, name: str) -> Optional[str]
      :classmethod:


   .. py:method:: get_field_names_by_realtype_name(cls, name: str) -> Optional[List[str]]
      :classmethod:


   .. py:method:: realtypes_from_datfile(cls, dat_file: Optional[Union[str, os.PathLike, BinaryIO]] = None, encoding: Optional[str] = None, module_path: Optional[str] = None) -> List[KiwoomOpenApiPlusRealType]
      :classmethod:


   .. py:method:: realtype_by_desc_from_datfile(cls, dat_file: Optional[Union[str, os.PathLike, BinaryIO]] = None) -> Dict[str, KiwoomOpenApiPlusRealType]
      :classmethod:


   .. py:method:: dump_realtype_by_desc(cls, dump_file: Optional[Union[str, os.PathLike, TextIO]] = None, dat_file: Optional[Union[str, os.PathLike, BinaryIO]] = None, encoding: Optional[str] = None)
      :classmethod:


   .. py:method:: realtype_by_desc_from_dump_file(cls, dump_file: Optional[Union[str, os.PathLike, TextIO]] = None, encoding: Optional[str] = None) -> Dict[str, KiwoomOpenApiPlusRealType]
      :classmethod:


   .. py:method:: load_from_dump_file(cls, dump_file: Optional[Union[str, os.PathLike, TextIO]] = None)
      :classmethod:


   .. py:method:: load_from_datfile(cls, dat_file: Optional[Union[str, os.PathLike, BinaryIO]] = None)
      :classmethod:


   .. py:method:: load(cls)
      :classmethod:



.. py:function:: main()


