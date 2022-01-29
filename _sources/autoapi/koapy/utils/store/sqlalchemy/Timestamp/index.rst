:py:mod:`koapy.utils.store.sqlalchemy.Timestamp`
================================================

.. py:module:: koapy.utils.store.sqlalchemy.Timestamp


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.utils.store.sqlalchemy.Timestamp.Timestamp




.. py:class:: Timestamp(*args, **kwargs)

   Bases: :py:obj:`sqlalchemy.types.TypeDecorator`

   Allows the creation of types which add additional functionality
   to an existing type.

   This method is preferred to direct subclassing of SQLAlchemy's
   built-in types as it ensures that all required functionality of
   the underlying type is kept in place.

   Typical usage::

     import sqlalchemy.types as types

     class MyType(types.TypeDecorator):
         '''Prefixes Unicode values with "PREFIX:" on the way in and
         strips it off on the way out.
         '''

         impl = types.Unicode

         cache_ok = True

         def process_bind_param(self, value, dialect):
             return "PREFIX:" + value

         def process_result_value(self, value, dialect):
             return value[7:]

         def copy(self, **kw):
             return MyType(self.impl.length)

   The class-level ``impl`` attribute is required, and can reference any
   :class:`.TypeEngine` class.  Alternatively, the :meth:`load_dialect_impl`
   method can be used to provide different type classes based on the dialect
   given; in this case, the ``impl`` variable can reference
   ``TypeEngine`` as a placeholder.

   The :attr:`.TypeDecorator.cache_ok` class-level flag indicates if this
   custom :class:`.TypeDecorator` is safe to be used as part of a cache key.
   This flag defaults to ``None`` which will initially generate a warning
   when the SQL compiler attempts to generate a cache key for a statement
   that uses this type.  If the :class:`.TypeDecorator` is not guaranteed
   to produce the same bind/result behavior and SQL generation
   every time, this flag should be set to ``False``; otherwise if the
   class produces the same behavior each time, it may be set to ``True``.
   See :attr:`.TypeDecorator.cache_ok` for further notes on how this works.

   Types that receive a Python type that isn't similar to the ultimate type
   used may want to define the :meth:`TypeDecorator.coerce_compared_value`
   method. This is used to give the expression system a hint when coercing
   Python objects into bind parameters within expressions. Consider this
   expression::

       mytable.c.somecol + datetime.date(2009, 5, 15)

   Above, if "somecol" is an ``Integer`` variant, it makes sense that
   we're doing date arithmetic, where above is usually interpreted
   by databases as adding a number of days to the given date.
   The expression system does the right thing by not attempting to
   coerce the "date()" value into an integer-oriented bind parameter.

   However, in the case of ``TypeDecorator``, we are usually changing an
   incoming Python type to something new - ``TypeDecorator`` by default will
   "coerce" the non-typed side to be the same type as itself. Such as below,
   we define an "epoch" type that stores a date value as an integer::

       class MyEpochType(types.TypeDecorator):
           impl = types.Integer

           epoch = datetime.date(1970, 1, 1)

           def process_bind_param(self, value, dialect):
               return (value - self.epoch).days

           def process_result_value(self, value, dialect):
               return self.epoch + timedelta(days=value)

   Our expression of ``somecol + date`` with the above type will coerce the
   "date" on the right side to also be treated as ``MyEpochType``.

   This behavior can be overridden via the
   :meth:`~TypeDecorator.coerce_compared_value` method, which returns a type
   that should be used for the value of the expression. Below we set it such
   that an integer value will be treated as an ``Integer``, and any other
   value is assumed to be a date and will be treated as a ``MyEpochType``::

       def coerce_compared_value(self, op, value):
           if isinstance(value, int):
               return Integer()
           else:
               return self

   .. warning::

      Note that the **behavior of coerce_compared_value is not inherited
      by default from that of the base type**.
      If the :class:`.TypeDecorator` is augmenting a
      type that requires special logic for certain types of operators,
      this method **must** be overridden.  A key example is when decorating
      the :class:`_postgresql.JSON` and :class:`_postgresql.JSONB` types;
      the default rules of :meth:`.TypeEngine.coerce_compared_value` should
      be used in order to deal with operators like index operations::

           class MyJsonType(TypeDecorator):
               impl = postgresql.JSON

               cache_ok = True

               def coerce_compared_value(self, op, value):
                   return self.impl.coerce_compared_value(op, value)

      Without the above step, index operations such as ``mycol['foo']``
      will cause the index value ``'foo'`` to be JSON encoded.


   .. py:attribute:: impl
      

      

   .. py:attribute:: cache_ok
      :annotation: = True

      

   .. py:attribute:: signature
      

      

   .. py:attribute:: utc
      

      

   .. py:attribute:: local_timezone
      

      

   .. py:method:: is_naive(cls, value)
      :classmethod:


   .. py:method:: process_bind_param(self, value, dialect)

      Receive a bound parameter value to be converted.

      Custom subclasses of :class:`_types.TypeDecorator` should override
      this method to provide custom behaviors for incoming data values.
      This method is called at **statement execution time** and is passed
      the literal Python data value which is to be associated with a bound
      parameter in the statement.

      The operation could be anything desired to perform custom
      behavior, such as transforming or serializing data.
      This could also be used as a hook for validating logic.

      :param value: Data to operate upon, of any type expected by
       this method in the subclass.  Can be ``None``.
      :param dialect: the :class:`.Dialect` in use.

      .. seealso::

          :ref:`types_typedecorator`

          :meth:`_types.TypeDecorator.process_result_value`



   .. py:method:: process_result_value(self, value, dialect)

      Receive a result-row column value to be converted.

      Custom subclasses of :class:`_types.TypeDecorator` should override
      this method to provide custom behaviors for data values
      being received in result rows coming from the database.
      This method is called at **result fetching time** and is passed
      the literal Python data value that's extracted from a database result
      row.

      The operation could be anything desired to perform custom
      behavior, such as transforming or deserializing data.

      :param value: Data to operate upon, of any type expected by
       this method in the subclass.  Can be ``None``.
      :param dialect: the :class:`.Dialect` in use.

      .. seealso::

          :ref:`types_typedecorator`

          :meth:`_types.TypeDecorator.process_bind_param`





