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

      


.. py:class:: MetaKiwoomOpenApiPlusBroker(cls, name, bases, dct)

   Bases: :py:obj:`backtrader.BrokerBase.__class__`


.. py:class:: KiwoomOpenApiPlusBroker(*args, **kwargs)

   Bases: :py:obj:`with_metaclass`\ (\ :py:obj:`MetaKiwoomOpenApiPlusBroker`\ , :py:obj:`BrokerBase`\ )

   .. py:attribute:: params
      :annotation: = [['use_positions', True], None]

      

   .. py:method:: start(self)


   .. py:method:: data_started(self, data)


   .. py:method:: stop(self)


   .. py:method:: getcash(self)


   .. py:method:: getvalue(self, datas=None)


   .. py:method:: getposition(self, data, clone=True)


   .. py:method:: orderstatus(self, order)


   .. py:method:: buy(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None, transmit=True, **kwargs)


   .. py:method:: sell(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, parent=None, transmit=True, **kwargs)


   .. py:method:: cancel(self, order)


   .. py:method:: notify(self, order)


   .. py:method:: get_notification(self)


   .. py:method:: next(self)


   .. py:method:: submit(self, order)


   .. py:method:: add_order_history(self, orders, notify=False)


   .. py:method:: set_fund_history(self, fund)



