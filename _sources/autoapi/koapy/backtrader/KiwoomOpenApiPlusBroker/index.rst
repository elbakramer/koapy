:py:mod:`koapy.backtrader.KiwoomOpenApiPlusBroker`
==================================================

.. py:module:: koapy.backtrader.KiwoomOpenApiPlusBroker


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KiwoomOpenApiPlusBroker.KiwoomOpenApiPlusCommInfo
   koapy.backtrader.KiwoomOpenApiPlusBroker.MetaKiwoomOpenApiPlusBroker
   koapy.backtrader.KiwoomOpenApiPlusBroker.KiwoomOpenApiPlusBroker




.. py:class:: KiwoomOpenApiPlusCommInfo(*args, **kwargs)

   Bases: :py:obj:`backtrader.comminfo.CommInfoBase`

   .. py:attribute:: params
      :annotation: = [['stocklike', True], None, ['percabs', False], ['commission', 0.015], ['tax', 0.25], ['mult', 1.0]]

      

   .. py:method:: _getcommissionbuy(self, size, price, pseudoexec)


   .. py:method:: _getcommissionsell(self, size, price, pseudoexec)


   .. py:method:: _getcommission(self, size, price, pseudoexec)



.. py:class:: MetaKiwoomOpenApiPlusBroker(cls, name, bases, dct)

   Bases: :py:obj:`backtrader.BrokerBase.__class__`


.. py:class:: KiwoomOpenApiPlusBroker(*args, **kwargs)

   Bases: :py:obj:`with_metaclass`\ (\ :py:obj:`MetaKiwoomOpenApiPlusBroker`\ , :py:obj:`BrokerBase`\ )

   .. py:attribute:: params
      :annotation: = [['use_positions', True], None]

      

   .. py:attribute:: _store
      

      

   .. py:method:: start(self)


   .. py:method:: data_started(self, data)


   .. py:method:: stop(self)


   .. py:method:: getcash(self)


   .. py:method:: getvalue(self, datas=None)


   .. py:method:: getposition(self, data, clone=True)


   .. py:method:: orderstatus(self, order)


   .. py:method:: _submit(self, oref)


   .. py:method:: _reject(self, oref)


   .. py:method:: _accept(self, oref)


   .. py:method:: _cancel(self, oref)


   .. py:method:: _expire(self, oref)


   .. py:method:: _bracketnotif(self, order)


   .. py:method:: _bracketize(self, order, cancel=False)


   .. py:method:: _fill(self, oref, size, price, ttype, **kwargs)


   .. py:method:: _transmit(self, order)


   .. py:method:: buy(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None, transmit=True, **kwargs)


   .. py:method:: sell(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None, transmit=True, **kwargs)


   .. py:method:: cancel(self, order)


   .. py:method:: notify(self, order)


   .. py:method:: get_notification(self)


   .. py:method:: next(self)


   .. py:method:: submit(self, order)


   .. py:method:: add_order_history(self, orders, notify=False)


   .. py:method:: set_fund_history(self, fund)



