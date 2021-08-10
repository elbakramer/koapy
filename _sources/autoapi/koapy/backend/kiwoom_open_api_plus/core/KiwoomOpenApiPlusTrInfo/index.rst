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



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo.__outer_class__


.. py:class:: KiwoomOpenApiPlusTrInfo(tr_code=None, name=None, tr_name=None, tr_names_svr=None, tr_type=None, gfid=None, inputs=None, single_outputs_name=None, single_outputs=None, multi_outputs_name=None, multi_outputs=None)

   Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:class:: Field(name=None, start=None, offset=None, fid=None)

      Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

      .. py:attribute:: __outer_class__
         

         

      .. py:method:: __repr__(self)

         Return repr(self).


      .. py:method:: __eq__(self, other)

         Return self==value.



   .. py:attribute:: _TRINFO_BY_CODE_DUMP_FILEDIR
      

      

   .. py:attribute:: _TRINFO_BY_CODE_DUMP_FILENAME
      :annotation: = trinfo_by_code.json

      

   .. py:attribute:: _TRINFO_BY_CODE_DUMP_FILEPATH
      

      

   .. py:attribute:: _TRINFO_BY_CODE
      

      

   .. py:attribute:: _SINGLE_TO_MULTI_TRCODES
      :annotation: = ['opt10072', 'opt10073', 'opt10075', 'opt10076', 'opt10085', 'optkwfid', 'optkwinv', 'optkwpro']

      

   .. py:method:: __repr__(self)

      Return repr(self).


   .. py:method:: __eq__(self, other)

      Return self==value.


   .. py:method:: to_dict(self)


   .. py:method:: from_dict(cls, dic)
      :classmethod:


   .. py:method:: get_input_names(self)


   .. py:method:: get_single_output_names(self)


   .. py:method:: get_multi_output_names(self)


   .. py:method:: get_trinfo_by_code(cls, trcode)
      :classmethod:


   .. py:method:: from_encfile(cls, f, tr_code=None)
      :classmethod:


   .. py:method:: infos_from_data_dir(cls, data_dir=None, encoding=None, module_path=None)
      :classmethod:


   .. py:method:: _single_outputs_are_actually_multi_outputs(cls, item)
      :classmethod:


   .. py:method:: trinfo_by_code_from_data_dir(cls, data_dir=None, post_process=True)
      :classmethod:


   .. py:method:: dump_trinfo_by_code(cls, dump_file=None, data_dir=None)
      :classmethod:


   .. py:method:: trinfo_by_code_from_dump_file(cls, dump_file=None)
      :classmethod:


   .. py:method:: load_from_dump_file(cls, dump_file=None)
      :classmethod:


   .. py:method:: load_from_data_dir(cls, data_dir=None)
      :classmethod:


   .. py:method:: load(cls)
      :classmethod:



.. py:data:: __outer_class__
   

   

.. py:function:: main()


.. py:function:: infer_fids_by_tr_outputs(output_filename=None)


