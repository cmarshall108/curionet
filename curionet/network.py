"""
 * Copyright (C) Caleb Marshall and others... - All Rights Reserved
 * Written by Caleb Marshall <anythingtechpro@gmail.com>, May 23rd, 2017
 * Licensing information can found in 'LICENSE', which is part of this source code package.
"""

from curio import socket, run, spawn

class NetworkHandlerError(RuntimeError):
    """
    A network handler specific runtime error
    """

class NetworkHandler(object):
    """
    A handler instance which streams connection-orientated protocols
    """

    BUFFER_SIZE = 1024

    def __init__(self, factory, connection, address):
        self.factory = factory
        self.connection = connection
        self.address = address
        self.task = None

    async def handle_connected(self):
        self.factory.add_handler(self)

    async def execute(self):
        await self.handle_connected()

        async with self.connection:
            while True:
                try:
                    data = await self.connection.recv(self.BUFFER_SIZE)
                except socket.error:
                    break

                if not data:
                    break

                await self.handle_received(data)

            await self.handle_close()

        await self.handle_join()

    async def handle_received(self, data):
        pass

    async def handle_send(self, data):
        try:
            await self.connection.sendall(data)
        except socket.error:
            await self.handle_close()

    async def handle_close(self):
        try:
            await self.connection.close()
        finally:
            await self.handle_closed()

    async def handle_closed(self):
        self.factory.remove_handler(self)

    async def handle_join(self):
        if not self.task:
            return

        await self.task.join()

class NetworkFactoryError(RuntimeError):
    """
    A network factory specific runtime error
    """

class NetworkFactory(object):
    """
    A factory instance which manages connection handlers
    """

    REUSE_ADDRESS = True
    ADDRESS = '0.0.0.0'
    BACKLOG = 10000
    TIMEOUT = 0

    def __init__(self, port, handler):
        self.address = self.ADDRESS
        self.port = port
        self.handler = handler

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.REUSE_ADDRESS:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        if self.TIMEOUT:
            self.socket.settimeout(self.TIMEOUT)

        self.handlers = []

    def has_handler(self, handler):
        return handler in self.handlers

    def add_handler(self, handler):
        if self.has_handler(handler):
            return

        self.handlers.append(handler)

    def remove_handler(self, handler):
        if not self.has_handler(handler):
            return

        self.handlers.remove(handler)

    async def execute(self):
        async with self.socket:
            while True:
                (connection, address) = await self.socket.accept()

                if self.TIMEOUT:
                    connection.settimeout(self.TIMEOUT)

                # create a new instance of the protocol handler
                handler = self.handler(self, connection, address)

                # spawn the instance main loop on the curio task manager
                handler.task = await spawn(handler.execute)

            await self.handle_close()

    async def handle_send(self, data, exceptions=[]):
        for handler in self.handlers:

            if handler in exceptions:
                continue

            await handler.handle_send(data)

    async def handle_close(self):
        try:
            await self.socket.close()
        finally:
            await self.handle_closed()

    async def handle_closed(self):
        pass

    def run(self):
        try:
            self.socket.bind((self.address, self.port))
        except socket.error:
            raise NetworkFactoryError('Failed to bind socket on address %s:%d!' % (self.address,
                self.port))
        finally:
            self.socket.listen(self.BACKLOG)

        # run the main loop, on the curio task manager
        run(self.execute)
