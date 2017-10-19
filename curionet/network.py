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

    async def __update(self):
        try:
            data = await self.connection.recv(self.BUFFER_SIZE)
        except socket.error:
            return await self.handle_disconnect()

        if not data:
            return await self.handle_disconnect()

        await self.handle_received(data)

    async def handle_connect(self):
        await self.factory.add_handler(self)

        async with self.connection:
            while True:
                await self.__update()

    async def handle_connected(self):
        pass

    async def handle_send(self, data):
        try:
            await self.connection.sendall(data)
        except socket.error:
            return await self.handle_disconnect()

    async def handle_received(self, data):
        pass

    async def handle_disconnect(self):
        await self.connection.close()
        await self.factory.remove_handler(self)
        await self.handle_join()

    async def handle_disconnected(self):
        pass

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

    def __init__(self, address, port, handler, backlog=100):
        self.address = address
        self.port = port
        self.handler = handler
        self.backlog = backlog

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

        self.handlers = []

    def has_handler(self, handler):
        return handler in self.handlers

    async def add_handler(self, handler):
        if self.has_handler(handler):
            return

        self.handlers.append(handler)
        await handler.handle_connected()

    async def remove_handler(self, handler):
        if not self.has_handler(handler):
            return

        self.handlers.remove(handler)
        await handler.handle_disconnected()

    async def handle_start(self):
        pass

    async def __update(self):
        try:
            (connection, address) = await self.__socket.accept()
        except socket.error:
            raise NetworkFactoryError('An error occurred, when trying to accept an incoming connection!')

        handler = self.handler(self, connection, address)
        handler.task = await spawn(handler.handle_connect)

    async def execute(self):
        await self.handle_start()

        async with self.__socket:
            while True:
                await self.__update()

            await self.handle_disconnect()

    async def handle_send(self, data, exceptions=[]):
        for handler in self.handlers:

            if handler in exceptions:
                continue

            await handler.handle_send(data)

    async def handle_disconnect(self):
        await self.__socket.close()
        await self.handle_stop()

    async def handle_stop(self):
        pass

    def run(self):
        try:
            self.__socket.bind((self.address, self.port))
        except socket.error:
            raise NetworkFactoryError('Failed to bind socket on address (%s:%d)!' % (self.address,
                self.port))

        try:
            self.__socket.listen(self.backlog)
        except socket.error:
            raise NetworkFactoryError('Failed to listen on socket!')

        return run(self.execute)

class NetworkConnectorError(RuntimeError):
    """
    A network connector specific runtime error
    """

class NetworkConnector(object):
    """
    A connector instance that manages single a socket connection
    """

    BUFFER_SIZE = 1024

    def __init__(self, address, port):
        self.address = address
        self.port = port

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    async def __update(self):
        try:
            data = await self.__socket.recv(self.BUFFER_SIZE)
        except socket.error:
            return await self.handle_disconnect()

        if not data:
            return await self.handle_disconnect()

        await self.handle_received(data)

    async def handle_connected(self):
        pass

    async def handle_send(self, data):
        try:
            await self.__socket.sendall(data)
        except socket.error:
            return await self.handle_disconnect()

    async def handle_received(self, data):
        pass
    
    async def handle_disconnect(self):
        await self.__socket.close()
        await self.handle_disconnected()

    async def handle_disconnected(self):
        pass
    
    async def execute(self):
        try:
            await self.__socket.connect((self.address, self.port))
        except socket.error:
            raise NetworkConnectorError('Failed to connect to server at (%s:%d)!' % (self.address,
                self.port))
 
        await self.handle_connected()

        async with self.__socket:
            while True:
                await self.__update()
    
    def run(self):
        return run(self.execute)
