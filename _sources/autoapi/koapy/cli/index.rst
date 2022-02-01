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


Package Contents
----------------


Functions
~~~~~~~~~

.. autoapisummary::

   koapy.cli.configure
   koapy.cli.generate
   koapy.cli.get
   koapy.cli.install
   koapy.cli.serve
   koapy.cli.uninstall
   koapy.cli.update
   koapy.cli.get_credentials
   koapy.cli.fail_with_usage
   koapy.cli.verbose_option
   koapy.cli.get_logger
   koapy.cli.cli
   koapy.cli.login
   koapy.cli.watch
   koapy.cli.order
   koapy.cli.main



Attributes
~~~~~~~~~~

.. autoapisummary::

   koapy.cli.default_encoding
   koapy.cli.logger
   koapy.cli.help_option_names
   koapy.cli.context_settings
   koapy.cli.order_types
   koapy.cli.quote_types


.. py:function:: configure()


.. py:function:: generate()


.. py:function:: get()


.. py:function:: install()


.. py:function:: serve(ctx, verbose, **kwargs)


.. py:function:: uninstall()


.. py:function:: update()


.. py:function:: get_credentials(interactive=False)


.. py:function:: fail_with_usage(message=None, ctx=None)


.. py:function:: verbose_option(*args, **kwargs)


.. py:data:: default_encoding
   :annotation: = utf-8

   

.. py:function:: get_logger(name=None)


.. py:data:: logger
   

   

.. py:data:: help_option_names
   :annotation: = ['-h', '--help']

   

.. py:data:: context_settings
   

   

.. py:function:: cli()


.. py:function:: login(interactive, disable_auto_login, port)


.. py:function:: watch(codes, input, fids, realtype, output, format, port)


.. py:data:: order_types
   :annotation: = ['1', '2', '3', '4', '5', '6']

   

.. py:data:: quote_types
   :annotation: = ['00', '03', '05', '06', '07', '10', '13', '16', '20', '23', '26', '61', '62', '81']

   

.. py:function:: order(request_name, screen_no, account_no, order_type, code, quantity, price, quote_type, original_order_no, format, port)

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


