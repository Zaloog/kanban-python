import argparse

from kanban_python import __version__
from kanban_python.constants import REPORT_FILE_PATH


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Usage Options")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"kanban-python {__version__}",
    )

    command_parser = parser.add_subparsers(
        title="commands", dest="command", description="available commands"
    )

    # Init
    init_parser = command_parser.add_parser(
        "init",
        help="initialize a new board, use `--local`-flag to create in current working directory",
    )
    init_parser.add_argument(
        "-l",
        "--local",
        help="create a local board in the current working directory, default:False",
        action="store_true",
    )

    # Configure
    command_parser.add_parser("configure", help="configure settings")

    # Scan
    scan_parser = command_parser.add_parser(
        "scan", help="scan path for TODOs in files (default: `.`)"
    )
    scan_parser.add_argument(
        "-p", "--path", required=False, help="path to scan (default: `.`)", default="."
    )

    # Report
    report_parser = command_parser.add_parser(
        "report", help=f"create report in output path (default: {REPORT_FILE_PATH})"
    )
    report_parser.add_argument(
        "-p",
        "--path",
        required=False,
        help=f"path to save output to (default: {REPORT_FILE_PATH})",
        default=REPORT_FILE_PATH,
    )

    return parser.parse_args(args)
