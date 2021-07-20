:mod:`koapy.utils.subprocess`
=============================

.. py:module:: koapy.utils.subprocess


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.subprocess.function_to_script
   koapy.utils.subprocess.function_to_subprocess_args
   koapy.utils.subprocess.get_executable_from_conda_envname
   koapy.utils.subprocess.get_executable_from_conda_envpath
   koapy.utils.subprocess.get_executable_from_executable_config
   koapy.utils.subprocess.get_32bit_executable
   koapy.utils.subprocess.get_64bit_executable
   koapy.utils.subprocess.run_file
   koapy.utils.subprocess.run_script
   koapy.utils.subprocess.run_function



.. function:: function_to_script(func)


.. function:: function_to_subprocess_args(func, executable=None)


.. function:: get_executable_from_conda_envname(envname)


.. function:: get_executable_from_conda_envpath(envpath)


.. function:: get_executable_from_executable_config(executable_config)


.. function:: get_32bit_executable()


.. function:: get_64bit_executable()


.. function:: run_file(filename, *args, executable=None, **kwargs)


.. function:: run_script(script, *args, executable=None, **kwargs)


.. function:: run_function(function, *args, executable=None, **kwargs)


