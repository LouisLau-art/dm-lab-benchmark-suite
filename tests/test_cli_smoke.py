from dm_lab.cli import build_parser


def test_cli_has_run_command() -> None:
    parser = build_parser()
    subcommands = parser._subparsers._group_actions[0].choices
    assert "run" in subcommands


def test_cli_accepts_full_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(["run", "--full"])
    assert args.full is True
