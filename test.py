from curionet import network

class ExampleHandler(network.NetworkHandler):
    """
    An example connection handler derived from NetworkHandler
    """

    async def handle_connected(self):
        print ('Connected.')

    async def handle_received(self, data):
        print ('Data recieved from %s: %r!' % (self.address, data))

    async def handle_disconnected(self):
        print ('Disconnected.')

if __name__ == '__main__':
    factory = network.NetworkFactory('0.0.0.0', 8080, ExampleHandler)
    factory.run()
