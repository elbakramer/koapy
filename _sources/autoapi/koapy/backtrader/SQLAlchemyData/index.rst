:py:mod:`koapy.backtrader.SQLAlchemyData`
=========================================

.. py:module:: koapy.backtrader.SQLAlchemyData


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.SQLAlchemyData.SQLAlchemyData




.. py:class:: SQLAlchemyData

   Bases: :py:obj:`backtrader.feed.DataBase`

   .. py:attribute:: params
      :annotation: = [['url', None], ['engine', None], ['connection', None], ['tablename', None], ['timestampcolumn',...

      

   .. py:method:: _dispose_engine(self)


   .. py:method:: _initialize_engine(self)


   .. py:method:: _close_cursor(self)


   .. py:method:: _initialize_cursor(self)


   .. py:method:: start(self)


   .. py:method:: stop(self)


   .. py:method:: _load(self)



