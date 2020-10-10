import collections

from backtrader import BrokerBase, Order, BuyOrder, SellOrder
from backtrader.utils.py3 import with_metaclass

from backtrader.comminfo import CommInfoBase
from backtrader.position import Position

from koapy.backtrader.KiwoomOpenApiStore import KiwoomOpenApiStore

class KiwoomOpenApiCommInfo(CommInfoBase):

    # pylint: disable=no-member

    params = (
        ('stocklike', True),
        ('commtype', CommInfoBase.COMM_PERC),
        ('percabs', False),
        ('commission', 0.015),
        ('tax', 0.25),
        ('mult', 1.0),
    )

    def __init__(self):
        super().__init__()

        if self._commtype == self.COMM_PERC and not self.p.percabs:
            self.p.tax /= 100.0

    def _getcommissionbuy(self, size, price, pseudoexec): # pylint: disable=unused-argument
        return size * price * self.p.commission * self.p.mult

    def _getcommissionsell(self, size, price, pseudoexec): # pylint: disable=unused-argument
        return abs(size) * price * (self.p.commission + self.p.tax) * self.p.mult

    def _getcommission(self, size, price, pseudoexec):
        if size < 0:
            return self._getcommissionsell(size, price, pseudoexec)
        else:
            return self._getcommissionbuy(size, price, pseudoexec)

class MetaKiwoomOpenApiBroker(BrokerBase.__class__):

    def __init__(cls, name, bases, dct):
        super().__init__(name, bases, dct)
        KiwoomOpenApiStore.BrokerCls = cls

class KiwoomOpenApiBroker(with_metaclass(MetaKiwoomOpenApiBroker, BrokerBase)):

    params = (
        ('use_positions', True),
        ('commission', KiwoomOpenApiCommInfo()),
    )

    _store = KiwoomOpenApiStore

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.k = self._store(*args, **kwargs)

        self.orders = collections.OrderedDict()  # orders by order id
        self.notifs = collections.deque()  # holds orders which are notified

        self.opending = collections.defaultdict(list)  # pending transmission
        self.brackets = dict()  # confirmed brackets

        self.startingcash = self.cash = 0.0
        self.startingvalue = self.value = 0.0
        self.positions = collections.defaultdict(Position)

    def start(self):
        super().start()
        self.k.start(broker=self)
        self.startingcash = self.cash = self.k.get_cash()
        self.startingvalue = self.value = self.k.get_value()

        if self.p.use_positions: # pylint: disable=no-member
            for p in self.k.get_positions():
                is_sell = p['side'] == 'sell'
                size = p['units']
                if is_sell:
                    size = -size
                price = p['avgPrice']
                self.positions[p['instrument']] = Position(size, price)

    def data_started(self, data):
        pos = self.getposition(data)

        if pos.size < 0:
            # pylint: disable=unexpected-keyword-arg
            order = SellOrder(data=data,
                              size=pos.size, price=pos.price,
                              exectype=Order.Market,
                              simulated=True)

            order.addcomminfo(self.getcommissioninfo(data))
            order.execute(0, pos.size, pos.price,
                          0, 0.0, 0.0,
                          pos.size, 0.0, 0.0,
                          0.0, 0.0,
                          pos.size, pos.price)

            order.completed()
            self.notify(order)

        elif pos.size > 0:
            # pylint: disable=unexpected-keyword-arg
            order = BuyOrder(data=data,
                             size=pos.size, price=pos.price,
                             exectype=Order.Market,
                             simulated=True)

            order.addcomminfo(self.getcommissioninfo(data))
            order.execute(0, pos.size, pos.price,
                          0, 0.0, 0.0,
                          pos.size, 0.0, 0.0,
                          0.0, 0.0,
                          pos.size, pos.price)

            order.completed()
            self.notify(order)

    def stop(self):
        super().stop()
        self.k.stop()

    def getcash(self):
        self.cash = self.k.get_cash()
        return self.cash

    def getvalue(self, datas=None):
        self.value = self.k.get_value()
        return self.value

    def getposition(self, data, clone=True): # pylint: disable=arguments-differ
        pos = self.positions[data._dataname] # pylint: disable=protected-access
        if clone:
            pos = pos.clone()
        return pos

    def orderstatus(self, order):
        order = self.orders[order.ref]
        return order.status

    def _submit(self, oref):
        order = self.orders[oref]
        order.submit(self)
        self.notify(order)
        for o in self._bracketnotif(order):
            o.submit(self)
            self.notify(o)

    def _reject(self, oref):
        order = self.orders[oref]
        order.reject(self)
        self.notify(order)
        self._bracketize(order, cancel=True)

    def _accept(self, oref):
        order = self.orders[oref]
        order.accept()
        self.notify(order)
        for o in self._bracketnotif(order):
            o.accept(self)
            self.notify(o)

    def _cancel(self, oref):
        order = self.orders[oref]
        order.cancel()
        self.notify(order)
        self._bracketize(order, cancel=True)

    def _expire(self, oref):
        order = self.orders[oref]
        order.expire()
        self.notify(order)
        self._bracketize(order, cancel=True)

    def _bracketnotif(self, order):
        pref = getattr(order.parent, 'ref', order.ref)  # parent ref or self
        br = self.brackets.get(pref, None)  # to avoid recursion
        return br[-2:] if br is not None else []

    def _bracketize(self, order, cancel=False):
        pref = getattr(order.parent, 'ref', order.ref)  # parent ref or self
        br = self.brackets.pop(pref, None)  # to avoid recursion
        if br is None:
            return

        if not cancel:
            if len(br) == 3:  # all 3 orders in place, parent was filled
                br = br[1:]  # discard index 0, parent
                for o in br:
                    o.activate()  # simulate activate for children
                self.brackets[pref] = br  # not done - reinsert children

            elif len(br) == 2:  # filling a children
                oidx = br.index(order)  # find index to filled (0 or 1)
                self._cancel(br[1 - oidx].ref)  # cancel remaining (1 - 0 -> 1)
        else:
            # Any cancellation cancel the others
            for o in br:
                if o.alive():
                    self._cancel(o.ref)

    def _fill(self, oref, size, price, ttype, **kwargs): # pylint: disable=unused-argument
        order = self.orders[oref]

        if not order.alive():  # can be a bracket
            pref = getattr(order.parent, 'ref', order.ref)
            if pref not in self.brackets:
                msg = ('Order fill received for {}, with price {} and size {} '
                       'but order is no longer alive and is not a bracket. '
                       'Unknown situation')
                msg.format(order.ref, price, size)
                self.put_notification(msg, order, price, size) # pylint: disable=no-member
                return

            # [main, stopside, takeside], neg idx to array are -3, -2, -1
            if ttype == 'STOP_LOSS_FILLED':
                order = self.brackets[pref][-2]
            elif ttype == 'TAKE_PROFIT_FILLED':
                order = self.brackets[pref][-1]
            else:
                msg = ('Order fill received for {}, with price {} and size {} '
                       'but order is no longer alive and is a bracket. '
                       'Unknown situation')
                msg.format(order.ref, price, size)
                self.put_notification(msg, order, price, size) # pylint: disable=no-member
                return

        data = order.data
        pos = self.getposition(data, clone=False)
        psize, pprice, opened, closed = pos.update(size, price)

        comminfo = self.getcommissioninfo(data) # pylint: disable=unused-variable

        closedvalue = closedcomm = 0.0
        openedvalue = openedcomm = 0.0
        margin = pnl = 0.0

        order.execute(data.datetime[0], size, price,
                      closed, closedvalue, closedcomm,
                      opened, openedvalue, openedcomm,
                      margin, pnl,
                      psize, pprice)

        if order.executed.remsize:
            order.partial()
            self.notify(order)
        else:
            order.completed()
            self.notify(order)
            self._bracketize(order)

    def _transmit(self, order):
        oref = order.ref
        pref = getattr(order.parent, 'ref', oref)  # parent ref or self

        if order.transmit:
            if oref != pref:  # children order
                # Put parent in orders dict, but add stopside and takeside
                # to order creation. Return the takeside order, to have 3s
                takeside = order  # alias for clarity
                parent, stopside = self.opending.pop(pref)
                for o in parent, stopside, takeside:
                    self.orders[o.ref] = o  # write them down

                self.brackets[pref] = [parent, stopside, takeside]
                self.k.order_create(parent, stopside, takeside)
                return takeside  # parent was already returned

            else:  # Parent order, which is not being transmitted
                self.orders[order.ref] = order
                return self.k.order_create(order)

        # Not transmitting
        self.opending[pref].append(order)
        return order

    def buy(self, owner, data,
            size, price=None, plimit=None,
            exectype=None, valid=None, tradeid=0, oco=None,
            trailamount=None, trailpercent=None,
            parent=None, transmit=True,
            **kwargs): # pylint: disable=arguments-differ

        # pylint: disable=unexpected-keyword-arg
        order = BuyOrder(owner=owner, data=data,
                         size=size, price=price, pricelimit=plimit,
                         exectype=exectype, valid=valid, tradeid=tradeid,
                         trailamount=trailamount, trailpercent=trailpercent,
                         parent=parent, transmit=transmit)

        order.addinfo(**kwargs)
        order.addcomminfo(self.getcommissioninfo(data))
        return self._transmit(order)

    def sell(self, owner, data,
             size, price=None, plimit=None,
             exectype=None, valid=None, tradeid=0, oco=None,
             trailamount=None, trailpercent=None,
             parent=None, transmit=True,
             **kwargs): # pylint: disable=arguments-differ

        # pylint: disable=unexpected-keyword-arg
        order = SellOrder(owner=owner, data=data,
                          size=size, price=price, pricelimit=plimit,
                          exectype=exectype, valid=valid, tradeid=tradeid,
                          trailamount=trailamount, trailpercent=trailpercent,
                          parent=parent, transmit=transmit)

        order.addinfo(**kwargs)
        order.addcomminfo(self.getcommissioninfo(data))
        return self._transmit(order)

    def cancel(self, order):
        order = self.orders[order.ref]
        if order.status == Order.Cancelled:
            return
        return self.k.order_cancel(order)

    def notify(self, order):
        self.notifs.append(order.clone())

    def get_notification(self):
        if not self.notifs:
            return None
        return self.notifs.popleft()

    def next(self):
        self.notifs.append(None)

    # below may not accurate

    def submit(self, order):
        return self._transmit(order)

    def add_order_history(self, orders, notify=False):
        return self.k.add_order_history(orders, notify)

    def set_fund_history(self, fund):
        return self.k.set_fund_history(fund)
