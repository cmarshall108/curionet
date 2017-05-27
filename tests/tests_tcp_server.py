"""
 * Copyright (C) Caleb Marshall and others... - All Rights Reserved
 * Written by Caleb Marshall <anythingtechpro@gmail.com>, May 23rd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
"""

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
