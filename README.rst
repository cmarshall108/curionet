Curionet
========

An asynchronous high-level networking framework built on top of the Curio library.

Example
-------

A simple tcp server example

.. code:: python

  from curionet import network

  class ExampleHandler(network.NetworkHandler):
      """
      An example connection handler derived from NetworkHandler
      """

      async def handle_connected(self):
          print ('Connected.')

      async def handle_received(self, data):
          print ('Data recieved from (%s: %r)!' % (self.address, data))

      async def handle_disconnected(self):
          print ('Disconnected.')

  if __name__ == '__main__':
      factory = network.NetworkFactory('0.0.0.0', 8080, ExampleHandler)
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
