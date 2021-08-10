:py:mod:`koapy.config`
======================

.. py:module:: koapy.config


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.config.read_config
   koapy.config.save_config
   koapy.config.save_user_config
   koapy.config.get_executable_from_conda_envname
   koapy.config.get_executable_from_conda_envpath
   koapy.config.get_executable_from_executable_config
   koapy.config.get_32bit_executable
   koapy.config.get_64bit_executable



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.config.default_config_filename
   koapy.config.default_config_file_directory
   koapy.config.default_config_filepath
   koapy.config.default_config
   koapy.config.empty_config
   koapy.config.user_config
   koapy.config.home
   koapy.config.cwd
   koapy.config.config_folder_candidates
   koapy.config.config_filename_cadidates
   koapy.config.default_user_config_path
   koapy.config.config_path
   koapy.config.config
   koapy.config._config
   koapy.config._user_config


.. py:function:: read_config(filename)


.. py:data:: default_config_filename
   :annotation: = config.conf

   

.. py:data:: default_config_file_directory
   

   

.. py:data:: default_config_filepath
   

   

.. py:data:: default_config
   

   

.. py:data:: empty_config
   

   

.. py:data:: user_config
   

   

.. py:data:: home
   

   

.. py:data:: cwd
   

   

.. py:data:: config_folder_candidates
   

   

.. py:data:: config_filename_cadidates
   :annotation: = ['koapy.conf', '.koapy.conf']

   

.. py:data:: default_user_config_path
   

   

.. py:data:: config_path
   

   

.. py:data:: config
   

   

.. py:data:: _config
   

   

.. py:data:: _user_config
   

   

.. py:function:: save_config(filename, config=None, compact=True, indent=4)


.. py:function:: save_user_config(filename=None, user_config=None)


.. py:function:: get_executable_from_conda_envname(envname)


.. py:function:: get_executable_from_conda_envpath(envpath)


.. py:function:: get_executable_from_executable_config(executable_config)


.. py:function:: get_32bit_executable()


.. py:function:: get_64bit_executable()


