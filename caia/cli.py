#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import logging.config
import os
import sys
from datetime import datetime
from importlib import import_module
from pkgutil import iter_modules
from caia import commands, version
from caia.logging import DEFAULT_LOGGING_OPTIONS
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()
logger = logging.getLogger(__name__)

now = datetime.utcnow().strftime('%Y%m%d%H%M%S')


def main() -> None:
    """Parse args and handle options."""

    parser = argparse.ArgumentParser(
        prog='caia',
        description='Middleware tool for connecting Aleph and CaiaSoft'
    )

    parser.add_argument(
        '-V', '--version',
        help='Print version and exit.',
        action='version',
        version=version
    )

    parser.add_argument(
        '-v', '--verbose',
        help='increase the verbosity of the status output',
        action='store_true'
    )

    parser.add_argument(
        '-q', '--quiet',
        help='decrease the verbosity of the status output',
        action='store_true'
    )

    subparsers = parser.add_subparsers(title='commands')

    # load all defined subcommands from the caia.commands package
    command_modules = {}
    for finder, name, ispkg in iter_modules(commands.__path__):  # type: ignore[attr-defined]
        module = import_module(commands.__name__ + '.' + name)
        if hasattr(module, 'configure_cli'):
            module.configure_cli(subparsers)  # type: ignore[attr-defined]
            command_modules[name] = module

    # parse command line args
    args = parser.parse_args()

    # if no subcommand was selected, display the help
    if args.cmd_name is None:
        parser.print_help()
        sys.exit(0)

    logging_options: Dict[str, Any] = DEFAULT_LOGGING_OPTIONS

    # log file configuration
    log_dirname = os.getenv("LOG_DIR", default="")
    if not log_dirname:
        logger.error("The 'LOG_DIR' environment variable is not defined. Exiting")
        sys.exit(1)

    if not os.path.isdir(log_dirname):
        logger.debug(f"Creating log directory at {log_dirname}")
        os.makedirs(log_dirname)

    log_filename = 'caia.{0}.{1}.log'.format(args.cmd_name, now)
    logfile = os.path.join(log_dirname, log_filename)
    logging_options['handlers']['file']['filename'] = logfile

    # manipulate console verbosity
    if args.verbose:
        logging_options['handlers']['console']['level'] = 'DEBUG'
    elif args.quiet:
        logging_options['handlers']['console']['level'] = 'WARNING'

    # configure logging
    logging.config.dictConfig(logging_options)

    # get the selected subcommand
    command = command_modules[args.cmd_name].Command()  # type: ignore[attr-defined]

    logger.info(f"Starting {args.cmd_name} at {now} with args: {args}")

    try:
        # dispatch to the selected subcommand
        print_header(args)
        # logger.info(f'Loaded repo configuration from {args.repo}')
        # if args.delegated_user is not None:
        #     logger.info(f'Running repository operations on behalf of {args.delegated_user}')
        result = command(now, args)

        if result.was_successful() is False:
            errors = result.errors
            if len(errors) > 0:
                print("The following errors occurred:")
                for error in errors:
                    print(f"\t{error}")

            sys.exit(1)

        print_footer(args)
    except KeyboardInterrupt:
        # aborted due to Ctrl+C
        sys.exit(2)
    except Exception as ex:
        # something failed, exit with non-zero status
        logger.exception(ex)
        sys.exit(1)


def print_header(args: argparse.Namespace) -> None:
    """Common header formatting."""
    if not args.quiet:
        title = '|       CAIA       |'
        bar = '+' + '=' * (len(title) - 2) + '+'
        spacer = '|' + ' ' * (len(title) - 2) + '|'
        print('\n'.join(['', bar, spacer, title, spacer, bar, '']), file=sys.stderr)


def print_footer(args: argparse.Namespace) -> None:
    """Report success or failure and resources created."""
    if not args.quiet:
        print('\nScript complete. Goodbye!\n', file=sys.stderr)


if __name__ == "__main__":
    main()
