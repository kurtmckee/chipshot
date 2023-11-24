# This file is a part of Chipshot <https://github.com/kurtmckee/chipshot>
# Copyright 2022-2023 Kurt McKee <contactme@kurtmckee.org>
# SPDX-License-Identifier: MIT

import logging


def setup(*, enable_debug: bool) -> None:
    log_level = logging.DEBUG if enable_debug else logging.INFO
    log = logging.getLogger("chipshot")
    log.setLevel(log_level)
    log.propagate = True

    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)

    log.addHandler(console_handler)
