:py:mod:`koapy.cli.utils.openapi`
=================================

.. py:module:: koapy.cli.utils.openapi


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.cli.utils.openapi.download_openapi_installer
   koapy.cli.utils.openapi.prepare_issfile_for_install
   koapy.cli.utils.openapi.prepare_issfile_for_uninstall
   koapy.cli.utils.openapi.run_installer_with_issfile



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.cli.utils.openapi.logger
   koapy.cli.utils.openapi.iss_file_encoding


.. py:data:: logger
   

   

.. py:data:: iss_file_encoding
   :annotation: = euc-kr

   

.. py:function:: download_openapi_installer(filepath)


.. py:function:: prepare_issfile_for_install(filepath, target=None)


.. py:function:: prepare_issfile_for_uninstall(filepath, reboot=False)


.. py:function:: run_installer_with_issfile(installer, issfile, logfile=None, cwd=None)


