:mod:`koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypoint`
================================================================

.. py:module:: koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypoint


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypoint.CybosPlusDispatch
   koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypoint.CybosPlusIncompleteProgID
   koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypoint.CybosPlusEntrypoint




.. class:: CybosPlusDispatch(entrypoint, progid)


   .. method:: __getattr__(self, name)


   .. method:: __repr__(self)

      Return repr(self).



.. class:: CybosPlusIncompleteProgID(entrypoint, prefix)


   .. method:: __getattr__(self, name)


   .. method:: __repr__(self)

      Return repr(self).



.. class:: CybosPlusEntrypoint


   Bases: :py:obj:`koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin.CybosPlusEntrypointMixin`

   http://cybosplus.github.io/

   .. method:: __getattr__(self, name)



