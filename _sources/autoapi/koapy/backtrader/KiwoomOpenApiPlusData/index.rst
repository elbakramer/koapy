:mod:`koapy.backtrader.KiwoomOpenApiPlusData`
=============================================

.. py:module:: koapy.backtrader.KiwoomOpenApiPlusData


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KiwoomOpenApiPlusData.MetaKiwoomOpenApiPlusData
   koapy.backtrader.KiwoomOpenApiPlusData.KiwoomOpenApiPlusData




.. class:: MetaKiwoomOpenApiPlusData(cls, clsname, bases, dct)


   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`type`\ (\ :py:obj:`DataBase`\ )


.. class:: KiwoomOpenApiPlusData(*args, **kwargs)


   Bases: :py:obj:`backtrader.feed.DataBase`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. attribute:: params
      :annotation: = [['qcheck', 0.5], ['historical', False], ['backfill_start', True], ['backfill', True],...

      

   .. attribute:: _store
      

      

   .. method:: _timeoffset(self)


   .. method:: isnaive(self, dt)


   .. method:: asutc(self, dt, tz=None, naive=True)


   .. method:: date2num(self, dt, tz=None)


   .. method:: num2date(self, dt=None, tz=None, naive=False)


   .. method:: fromtimestamp(self, timestamp, tz=None)


   .. method:: islive(self)


   .. method:: setenvironment(self, env)


   .. method:: start(self)


   .. method:: _st_start(self, instart=True, tmout=None)


   .. method:: stop(self)


   .. method:: haslivedata(self)


   .. method:: _load(self)


   .. method:: _load_tick(self, msg)


   .. method:: _load_history(self, msg)



