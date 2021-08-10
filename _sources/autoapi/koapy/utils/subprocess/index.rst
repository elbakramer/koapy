:py:mod:`koapy.utils.subprocess`
================================

.. py:module:: koapy.utils.subprocess


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.utils.subprocess.function_to_script
   koapy.utils.subprocess.function_to_subprocess_args
   koapy.utils.subprocess.run_file
   koapy.utils.subprocess.run_script
   koapy.utils.subprocess.run_function
   koapy.utils.subprocess.quote
   koapy.utils.subprocess.run_as_admin



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.utils.subprocess.logger


.. py:data:: logger
   

   

.. py:function:: function_to_script(func)


.. py:function:: function_to_subprocess_args(func, executable=None)


.. py:function:: run_file(filename, *args, executable=None, **kwargs)


.. py:function:: run_script(script, *args, executable=None, **kwargs)


.. py:function:: run_function(function, *args, executable=None, **kwargs)


.. py:function:: quote(s)


.. py:function:: run_as_admin(cmd, cwd=None, check=True, wait=True)


