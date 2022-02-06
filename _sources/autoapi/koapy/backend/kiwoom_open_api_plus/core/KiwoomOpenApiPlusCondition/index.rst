:py:mod:`koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusCondition`
============================================================================

.. py:module:: koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusCondition


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusCondition.KiwoomOpenApiPlusConditionEntry
   koapy.backend.kiwoom_open_api_plus.core.KiwoomOpenApiPlusCondition.KiwoomOpenApiPlusConditionFile




.. py:class:: KiwoomOpenApiPlusConditionEntry(header, item_id, group_id, group_name, group_tp, name, group_id_small, order_no, type_position, upjong, portfolio, recommend, acc, group, excepts, month, exp, count, rules)

   .. py:method:: from_datfile(cls, f: TextIO)
      :classmethod:



.. py:class:: KiwoomOpenApiPlusConditionFile(version: str, entries: Sequence[KiwoomOpenApiPlusConditionEntry])

   .. py:method:: from_datfile(cls, f: Union[str, os.PathLike, TextIO], encoding: Optional[str] = None)
      :classmethod:



