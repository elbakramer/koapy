:py:mod:`koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusServerApplication`
=======================================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusServerApplication


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusServerApplication.KiwoomOpenApiPlusServerApplicationArgumentParser
   koapy.backend.kiwoom_open_api_plus.pyside2.KiwoomOpenApiPlusServerApplication.KiwoomOpenApiPlusServerApplication




.. py:class:: KiwoomOpenApiPlusServerApplicationArgumentParser

   Bases: :py:obj:`koapy.cli.extensions.parser.ArgumentParser`

   .. py:method:: parse_args(self, args: Optional[Sequence[str]] = None, namespace: Optional[argparse.Namespace] = None) -> argparse.Namespace


   .. py:method:: parse_known_args(self, args: Optional[Sequence[str]] = None, namespace: Optional[argparse.Namespace] = None) -> Tuple[argparse.Namespace, List[str]]



.. py:class:: KiwoomOpenApiPlusServerApplication(args=())

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

         


   .. py:method:: exec_(self)


   .. py:method:: exit(self, return_code=0)


   .. py:method:: execAndExit(self)


   .. py:method:: main(cls, args=None)
      :classmethod:



