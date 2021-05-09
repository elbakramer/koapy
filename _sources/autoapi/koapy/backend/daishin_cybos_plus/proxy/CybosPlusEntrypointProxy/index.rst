:mod:`koapy.backend.daishin_cybos_plus.proxy.CybosPlusEntrypointProxy`
======================================================================

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




.. class:: CybosPlusDispatchProxyMethod(proxy, name)


   .. method:: __call__(self, *args, **kwargs)



.. class:: CybosPlusDispatchProxy(proxy, progid)


   Bases: :py:obj:`koapy.utils.logging.Logging.Logging`

   .. method:: _GetProperty(self, name)


   .. method:: _InvokeMethod(self, name, args)


   .. method:: __getattr__(self, name)



.. class:: CybosPlusIncompleteProgIDProxy(proxy, prefix)


   .. method:: __getattr__(self, name)



.. class:: CybosPlusEntrypointProxy(host=None, port=None)


   Bases: :py:obj:`koapy.backend.daishin_cybos_plus.core.CybosPlusEntrypointMixin.CybosPlusEntrypointMixin`

   .. method:: __getattr__(self, name)



