from __future__ import annotations

import argparse
from pathlib import Path

from dm_lab.config import load_config
from dm_lab.pipeline import run_all_tasks

VALID_TASKS = ["classification", "clustering", "association", "anomaly"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dm-lab", description="Run DM-Lab benchmark tasks")
    sub = parser.add_subparsers(dest="command")

    run = sub.add_parser("run", help="Run benchmark tasks")
    run.add_argument("--config", default="configs/default.yaml", help="Path to YAML config")
    run.add_argument("--output-dir", default=None, help="Artifact output directory")
    run.add_argument(
        "--task",
        action="append",
        choices=VALID_TASKS + ["all"],
        default=None,
        help="Task(s) to run. Repeat for multiple tasks.",
    )
    run.add_argument("--seed", type=int, default=None, help="Override seed")
    run.add_argument("--quick", action="store_true", help="Force quick synthetic mode")

    return parser


def _resolve_tasks(task_args: list[str] | None, config_tasks: list[str]) -> list[str]:
    if not task_args:
        return config_tasks
    if "all" in task_args:
        return VALID_TASKS.copy()
    return task_args


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command != "run":
        parser.print_help()
        return 1

    cfg = load_config(args.config)
    seed = args.seed if args.seed is not None else cfg["seed"]
    output_dir = Path(args.output_dir or cfg.get("output_dir", "artifacts"))
    tasks = _resolve_tasks(args.task, cfg.get("tasks", VALID_TASKS))
    quick_mode = args.quick or bool(cfg.get("quick_mode", True))

    results = run_all_tasks(
        output_dir=output_dir,
        seed=seed,
        selected_tasks=tasks,
        quick=quick_mode,
    )

    print(f"Completed tasks: {', '.join(results.keys())}")
    print(f"Artifacts written to: {output_dir.resolve()}")
    return 0


def entrypoint() -> None:
    raise SystemExit(main())
