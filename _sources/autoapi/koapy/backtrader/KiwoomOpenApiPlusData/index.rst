:py:mod:`koapy.backtrader.KiwoomOpenApiPlusData`
================================================

.. py:module:: koapy.backtrader.KiwoomOpenApiPlusData


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.KiwoomOpenApiPlusData.MetaKiwoomOpenApiPlusData
   koapy.backtrader.KiwoomOpenApiPlusData.KiwoomOpenApiPlusData




.. py:class:: MetaKiwoomOpenApiPlusData(cls, clsname, bases, dct)

   Bases: :py:obj:`type`\ (\ :py:obj:`Logging`\ ), :py:obj:`type`\ (\ :py:obj:`DataBase`\ )


.. py:class:: KiwoomOpenApiPlusData(*args, **kwargs)

   Bases: :py:obj:`backtrader.feed.DataBase`, :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:attribute:: params
      :annotation: = [['qcheck', 0.5], ['historical', False], ['backfill_start', True], ['backfill', True],...

      

   .. py:attribute:: _store
      

      

   .. py:method:: _timeoffset(self)


   .. py:method:: isnaive(self, dt)


   .. py:method:: asutc(self, dt, tz=None, naive=True)


   .. py:method:: date2num(self, dt, tz=None)


   .. py:method:: num2date(self, dt=None, tz=None, naive=False)


   .. py:method:: fromtimestamp(self, timestamp, tz=None)


   .. py:method:: islive(self)


   .. py:method:: setenvironment(self, env)


   .. py:method:: start(self)


   .. py:method:: _st_start(self, instart=True, tmout=None)


   .. py:method:: stop(self)


   .. py:method:: haslivedata(self)


   .. py:method:: _load(self)


   .. py:method:: _load_tick(self, msg)


   .. py:method:: _load_history(self, msg)



