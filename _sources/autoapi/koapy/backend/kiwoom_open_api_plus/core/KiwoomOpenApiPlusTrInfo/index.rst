:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusTrInfo`
======================================================================

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


.. class:: KiwoomOpenApiPlusTrInfo(tr_code=None, name=None, tr_name=None, tr_names_svr=None, tr_type=None, gfid=None, inputs=None, single_outputs_name=None, single_outputs=None, multi_outputs_name=None, multi_outputs=None)


   Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. class:: Field(name=None, start=None, offset=None, fid=None)


      Bases: :py:obj:`koapy.utils.serialization.JsonSerializable`

      .. attribute:: __outer_class__
         

         

      .. method:: __repr__(self)

         Return repr(self).



   .. attribute:: _TRINFO_BY_CODE_DUMP_FILENAME
      :annotation: = trinfo_by_code.json

      

   .. attribute:: _TRINFO_BY_CODE
      

      

   .. attribute:: _SINGLE_TO_MULTI_TRCODES
      :annotation: = ['opt10075', 'opt10076', 'opt10085', 'optkwfid', 'optkwinv', 'optkwpro']

      

   .. method:: __repr__(self)

      Return repr(self).


   .. method:: to_dict(self)


   .. method:: from_dict(cls, dic)
      :classmethod:


   .. method:: get_input_names(self)


   .. method:: get_single_output_names(self)


   .. method:: get_multi_output_names(self)


   .. method:: get_trinfo_by_code(cls, trcode)
      :classmethod:


   .. method:: from_encfile(cls, f, tr_code=None)
      :classmethod:


   .. method:: infos_from_data_dir(cls, data_dir=None, encoding=None, module_path=None)
      :classmethod:


   .. method:: trinfo_by_code_from_data_dir(cls, data_dir=None)
      :classmethod:


   .. method:: dump_trinfo_by_code(cls, dump_file=None, data_dir=None)
      :classmethod:


   .. method:: _single_outputs_are_actually_multi_outputs(cls, item)
      :classmethod:


   .. method:: trinfo_by_code_from_dump_file(cls, dump_file=None)
      :classmethod:


   .. method:: load_from_dump_file(cls, dump_file=None)
      :classmethod:



.. data:: __outer_class__
   

   

.. function:: main()


.. function:: infer_fids_by_tr_outputs(output_filename=None)


