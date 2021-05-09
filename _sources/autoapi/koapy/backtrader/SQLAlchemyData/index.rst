:mod:`koapy.backtrader.SQLAlchemyData`
======================================

.. py:module:: koapy.backtrader.SQLAlchemyData


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backtrader.SQLAlchemyData.SQLAlchemyData




.. class:: SQLAlchemyData


   Bases: :py:obj:`backtrader.feed.DataBase`

   .. attribute:: params
      :annotation: = [['url', None], ['engine', None], ['connection', None], ['tablename', None], ['timestampcolumn',...

      

   .. method:: _dispose_engine(self)


   .. method:: _initialize_engine(self)


   .. method:: _close_cursor(self)


   .. method:: _initialize_cursor(self)


   .. method:: start(self)


   .. method:: stop(self)


   .. method:: _load(self)



