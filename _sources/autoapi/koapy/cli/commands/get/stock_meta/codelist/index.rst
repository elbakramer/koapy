:py:mod:`koapy.cli.commands.get.stock_meta.codelist`
====================================================

.. py:module:: koapy.cli.commands.get.stock_meta.codelist


Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.cli.commands.get.stock_meta.codelist.codelist
   koapy.cli.commands.get.stock_meta.codelist.main



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.cli.commands.get.stock_meta.codelist.market_codes


.. py:data:: market_codes
   :annotation: = ['0', '10', '3', '8', '50', '4', '5', '6', '9', '30', 'all']

   

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


.. py:function:: main()


