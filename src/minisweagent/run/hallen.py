"""Headless JSON entrypoint.

Everything is explicit: task file, model, working directory, limits, output paths.
Nothing is read from ambient configuration except provider credentials.
"""

from __future__ import annotations

import json
from pathlib import Path

import typer

from minisweagent.environments.local import LocalEnvironment
from minisweagent.run.prompt import run_prompt


def main(
    task_file: Path = typer.Option(..., "--task-file", exists=True, dir_okay=False),
    model: str = typer.Option(..., "--model", help="litellm model, e.g. nvidia_nim/meta/llama-3.3-70b-instruct"),
    cwd: Path = typer.Option(Path("."), "--cwd", help="Workspace root where the agent runs"),
    result: Path | None = typer.Option(None, "--result", help="Write the JSON result here"),
    trajectory: Path | None = typer.Option(None, "--trajectory", help="Write the trajectory here"),
    step_limit: int = typer.Option(200, "--step-limit", min=0),
    wall_time_limit: int = typer.Option(3600, "--wall-time-limit", min=0),
    max_format_errors: int = typer.Option(3, "--max-format-errors", min=0),
    cost_limit: float = typer.Option(0.0, "--cost-limit", min=0.0),
) -> None:
    if not model.strip():
        raise typer.BadParameter("a model is required")

    info = run_prompt(
        task_file.read_text(encoding="utf-8"),
        model_name=model,
        env=LocalEnvironment(cwd=str(cwd.resolve())),
        output_path=trajectory,
        step_limit=step_limit,
        wall_time_limit_seconds=wall_time_limit,
        max_consecutive_format_errors=max_format_errors,
        cost_limit=cost_limit,
    )
    payload = {
        "success": bool(info.get("success")),
        "exit_status": info.get("exit_status", ""),
        "submission": info.get("submission", ""),
        "cost": info.get("cost", 0.0),
        "n_calls": info.get("n_calls", 0),
        "trajectory_path": info.get("trajectory_path") or "",
        "cwd": str(cwd.resolve()),
        "model": model,
    }
    if result:
        result.parent.mkdir(parents=True, exist_ok=True)
        result.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    typer.echo(json.dumps(payload))


if __name__ == "__main__":
    typer.run(main)
