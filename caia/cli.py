#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config
import os
import sys

logger = logging.getLogger(__name__)


def main():
    """Parse args and handle options."""

    parser = argparse.ArgumentParser(
        prog='caia',
        description='Middleware tool for connecting Aleph and CaiaSoft'
    )

    parser.parse_args()


if __name__ == "__main__":
    main()
