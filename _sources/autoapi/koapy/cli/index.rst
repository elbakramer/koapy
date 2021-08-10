:py:mod:`koapy.cli`
===================

.. py:module:: koapy.cli

.. autoapi-nested-parse::

   Console script for koapy.



Subpackages
-----------
.. toctree::
   :titlesonly:
   :maxdepth: 3

   commands/index.rst
   extensions/index.rst
   utils/index.rst


Submodules
----------
.. toctree::
   :titlesonly:
   :maxdepth: 1

   __main__/index.rst


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.cli.codelist
   koapy.cli.install
   koapy.cli.uninstall
   koapy.cli.update
   koapy.cli.fail_with_usage
   koapy.cli.verbose_option
   koapy.cli.get_credential
   koapy.cli.get_logger
   koapy.cli.cli
   koapy.cli.serve
   koapy.cli.login
   koapy.cli.configure
   koapy.cli.autologin
   koapy.cli.get
   koapy.cli.stockcode
   koapy.cli.stockname
   koapy.cli.stockinfo
   koapy.cli.daily
   koapy.cli.minute
   koapy.cli.trinfo
   koapy.cli.realinfo
   koapy.cli.userinfo
   koapy.cli.deposit
   koapy.cli.evaluation
   koapy.cli.orders
   koapy.cli.modulepath
   koapy.cli.errmsg
   koapy.cli.watch
   koapy.cli.order
   koapy.cli.main



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.cli.config
   koapy.cli.logger
   koapy.cli.context_settings
   koapy.cli.market_codes
   koapy.cli.minute_intervals
   koapy.cli.order_types
   koapy.cli.quote_types


.. py:function:: codelist(markets, port, verbose)

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


.. py:function:: install()


.. py:function:: uninstall()


.. py:function:: update()


.. py:function:: fail_with_usage(message=None)


.. py:function:: verbose_option(*args, **kwargs)


.. py:function:: get_credential(interactive=False)


.. py:data:: config
   

   

.. py:function:: get_logger(name=None)


.. py:data:: logger
   

   

.. py:data:: context_settings
   

   

.. py:function:: cli()


.. py:function:: serve(port, args, verbose)


.. py:function:: login(interactive, disable_auto_login, port, verbose)


.. py:function:: configure()


.. py:function:: autologin(port, verbose)


.. py:function:: get()


.. py:data:: market_codes
   :annotation: = ['0', '10', '3', '8', '50', '4', '5', '6', '9', '30', 'all']

   

.. py:function:: stockcode(names, markets, port, verbose)

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


.. py:function:: stockname(codes, port, verbose)


.. py:function:: stockinfo(code, output, format, port, verbose)


.. py:function:: daily(code, output, format, start_date, end_date, port, verbose)


.. py:data:: minute_intervals
   :annotation: = ['1', '3', '5', '10', '15', '30', '45', '60']

   

.. py:function:: minute(code, interval, output, format, start_date, end_date, port, verbose)


.. py:function:: trinfo(trcodes, verbose)


.. py:function:: realinfo(realtypes, verbose)


.. py:function:: userinfo(port, verbose)


.. py:function:: deposit(account, port, verbose)


.. py:function:: evaluation(account, include_delisted, exclude_delisted, for_each, as_summary, port, verbose)


.. py:function:: orders(account, date, reverse, executed_only, not_executed_only, stock_only, bond_only, sell_only, buy_only, code, starting_order_no, port, verbose)


.. py:function:: modulepath(verbose)


.. py:function:: errmsg(err_code, verbose)


.. py:function:: watch(codes, input, fids, realtype, output, format, port, verbose)


.. py:data:: order_types
   :annotation: = ['1', '2', '3', '4', '5', '6']

   

.. py:data:: quote_types
   :annotation: = ['00', '03', '05', '06', '07', '10', '13', '16', '20', '23', '26', '61', '62', '81']

   

.. py:function:: order(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no, format, port, verbose)

   
   [주문유형]
     1 : 신규매수
     2 : 신규매도
     3 : 매수취소
     4 : 매도취소
     5 : 매수정정
     6 : 매도정정

   
   [거래구분]
     모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.
     00 : 지정가
     03 : 시장가
     05 : 조건부지정가
     06 : 최유리지정가
     07 : 최우선지정가
     10 : 지정가IOC
     13 : 시장가IOC
     16 : 최유리IOC
     20 : 지정가FOK
     23 : 시장가FOK
     26 : 최유리FOK
     61 : 장전시간외종가
     62 : 시간외단일가매매
     81 : 장후시간외종가


.. py:function:: main()


