:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector`
==================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector.KiwoomOpenApiPlusSignalConnector
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusSignalConnector.KiwoomOpenApiPlusOnReceiveRealDataSignalConnector




.. py:class:: KiwoomOpenApiPlusSignalConnector(name)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: is_valid_slot(self, slot)


   .. py:method:: connect_to(self, control)


   .. py:method:: connect(self, slot)


   .. py:method:: disconnect(self, slot=None)


   .. py:method:: call(self, *args, **kwargs)


   .. py:method:: __call__(self, *args, **kwargs)



.. py:class:: KiwoomOpenApiPlusOnReceiveRealDataSignalConnector(control)

   Bases: :py:obj:`KiwoomOpenApiPlusSignalConnector`

   .. py:method:: SetRealReg(self, screen_no, code_list, fid_list, opt_type)


   .. py:method:: SetRealRemove(self, screen_no, code)


   .. py:method:: call(self, code, realtype, realdata)



