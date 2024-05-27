# Copyright (C) 2022 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause

"""
Module to generate dataset for Predictive Asset Maintenance
"""

# !/usr/bin/env python
# coding: utf-8
from argparse import ArgumentParser
from os import getenv

from requests import get

from app.__init__ import getLogger

url_base = getenv("APP_URL_BASE")
headers = {"Content-Type": "application/json"}


if __name__ == "__main__":
    logger = getLogger(__name__)

    parser = ArgumentParser()
    parser.add_argument("--ping", action="store_true", help="Ping the server")
    parser.add_argument(
        "--generate", action="store_true", required=False, help="generate data"
    )
    parser.add_argument(
        "-s", "--size", type=int, required=False, default=25000, help="data size"
    )
    FLAGS = parser.parse_args()

    if FLAGS.ping:
        response = get(f"{url_base}/ping")
        if response.status_code == 200:
            print("Server is Running")
        else:
            print("Server is not Running")
    else:
        raise ValueError(f"No valid arguments passed | {parser.print_help()}")
