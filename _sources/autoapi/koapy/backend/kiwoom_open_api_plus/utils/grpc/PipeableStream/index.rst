:mod:`koapy.backend.kiwoom_open_api_plus.utils.grpc.PipeableStream`
===================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.grpc.PipeableStream


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.grpc.PipeableStream.PipeableStream




.. class:: PipeableStream(stream, generator=None)


   Bases: :py:obj:`collections.abc.Iterator`

   .. method:: __next__(self)

      Return the next item from the iterator. When exhausted, raise StopIteration


   .. method:: pipe(self, func)


   .. method:: __getattr__(self, name)



