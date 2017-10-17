"""
 * Copyright (C) Caleb Marshall and others... - All Rights Reserved
 * Written by Caleb Marshall <anythingtechpro@gmail.com>, May 23rd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
"""

from curionet import network

class ExampleConnector(network.NetworkConnector):
    """
    An example connector derived from NetworkConnector
    """

    async def handle_connected(self):
        print ('Connected.')

        # send the server some data...
        await self.handle_send('Hello World!')

    async def handle_received(self, data):
        print ('Data recieved from server (%s: %r)!' % (self.address, data))

    async def handle_disconnected(self):
        print ('Disconnected.')

if __name__ == '__main__':
    connector = ExampleConnector('127.0.0.1', 8080)
    connector.run()