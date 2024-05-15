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

from tpm_multicast_client import __version__, listen_to_multicast


def pprint_datagram(data: dict):
    """Prints the TPM data."""

    pprint(data)


@click.command()
@click.option(
    "--version",
    is_flag=True,
    help="Print version and exit.",
)
@cli_coro()
async def tpm_multicast_client(version: bool = False):
    """TPM multicas client."""

    if version is True:
        click.echo(__version__)
        sys.exit(0)

    _, protocol = await listen_to_multicast(pprint_datagram)
    await protocol.run_forever()


if __name__ == "__main__":
    tpm_multicast_client()
