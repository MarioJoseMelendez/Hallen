"""Start the agent loop from a single prompt."""

from pathlib import Path

from minisweagent import Environment, Model
from minisweagent.agents import get_agent
from minisweagent.config import get_config_from_spec
from minisweagent.environments import get_environment
from minisweagent.models import get_model
from minisweagent.utils.serialize import UNSET, recursive_merge


def run_prompt(
    prompt: str,
    *,
    model: Model | None = None,
    env: Environment | None = None,
    config_spec: str | list[str] = "mini",
    model_name: str | None = None,
    model_class: str | None = None,
    environment_class: str | None = None,
    output_path: Path | None = None,
    **agent_config,
) -> dict:
    """Run the agent loop on one prompt and return its result.

    The returned dictionary has a ``success`` key. It is True when the agent
    finished by submitting its output and False for any other exit status, such
    as a cost limit or a repeated format error. The result also carries the exit
    status, the submission, the cost, the number of model calls and the path of
    the saved trajectory.
    """
    specs = [config_spec] if isinstance(config_spec, str) else config_spec
    config = recursive_merge(
        *(get_config_from_spec(spec) for spec in specs),
        {
            "agent": {"output_path": output_path or UNSET, **agent_config},
            "model": {"model_name": model_name or UNSET, "model_class": model_class or UNSET},
            "environment": {"environment_class": environment_class or UNSET},
        },
    )
    agent = get_agent(
        model or get_model(config=config.get("model", {})),
        env or get_environment(config.get("environment", {}), default_type="local"),
        config.get("agent", {}),
        default_type="default",
    )
    info = agent.run(prompt)
    return {
        **info,
        "success": info.get("success", info.get("exit_status") == "Submitted"),
        "cost": agent.cost,
        "n_calls": agent.n_calls,
        "trajectory_path": str(agent.config.output_path) if agent.config.output_path else None,
    }
