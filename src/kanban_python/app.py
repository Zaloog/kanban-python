import sys
from pathlib import Path

from kanban_python import cli_parser, config, controls, utils, constants

__author__ = "Zaloog"
__copyright__ = "Zaloog"
__license__ = "MIT"


def main(args):
    args = cli_parser.parse_args(args)

    if not config.check_config_exists():
        config.create_init_config()
        return

    # Delete Local Entry if no local file present
    if (not Path("pykanban.json").exists()) and ("local" in config.cfg.kanban_boards):
        config.delete_board_from_config(board_name="local")

    # New database creation
    if args.command == "init":
        utils.console.print("Starting new [blue]Kanban Board[/]:mechanical_arm:")
        controls.create_new_db(local=args.local)

    if args.command == "configure":
        controls.change_settings()
        utils.console.clear()

    if args.command == "scan":
        controls.add_todos_to_board(path=Path(args.path) or Path.cwd())

    if args.command == "report":
        controls.create_report(
            output_path=Path(args.path) or constants.REPORT_FILE_PATH
        )
        return

    while True:
        controls.show()
        user_input = controls.get_user_action()

        if user_input == 1:
            controls.add_new_task_to_db()
            utils.console.clear()
        elif user_input == 2:
            controls.update_task_from_db()
            utils.console.clear()
        elif user_input == 3:
            controls.change_kanban_board()
            utils.console.clear()
        elif user_input == 4:
            controls.show_tasks()
        elif user_input == 5:
            controls.delete_kanban_board()
            utils.console.clear()
        elif user_input == 6:
            controls.change_settings()
            utils.console.clear()


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    try:
        main(sys.argv[1:])
    except (KeyboardInterrupt, EOFError):
        utils.console.print(utils.get_motivational_quote())


if __name__ == "__main__":
    run()
