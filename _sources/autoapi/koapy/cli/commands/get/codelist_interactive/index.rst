:py:mod:`koapy.cli.commands.get.codelist_interactive`
=====================================================

.. py:module:: koapy.cli.commands.get.codelist_interactive


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.cli.commands.get.codelist_interactive.MarketEntry
   koapy.cli.commands.get.codelist_interactive.StockEntry
   koapy.cli.commands.get.codelist_interactive.StatusBarHandler
   koapy.cli.commands.get.codelist_interactive.Screen



Functions
~~~~~~~~~

.. autoapisummary::

   koapy.cli.commands.get.codelist_interactive.screen_len
   koapy.cli.commands.get.codelist_interactive.wrapper
   koapy.cli.commands.get.codelist_interactive.codelist_interactive
   koapy.cli.commands.get.codelist_interactive.main



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.cli.commands.get.codelist_interactive.markets


.. py:class:: MarketEntry(code, name)

   .. py:method:: to_string(self)



.. py:class:: StockEntry(code, name)

   .. py:method:: to_string(self)



.. py:data:: markets
   

   

.. py:class:: StatusBarHandler(screen, level=logging.NOTSET)

   Bases: :py:obj:`logging.Handler`

   Handler instances dispatch logging events to specific destinations.

   The base handler class. Acts as a placeholder which defines the Handler
   interface. Handlers can optionally use Formatter instances to format
   records as desired. By default, no formatter is specified; in this case,
   the 'raw' message as determined by record.message is logged.

   .. py:method:: emit(self, record)

      Do whatever it takes to actually log the specified logging record.

      This version is intended to be implemented by subclasses and so
      raises a NotImplementedError.



.. py:function:: screen_len(str)


.. py:class:: Screen(screen)

   .. py:method:: refresh_header_bar(self)


   .. py:method:: set_header_bar(self, text)


   .. py:method:: refresh_footer_bar(self)


   .. py:method:: set_footer_bar(self, text)


   .. py:method:: show_entries(self, entries)



.. py:function:: wrapper(stdscr)


.. py:function:: codelist_interactive()


.. py:function:: main()


