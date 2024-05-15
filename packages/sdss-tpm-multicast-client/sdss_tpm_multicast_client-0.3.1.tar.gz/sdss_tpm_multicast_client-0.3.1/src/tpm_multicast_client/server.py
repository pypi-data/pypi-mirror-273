#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2024-05-14
# @Filename: server.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import asyncio
from functools import partial

from tpm_multicast_client import log
from tpm_multicast_client.client import TPMClient


async def handle_connection(
    client: TPMClient,
    interval: float,
    _: asyncio.StreamReader,
    writer: asyncio.StreamWriter,
):
    """Handles a connection to the TPM server."""

    while True:
        try:
            if client.data is not None:
                writer.write((str(client.data) + "\n").encode())
                await writer.drain()
        except (ConnectionResetError, BrokenPipeError):
            break
        except Exception as ee:
            log.warning(f"Error writing to client: {ee}")
            writer.close()
            await writer.wait_closed()
            break

        await asyncio.sleep(interval)


async def tpm_server(port: int = 19991, interval: float = 1.0):
    """Creates a server that reports the TPM data every ``interval`` seconds.

    The output is a binary string delimited by a new line,
    that can be evaluated into a dictionary.

    """

    client = TPMClient()
    asyncio.create_task(client.listen())

    handle_connection_partial = partial(handle_connection, client, interval)

    server = await asyncio.start_server(handle_connection_partial, "0.0.0.0", port)

    await server.serve_forever()
