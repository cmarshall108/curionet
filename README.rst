Curionet
========

An asynchronous high-level networking framework built on top of the Curio library.

Example
-------

A simple tcp server example

.. code:: python

  from curionet.network import NetworkFactory, NetworkHandler

  class ExampleHandler(NetworkHandler):
      """
      An example connection handler derived from NetworkHandler
      """

      async def handle_connected(self):
          await super().handle_connected()

      async def handle_received(self, data):
          print ('Data recieved from %s: %r!' % (self.address, data))

      async def handle_closed(self):
          await super().handle_closed()

  if __name__ == '__main__':
      factory = NetworkFactory(8080, ExampleHandler)
      factory.run()

Other Resources
---------------

* `Curio <https://github.com/dabeaz/curio>`_, The asynchronous networking library written by David Beazley

Contributors
------------

- Caleb Marshall

About
-----

Curionet was inspired by the Twisted Matrix framework, and was implemented using the Curio library.
