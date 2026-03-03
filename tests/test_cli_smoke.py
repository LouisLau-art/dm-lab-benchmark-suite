from dm_lab.cli import build_parser


def test_cli_has_run_command() -> None:
    parser = build_parser()
    subcommands = parser._subparsers._group_actions[0].choices
    assert "run" in subcommands
