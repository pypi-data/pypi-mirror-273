#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2024-05-14
# @Filename: unpack.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import struct


# Structure of the data broadcast by the TPM. This is adapted from Jeff's
# C code in tpmtable.c.
# Columns are: name, count, size, type.
# The total length in bytes is count * size.

# NOTE: rot_velocity is an int64 here because that's necessary for the data
# to have the right format, but in tpmtable.c it's an int32. I'm not sure how
# that worked in the C code, I cannot find how those extra 4 bytes are being
# offset, except if for some reason that happens when one moves from int32 to float64,
# which doesn't make a lot of sense.
TPM_STRUCT = [
    ("magic", 24, 1, "CHARA"),
    ("mcp_vers", 24, 1, "CHARA"),
    ("plc_vers", 24, 1, "CHARA"),
    ("semaphore", 40, 1, "CHARA"),
    ("fid_vers", 24, 1, "CHARA"),
    ("ctime", 1, 8, "FLOAT64"),
    ("az_pos", 1, 4, "INT32"),
    ("az_actual_pos", 1, 4, "INT32"),
    ("az_actual_pos2", 1, 4, "INT32"),
    ("az_volts", 1, 4, "INT32"),
    ("az_volts2", 1, 4, "INT32"),
    ("az_velocity", 1, 4, "INT32"),
    ("az_amps", 1, 4, "INT32"),
    ("az_amps2", 1, 4, "INT32"),
    ("alt_pos", 1, 4, "INT32"),
    ("alt_actual_pos", 1, 4, "INT32"),
    ("alt_actual_pos2", 1, 4, "INT32"),
    ("alt_volts", 1, 4, "INT32"),
    ("alt_volts2", 1, 4, "INT32"),
    ("alt_amps", 1, 4, "INT32"),
    ("alt_amps2", 1, 4, "INT32"),
    ("alt_velocity", 1, 4, "INT32"),
    ("rot_pos", 1, 4, "INT32"),
    ("rot_actual_pos", 1, 4, "INT32"),
    ("rot_volts", 1, 4, "INT32"),
    ("rot_amps", 1, 4, "INT32"),
    ("rot_velocity", 1, 8, "INT64"),
    ("az_spt", 1, 8, "FLOAT64"),
    ("alt_spt", 1, 8, "FLOAT64"),
    ("rot_spt", 1, 8, "FLOAT64"),
    ("az_err", 1, 4, "INT32"),
    ("alt_err", 1, 4, "INT32"),
    ("rot_err", 1, 4, "INT32"),
    ("az_plc_volts", 1, 4, "FLOAT32"),
    ("az2_plc_volts", 1, 4, "FLOAT32"),
    ("alt_plc_volts", 1, 4, "FLOAT32"),
    ("alt2_plc_volts", 1, 4, "FLOAT32"),
    ("rot_plc_volts", 1, 4, "FLOAT32"),
    ("inclinometer", 1, 4, "FLOAT32"),
    ("axis_stat", 3, 4, "UINT32"),
    ("az_fid", 1, 4, "INT32"),
    ("alt_fid", 1, 4, "INT32"),
    ("rot_fid", 1, 4, "INT32"),
    ("az_fid_pos", 1, 4, "INT32"),
    ("alt_fid_pos", 1, 4, "INT32"),
    ("rot_fid_pos", 1, 4, "INT32"),
    ("sp1_door", 1, 4, "INT32"),
    ("sp2_door", 1, 4, "INT32"),
    ("inst_id", 3, 4, "INT32"),
    ("alt_servo", 1, 4, "FLOAT32"),
    ("alt_primary", 1, 4, "FLOAT32"),
    ("az_servo", 1, 4, "FLOAT32"),
    ("az_primary", 1, 4, "FLOAT32"),
    ("az_ff_drive", 1, 4, "FLOAT32"),
    ("lift_force", 1, 4, "FLOAT32"),
    ("lift_pos", 1, 4, "FLOAT32"),
    ("plc_cw", 4, 4, "FLOAT32"),
    ("plc_words", 192, 2, "UINT16"),
    ("tpm_vers", 24, 1, "CHARA"),
    ("az1_stat", 1, 4, "INT32"),
    ("az2_stat", 1, 4, "INT32"),
    ("alt1_stat", 1, 4, "INT32"),
    ("alt2_stat", 1, 4, "INT32"),
    ("rot_stat", 1, 4, "INT32"),
    ("slip_stat", 8, 4, "INT32"),
    ("m1_axial_a", 1, 4, "FLOAT32"),
    ("m1_axial_b", 1, 4, "FLOAT32"),
    ("m1_axial_c", 1, 4, "FLOAT32"),
    ("m1_transverse", 1, 4, "FLOAT32"),
    ("m1_lateral_e", 1, 4, "FLOAT32"),
    ("m1_lateral_f", 1, 4, "FLOAT32"),
    ("m1_mig_sevr", 1, 4, "INT32"),
    ("m2_axial_a", 1, 4, "FLOAT32"),
    ("m2_axial_b", 1, 4, "FLOAT32"),
    ("m2_axial_c", 1, 4, "FLOAT32"),
    ("m2_y", 1, 4, "FLOAT32"),
    ("m2_mig_sevr", 1, 4, "INT32"),
    ("dewar_sp1_lb", 1, 4, "FLOAT32"),
    ("dewar_sp2_lb", 1, 4, "FLOAT32"),
    ("dewar_sp1_psi", 1, 4, "FLOAT32"),
    ("dewar_sp2_psi", 1, 4, "FLOAT32"),
    ("sevr_sp1", 1, 4, "INT32"),
    ("sevr_sp2", 1, 4, "INT32"),
    ("pmss_pos", 4, 4, "FLOAT32"),
    ("pmss_pos_error", 4, 4, "FLOAT32"),
    ("pmss_press", 4, 4, "FLOAT32"),
    ("pmss_press_error", 4, 4, "FLOAT32"),
    ("DpTempA", 1, 4, "FLOAT32"),
    ("DpTempB", 1, 4, "FLOAT32"),
    ("DpDepMean", 1, 4, "FLOAT32"),
    ("sevr_humid", 1, 4, "INT32"),
    ("wind_speed", 1, 4, "FLOAT32"),
    ("wind_dir", 1, 4, "FLOAT32"),
    ("galil_m1_a", 6, 4, "INT32"),
    ("galil_m1_c", 6, 4, "INT32"),
    ("galil_m1_h", 6, 4, "INT32"),
    ("galil_m1_sevr", 1, 4, "INT32"),
    ("galil_m2_a", 5, 4, "INT32"),
    ("galil_m2_c", 5, 4, "INT32"),
    ("galil_m2_h", 5, 4, "INT32"),
    ("galil_m2_sevr", 1, 4, "INT32"),
    ("galil_m2_piezo_a", 1, 4, "INT32"),
    ("galil_m2_piezo_b", 1, 4, "INT32"),
    ("galil_m2_piezo_c", 1, 4, "INT32"),
    ("galil_m2_piezo_stat", 1, 4, "INT32"),
    ("therm0", 64, 4, "FLOAT32"),
    ("therm1", 64, 4, "FLOAT32"),
    ("therm2", 64, 4, "FLOAT32"),
    ("tmicro_sevr", 1, 4, "INT32"),
    ("cw_limits", 1, 4, "INT32"),
]


