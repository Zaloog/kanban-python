import sys

from kanban_python import cli_parser, config, controls, utils

__author__ = "Zaloog"
__copyright__ = "Zaloog"
__license__ = "MIT"


def main(args):
    args = cli_parser.parse_args(args)

    if not config.check_config_exists():
        config.create_init_config()
        return

    # New database creation
    if args.command == "init":
        utils.console.print("Starting new [blue]Kanban Board[/]:mechanical_arm:")
        # args.local
        controls.create_new_db(local=args.local)

    if args.command == "configure":
        controls.change_settings()

    if args.command == "scan":
        # args.path
        controls.add_todos_to_board()

    if args.command == "report":
        # args.path
        controls.create_report()
        return

    while True:
        controls.show()
        user_input = controls.get_user_action()

        if user_input == 1:
            controls.add_new_task_to_db()
        elif user_input == 2:
            controls.update_task_from_db()
        elif user_input == 3:
            controls.change_kanban_board()
        elif user_input == 4:
            controls.show_tasks()
        elif user_input == 5:
            controls.delete_kanban_board()
        elif user_input == 6:
            controls.change_settings()


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
