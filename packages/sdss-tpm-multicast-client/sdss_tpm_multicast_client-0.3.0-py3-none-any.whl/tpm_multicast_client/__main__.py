#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-10-22
# @Filename: __main__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

import sys
from pprint import pprint

import click

from sdsstools.daemonizer import cli_coro


def pprint_datagram(data: dict):
    """Prints the TPM data."""

    pprint(data)


@click.command()
@click.option(
    "--version",
    is_flag=True,
    help="Print version and exit.",
)
@click.option(
    "--serve",
    is_flag=True,
    help="Run as the TPM server.",
)
@click.option(
    "--port",
    type=int,
    default=19991,
    help="Port for the TPM server.",
)
@click.option(
    "--interval",
    type=float,
    default=1.0,
    help="Interval in which to output data to the TPM server, in seconds.",
)
@cli_coro()
async def tpm_multicast_client(
    version: bool = False,
    serve: bool = False,
    port: int = 19991,
    interval: float = 1.0,
):
    """TPM multicas client."""

    if version is True:
        from tpm_multicast_client import __version__

        click.echo(__version__)
        sys.exit(0)

    if serve is False:
        from tpm_multicast_client.client import listen_to_multicast

        _, protocol = await listen_to_multicast(pprint_datagram)
        await protocol.run_forever()

    else:
        from tpm_multicast_client.server import tpm_server

        click.echo(f"Serving TPM server on port {port}.")
        await tpm_server(port=port, interval=interval)


if __name__ == "__main__":
    tpm_multicast_client()
