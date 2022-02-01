:py:mod:`koapy.cli.extensions.parser`
=====================================

.. py:module:: koapy.cli.extensions.parser


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.cli.extensions.parser.ArgumentParser
   koapy.cli.extensions.parser.ClickArgumentParser




Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.cli.extensions.parser.Function
   koapy.cli.extensions.parser.FunctionOrCommand
   koapy.cli.extensions.parser.ArgumentDecorator
   koapy.cli.extensions.parser.CommandDecorator


.. py:data:: Function
   

   

.. py:data:: FunctionOrCommand
   

   

.. py:data:: ArgumentDecorator
   

   

.. py:data:: CommandDecorator
   

   

.. py:class:: ArgumentParser

   .. py:method:: parse_args(self, args: Optional[Sequence[str]] = None, namespace: Optional[argparse.Namespace] = None) -> argparse.Namespace
      :abstractmethod:


   .. py:method:: parse_known_args(self, args: Optional[Sequence[str]] = None, namespace: Optional[argparse.Namespace] = None) -> Tuple[argparse.Namespace, List[str]]
      :abstractmethod:



.. py:class:: ClickArgumentParser(params: Sequence[ArgumentDecorator], command: Optional[CommandDecorator] = None, help_option_names: Optional[Sequence[str]] = None)

   Bases: :py:obj:`ArgumentParser`

   .. py:method:: parse_args(self, args: Optional[Sequence[str]] = None, namespace: Optional[argparse.Namespace] = None) -> argparse.Namespace


   .. py:method:: parse_known_args(self, args: Optional[Sequence[str]] = None, namespace: Optional[argparse.Namespace] = None) -> Tuple[argparse.Namespace, List[str]]



