#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2023-10-24
# @Filename: __init__.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from sdsstools import get_package_version


NAME = "sdss-tpm-multicast-client"


__version__ = get_package_version(path=__file__, package_name=NAME)


from .client import listen_to_multicast
from .unpack import unpack_tpm_data
