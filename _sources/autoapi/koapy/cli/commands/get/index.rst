:py:mod:`koapy.cli.commands.get`
================================

.. py:module:: koapy.cli.commands.get


Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   account_data/index.rst
   chart_data/index.rst
   openapi_meta/index.rst
   stock_meta/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.cli.commands.get.deposit
   koapy.cli.commands.get.evaluation
   koapy.cli.commands.get.orders
   koapy.cli.commands.get.userinfo
   koapy.cli.commands.get.daily
   koapy.cli.commands.get.minute
   koapy.cli.commands.get.errmsg
   koapy.cli.commands.get.modulepath
   koapy.cli.commands.get.realinfo
   koapy.cli.commands.get.trinfo
   koapy.cli.commands.get.codelist
   koapy.cli.commands.get.stockcode
   koapy.cli.commands.get.stockinfo
   koapy.cli.commands.get.stockname
   koapy.cli.commands.get.get



.. py:function:: deposit(account, port)


.. py:function:: evaluation(account, include_delisted, exclude_delisted, for_each, as_summary, port)


.. py:function:: orders(account, date, reverse, executed_only, not_executed_only, stock_only, bond_only, sell_only, buy_only, code, starting_order_no, port)


.. py:function:: userinfo(port)


.. py:function:: daily(code, output, format, start_date, end_date, port)


.. py:function:: minute(code, interval, output, format, start_date, end_date, port)


.. py:function:: errmsg(err_code)


.. py:function:: modulepath()


.. py:function:: realinfo(realtypes)


.. py:function:: trinfo(trcodes)


.. py:function:: codelist(markets, port)

   
   Possible market codes are:
     0 : 장내
     10 : 코스닥
     3 : ELW
     8 : ETF
     50 : KONEX
     4 : 뮤추얼펀드
     5 : 신주인수권
     6 : 리츠
     9 : 하이얼펀드
     30 : K-OTC


.. py:function:: stockcode(names, markets, port)

   
   Possible market codes are:
     0 : 장내
     10 : 코스닥
     3 : ELW
     8 : ETF
     50 : KONEX
     4 : 뮤추얼펀드
     5 : 신주인수권
     6 : 리츠
     9 : 하이얼펀드
     30 : K-OTC


.. py:function:: stockinfo(code, output, format, port)


.. py:function:: stockname(codes, port)


.. py:function:: get()


