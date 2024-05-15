#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-10-24
# @Filename: client.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)


import asyncio
import socket
import struct
import warnings

from typing import Awaitable, Callable

from tpm_multicast_client.unpack import unpack_tpm_data


CallbackType = Callable[[dict], None | Awaitable[None]]

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 2007
IS_ALL_GROUPS = True


def get_socket():
    """Configures the socket to listen to the TPM multicast."""

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if IS_ALL_GROUPS:
        # On this port, receives ALL multicast groups.
        sock.bind(("", MCAST_PORT))
    else:
        # On this port, listen ONLY to MCAST_GRP.
        sock.bind((MCAST_GRP, MCAST_PORT))

    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    return sock


class TPMClientProtocol(asyncio.DatagramProtocol):
    """Client protocol for the TPM datagram."""

    def __init__(self, callback: CallbackType, loop: asyncio.AbstractEventLoop):
        self.callback = callback
        self.loop = loop

        self.is_closed = asyncio.Future()

    def datagram_received(self, data, _):
        try:
            dd = unpack_tpm_data(data)
            if asyncio.iscoroutinefunction(self.callback):
                asyncio.create_task(self.callback(dd))
            else:
                self.loop.call_soon(self.callback, dd)
        except Exception as ee:
            warnings.warn(f"Failed decoding message from multicast: {ee}", UserWarning)

    def error_received(self, exc):
        warnings.warn(f"Error received: {exc}", UserWarning)

    def connection_lost(self, exc):
        warnings.warn("Socket closed, stop the event loop", UserWarning)

        self.is_closed.set_result(True)

    async def run_forever(self):
        """Runs until the connection is closed."""

        await self.is_closed


async def listen_to_multicast(callback: CallbackType):
    """Listens to the TPM multicast.

    Parameters
    ----------
    callback
        A callback to call with every new mesage from the TPM. The callback
        can be a function or a coroutine and must accept a single argument,
        the TPM data dictionary.

    Returns
    -------
    A tuple with the transport and the protocol, the output of
    ``create_datagram_endpoint``.

    """

    loop = asyncio.get_running_loop()

    return await loop.create_datagram_endpoint(
        lambda: TPMClientProtocol(callback, loop),
        sock=get_socket(),
    )


class TPMClient:
    """A singleton class that listens to the TPM multicast."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            new = super().__new__(cls)
            cls._instance = new
            return new

        return cls._instance

    def __init__(self):
        # Prevent setting the data attribute to None if this is a reinitialisation
        # of an instance that already existed.
        already_initialized = hasattr(self, "data")
        if already_initialized:
            return

        self.data: dict[str, int | float | str] | None = None

    async def update_data(self, new_data: dict[str, int | float | str]):
        """Updates the TPM data."""

        self.data = new_data

    async def listen(self):
        """Listens to the TPM multicast."""

        await listen_to_multicast(self.update_data)


async def test():
    """Simple test function."""

    async def printer(dd: dict):
        print(dd)

    await listen_to_multicast(printer)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(test())
