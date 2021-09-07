:py:mod:`koapy.utils.logging.tqdm.TqdmStreamHandler`
====================================================

.. py:module:: koapy.utils.logging.tqdm.TqdmStreamHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.logging.tqdm.TqdmStreamHandler.TqdmStreamHandler




.. py:class:: TqdmStreamHandler(stream=None)

   Bases: :py:obj:`logging.StreamHandler`

   A handler class which writes logging records, appropriately formatted,
   to a stream. Note that this class does not close the stream, as
   sys.stdout or sys.stderr may be used.


