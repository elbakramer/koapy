:py:mod:`koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler`
=========================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler.QSignalHandler




.. py:class:: QSignalHandler(parent=None)

   Bases: :py:obj:`koapy.compat.pyside2.QtNetwork.QAbstractSocket`

   .. py:attribute:: signalReceived
      

      

   .. py:method:: onReadyRead(self)


   .. py:method:: setWakeUpFileDescriptor(self, descriptor)


   .. py:method:: restoreWakeUpFileDescrptor(self)


   .. py:method:: setHandler(self, signal, handler)


   .. py:method:: restoreHandler(self, signal, default=None)


   .. py:method:: restoreAllHandlers(self)


   .. py:method:: restoreAll(self)


   .. py:method:: __del__(self)



