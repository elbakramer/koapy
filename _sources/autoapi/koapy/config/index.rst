:py:mod:`koapy.config`
======================

.. py:module:: koapy.config


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.config.read_config
   koapy.config.config_from_dict
   koapy.config.find_user_config_file_in
   koapy.config.find_user_config_file_from
   koapy.config.set_user_config
   koapy.config.initialize_config_from_given_path
   koapy.config.initialize_config_from_expected_paths
   koapy.config.get_config
   koapy.config.get_user_config
   koapy.config.dump_config
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

   koapy.config.Config
   koapy.config.default_config_filename
   koapy.config.default_config_file_directory
   koapy.config.default_config_filepath
   koapy.config.current_working_directory
   koapy.config.home_directory
   koapy.config.default_user_config_filename
   koapy.config.user_config_filename_cadidates
   koapy.config.default_user_config_filepath
   koapy.config.default_encoding
   koapy.config.default_config
   koapy.config.empty_config
   koapy.config.user_config
   koapy.config.config
   koapy.config.debug


.. py:data:: Config
   

   

.. py:data:: default_config_filename
   :annotation: = config.conf

   

.. py:data:: default_config_file_directory
   

   

.. py:data:: default_config_filepath
   

   

.. py:data:: current_working_directory
   

   

.. py:data:: home_directory
   

   

.. py:data:: default_user_config_filename
   :annotation: = koapy.conf

   

.. py:data:: user_config_filename_cadidates
   

   

.. py:data:: default_user_config_filepath
   

   

.. py:data:: default_encoding
   :annotation: = utf-8

   

.. py:function:: read_config(filename: Optional[Union[os.PathLike, str]] = None, encoding: Optional[str] = None) -> Config


.. py:function:: config_from_dict(dictionary: Mapping[str, Any]) -> Config


.. py:data:: default_config
   

   

.. py:function:: find_user_config_file_in(searching_directory: Optional[Union[os.PathLike, str]] = None) -> Optional[pathlib.Path]


.. py:function:: find_user_config_file_from(starting_directory: Optional[Union[os.PathLike, str]] = None) -> Optional[pathlib.Path]


.. py:data:: empty_config
   

   

.. py:data:: user_config
   

   

.. py:data:: config
   

   

.. py:function:: set_user_config(c: Config) -> Config


.. py:function:: initialize_config_from_given_path(filename: Optional[Union[os.PathLike, str]] = None) -> bool


.. py:function:: initialize_config_from_expected_paths() -> bool


.. py:function:: get_config() -> Config


.. py:function:: get_user_config() -> Config


.. py:data:: debug
   :annotation: = False

   

.. py:function:: dump_config(config: Config, compact: bool = False, indent: int = 4) -> str


.. py:function:: save_config(filename: Union[os.PathLike, str], config: Optional[Config] = None, compact: bool = False, indent: int = 4, encoding: Optional[str] = None)


.. py:function:: save_user_config(filename: Optional[Union[os.PathLike, str]] = None, user_config: Optional[Config] = None, compact: bool = False, indent: int = 4, encoding: Optional[str] = None)


.. py:function:: get_executable_from_conda_envname(envname: str) -> str


.. py:function:: get_executable_from_conda_envpath(envpath: str) -> str


.. py:function:: get_executable_from_executable_config(executable_config: Config) -> Optional[str]


.. py:function:: get_32bit_executable() -> Optional[str]


.. py:function:: get_64bit_executable() -> Optional[str]


