:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo`
=========================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo.KiwoomOpenApiPlusTrInfo



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo.main
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo.infer_fids_by_tr_outputs



.. py:class:: KiwoomOpenApiPlusTrInfo(tr_code: Optional[str] = None, name: Optional[str] = None, tr_name: Optional[str] = None, tr_names_svr: Optional[str] = None, tr_type: Optional[str] = None, gfid: Optional[str] = None, inputs: Optional[Sequence[Field]] = None, single_outputs_name: Optional[str] = None, single_outputs: Optional[Sequence[Field]] = None, multi_outputs_name: Optional[str] = None, multi_outputs: Optional[Sequence[Field]] = None)

   Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:class:: Field(name: Optional[str] = None, start: Optional[int] = None, offset: Optional[int] = None, fid: Optional[int] = None)

      Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`


   .. py:attribute:: TRINFO_BY_CODE_DUMP_FILEDIR
      

      

   .. py:attribute:: TRINFO_BY_CODE_DUMP_FILENAME
      :annotation: = trinfo_by_code.json

      

   .. py:attribute:: TRINFO_BY_CODE_DUMP_FILEPATH
      

      

   .. py:attribute:: TRINFO_BY_CODE
      :annotation: :Dict[str, KiwoomOpenApiPlusTrInfo]

      

   .. py:attribute:: SINGLE_TO_MULTI_TRCODES
      :annotation: = ['opt10072', 'opt10073', 'opt10075', 'opt10076', 'opt10085', 'optkwfid', 'optkwinv', 'optkwpro']

      

   .. py:method:: to_dict(self) -> Dict[str, Any]


   .. py:method:: from_dict(cls, dic: Dict[str, Any]) -> KiwoomOpenApiPlusTrInfo
      :classmethod:


   .. py:method:: get_input_names(self) -> List[str]


   .. py:method:: get_single_output_names(self) -> List[str]


   .. py:method:: get_multi_output_names(self) -> List[str]


   .. py:method:: get_trcode_list(cls) -> List[str]
      :classmethod:


   .. py:method:: get_trinfo_list(cls) -> List[KiwoomOpenApiPlusTrInfo]
      :classmethod:


   .. py:method:: get_trinfo_by_code(cls, trcode: str) -> Optional[KiwoomOpenApiPlusTrInfo]
      :classmethod:


   .. py:method:: from_code(cls, trcode: str) -> Optional[KiwoomOpenApiPlusTrInfo]
      :classmethod:


   .. py:method:: from_encfile(cls, f: Union[str, os.PathLike, TextIO], tr_code: Optional[str] = None, encoding: Optional[str] = None) -> KiwoomOpenApiPlusTrInfo
      :classmethod:


   .. py:method:: infos_from_data_dir(cls, data_dir: Optional[Union[str, os.PathLike]] = None, encoding: Optional[str] = None, module_path: Optional[str] = None) -> List[KiwoomOpenApiPlusTrInfo]
      :classmethod:


   .. py:method:: swap_output_types(cls, item: KiwoomOpenApiPlusTrInfo) -> KiwoomOpenApiPlusTrInfo
      :classmethod:


   .. py:method:: trinfo_by_code_from_data_dir(cls, data_dir: Optional[Union[str, os.PathLike]] = None, post_process: bool = True) -> Dict[str, KiwoomOpenApiPlusTrInfo]
      :classmethod:


   .. py:method:: dump_trinfo_by_code(cls, dump_file: Optional[Union[str, os.PathLike, TextIO]] = None, data_dir: Optional[str] = None, encoding: Optional[str] = None)
      :classmethod:


   .. py:method:: trinfo_by_code_from_dump_file(cls, dump_file: Optional[Union[str, os.PathLike, TextIO]] = None, encoding: Optional[str] = None) -> Dict[str, KiwoomOpenApiPlusTrInfo]
      :classmethod:


   .. py:method:: load_from_dump_file(cls, dump_file: Optional[Union[str, os.PathLike, TextIO]] = None)
      :classmethod:


   .. py:method:: load_from_data_dir(cls, data_dir: Optional[Union[str, os.PathLike]] = None)
      :classmethod:


   .. py:method:: load(cls)
      :classmethod:



.. py:function:: main()


.. py:function:: infer_fids_by_tr_outputs(output_filename=None)


