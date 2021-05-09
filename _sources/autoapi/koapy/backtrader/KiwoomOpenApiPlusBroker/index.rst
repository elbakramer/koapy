:mod:`koapy.backtrader.KiwoomOpenApiPlusBroker`
===============================================

.. py:module:: koapy.backtrader.KiwoomOpenApiPlusBroker


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KiwoomOpenApiPlusBroker.KiwoomOpenApiPlusCommInfo
   koapy.backtrader.KiwoomOpenApiPlusBroker.MetaKiwoomOpenApiPlusBroker
   koapy.backtrader.KiwoomOpenApiPlusBroker.KiwoomOpenApiPlusBroker




.. class:: KiwoomOpenApiPlusCommInfo(*args, **kwargs)


   Bases: :py:obj:`backtrader.comminfo.CommInfoBase`

   .. attribute:: params
      :annotation: = [['stocklike', True], None, ['percabs', False], ['commission', 0.015], ['tax', 0.25], ['mult', 1.0]]

      

   .. method:: _getcommissionbuy(self, size, price, pseudoexec)


   .. method:: _getcommissionsell(self, size, price, pseudoexec)


   .. method:: _getcommission(self, size, price, pseudoexec)



.. class:: MetaKiwoomOpenApiPlusBroker(cls, name, bases, dct)


   Bases: :py:obj:`backtrader.BrokerBase.__class__`


.. class:: KiwoomOpenApiPlusBroker(*args, **kwargs)


   Bases: :py:obj:`with_metaclass`\ (\ :py:obj:`MetaKiwoomOpenApiPlusBroker`\ , :py:obj:`BrokerBase`\ )

   .. attribute:: params
      :annotation: = [['use_positions', True], None]

      

   .. attribute:: _store
      

      

   .. method:: start(self)


   .. method:: data_started(self, data)


   .. method:: stop(self)


   .. method:: getcash(self)


   .. method:: getvalue(self, datas=None)


   .. method:: getposition(self, data, clone=True)


   .. method:: orderstatus(self, order)


   .. method:: _submit(self, oref)


   .. method:: _reject(self, oref)


   .. method:: _accept(self, oref)


   .. method:: _cancel(self, oref)


   .. method:: _expire(self, oref)


   .. method:: _bracketnotif(self, order)


   .. method:: _bracketize(self, order, cancel=False)


   .. method:: _fill(self, oref, size, price, ttype, **kwargs)


   .. method:: _transmit(self, order)


   .. method:: buy(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None, transmit=True, **kwargs)


   .. method:: sell(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None, transmit=True, **kwargs)


   .. method:: cancel(self, order)


   .. method:: notify(self, order)


   .. method:: get_notification(self)


   .. method:: next(self)


   .. method:: submit(self, order)


   .. method:: add_order_history(self, orders, notify=False)


   .. method:: set_fund_history(self, fund)



