:py:mod:`koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler`
=========================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.utils.pyside2.QSignalHandler.QSignalHandler




.. py:class:: QSignalHandler(signals: Iterable[signal.Signals], parent: Optional[koapy.compat.pyside2.QtCore.QObject])           QSignalHandler(parent: Optional[koapy.compat.pyside2.QtCore.QObject])

   Bases: :py:obj:`koapy.utils.logging.pyside2.QAbstractSocketLogging.QAbstractSocketLogging`

   .. py:attribute:: signaled
      

      

   .. py:method:: onReadyRead(self)


   .. py:method:: emitSignal(self, signal, frame)


   .. py:method:: setWakeUpFileDescriptor(self, descriptor, warn_on_full_buffer=True)


   .. py:method:: restoreWakeUpFileDescrptor(self)


   .. py:method:: setHandler(self, signal, handler)


   .. py:method:: restoreHandler(self, signal, default=None)


   .. py:method:: restoreAllHandlers(self)


   .. py:method:: setAll(self)


   .. py:method:: restoreAll(self)



