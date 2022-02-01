:py:mod:`koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication`
========================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusManagerApplicationArgumentParser
   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusServerApplicationProcess
   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusServerApplicationSubprocess
   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusManagerApplication.KiwoomOpenApiPlusManagerApplication




.. py:class:: KiwoomOpenApiPlusManagerApplicationArgumentParser

   Bases: :py:obj:`koapy.cli.extensions.parser.ArgumentParser`

   .. py:method:: parse_args(self, args: Optional[Sequence[str]] = None, namespace: Optional[argparse.Namespace] = None) -> argparse.Namespace


   .. py:method:: parse_known_args(self, args: Optional[Sequence[str]] = None, namespace: Optional[argparse.Namespace] = None) -> Tuple[argparse.Namespace, List[str]]



.. py:class:: KiwoomOpenApiPlusServerApplicationProcess(args, parent=None)

   Bases: :py:obj:`koapy.compat.pyside2.QtCore.QProcess`


.. py:class:: KiwoomOpenApiPlusServerApplicationSubprocess(args, parent=None)

   .. py:method:: start(self)


   .. py:method:: waitForStarted(self, msecs: int = 30000) -> bool


   .. py:method:: close(self)


   .. py:method:: waitForFinished(self, msecs: int = 30000) -> bool



.. py:class:: KiwoomOpenApiPlusManagerApplication(args=())

   Bases: :py:obj:`koapy.utils.logging.pyside2.QObjectLogging.QObjectLogging`

   .. py:class:: ConnectionStatus

      Bases: :py:obj:`enum.Enum`

      Generic enumeration.

      Derive from this class to define new enumerations.

      .. py:attribute:: DISCONNECTED
         :annotation: = 1

         

      .. py:attribute:: CONNECTED
         :annotation: = 2

         


   .. py:class:: ServerType

      Bases: :py:obj:`enum.Enum`

      Generic enumeration.

      Derive from this class to define new enumerations.

      .. py:attribute:: SIMULATION
         :annotation: = 1

         

      .. py:attribute:: REAL
         :annotation: = 2

         

      .. py:attribute:: UNKNOWN
         :annotation: = 3

         


   .. py:class:: RestartType

      Bases: :py:obj:`enum.Enum`

      Generic enumeration.

      Derive from this class to define new enumerations.

      .. py:attribute:: RESTART_ONLY
         :annotation: = 1

         

      .. py:attribute:: RESTART_AND_CONNECT
         :annotation: = 2

         


   .. py:attribute:: shouldRestart
      

      

   .. py:method:: close(self)


   .. py:method:: exec_(self)


   .. py:method:: exit(self, return_code=0)


   .. py:method:: restart(self, restart_type: Optional[RestartType] = None)


   .. py:method:: execAndExit(self)


   .. py:method:: main(cls, args=None)
      :classmethod:



