:py:mod:`koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy`
=========================================================================

.. py:module:: koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy


Module Contents
---------------

Classes
~~~~~~~

.. autoapisummary::

   koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy.CybosPlusDispatchProxyMethod
   koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy.CybosPlusDispatchProxy
   koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy.CybosPlusIncompleteProgIDProxy
   koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy.CybosPlusEntrypointProxy




.. py:class:: CybosPlusDispatchProxyMethod(proxy, name)

   .. py:method:: __call__(self, *args, **kwargs)



.. py:class:: CybosPlusDispatchProxy(proxy, progid)

   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. py:method:: _GetProperty(self, name)


   .. py:method:: _InvokeMethod(self, name, args)


   .. py:method:: __getattr__(self, name)



.. py:class:: CybosPlusIncompleteProgIDProxy(proxy, prefix)

   .. py:method:: __getattr__(self, name)



.. py:class:: CybosPlusEntrypointProxy(host=None, port=None)

   Bases: :py:obj:`koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin.CybosPlusEntrypointMixin`

   .. py:method:: __getattr__(self, name)