def unpack_tpm_data(data: bytes) -> dict[str, str | int | float]:
    """Unpacks the TPM data into a dictionary.

    This is a pure Python rewrite of Jeff Hagen's ``tpmdgram.c``.

    Parameters
    ----------
    data
        The data to unpack, as broadcast by the TPM.

    Returns
    -------
    dict
        A dictionary with the unpacked data, following the format in ``TPM_STRUCT``.

    """

    unpacked_data: dict[str, str | int | float] = {}

    offset = 0
    for entry in TPM_STRUCT:
        name = entry[0]
        count = entry[1]
        size = entry[2]
        dtype = entry[3]

        end = offset + count * size
        chunk = data[offset:end]

        if dtype == "CHARA":
            if size != 1:
                raise ValueError("CHARA type must have size=1.")
            value = struct.unpack(f"<{count}s", chunk)[0].strip(b"\x00").decode()
        elif dtype == "FLOAT32":
            value = struct.unpack(f"<{count}f", chunk)
        elif dtype == "FLOAT64":
            value = struct.unpack(f"{count}d", chunk)
        elif dtype == "INT32":
            value = struct.unpack(f"<{count}l", chunk)
        elif dtype == "INT64":
            value = struct.unpack(f"<{count}q", chunk)
        elif dtype == "UINT16":
            value = struct.unpack(f"<{count}H", chunk)
        elif dtype == "UINT32":
            value = struct.unpack(f"<{count}I", chunk)
        else:
            raise ValueError(f"Unknown dtype {dtype}.")

        if isinstance(value, (tuple, list)):
            for ii in range(count):
                item_name = f"{name}_{ii}" if len(value) > 1 else name
                unpacked_data[item_name] = value[ii]
        else:
            unpacked_data[name] = value

        offset += count * size

    return unpacked_data
