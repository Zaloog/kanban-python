"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = kanban_python.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import sys

from kanban_python import cli_parser, config, controls, utils

__author__ = "Zaloog"
__copyright__ = "Zaloog"
__license__ = "MIT"


# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from kanban_python.skeleton import fib`,
# when using this Python module as a library.


def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for _i in range(n - 1):
        a, b = b, a + b
    return a


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def main(args):
    """Wrapper allowing :func:`fib` to be called with string arguments in a CLI fashion

    Instead of returning the value from :func:`fib`, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "42"]``).
    """
    args = cli_parser.parse_args(args)
    cli_parser.setup_logging(args.loglevel)

    if not config.check_config_exists():
        config.create_init_config()
        utils.console.print(
            "Welcome, I Created a new [orange3]pykanban.ini[/] file "
            + "located in the '.kanban-python' folder @Home Directory"
        )
        utils.console.print("Now use 'kanban init' to create kanban boards")
        return

    # New database creation
    if args.command == "init":
        utils.console.print("Starting new [blue]Kanban Board[/]:mechanical_arm:")
        controls.create_new_db()

    if args.command == "configure":
        controls.show_settings()
        return

    while True:
        controls.show()
        user_input = controls.get_user_action()

        if user_input == 1:
            controls.add_tasks_to_db()
        elif user_input == 2:
            controls.update_task_from_db()
        elif user_input == 3:
            controls.change_kanban_board()
        elif user_input == 4:
            controls.delete_kanban_board()
        elif user_input == 5:
            controls.show_settings()


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        utils.console.print(utils.get_motivational_quote())


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m kanban_python.skeleton 42
    #
    run()
