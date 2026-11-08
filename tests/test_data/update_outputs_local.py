#!/usr/bin/env python3

import json
import re
from pathlib import Path

from minisweagent.agents import get_agent
from minisweagent.config import builtin_config_dir, get_config_from_spec
from minisweagent.environments.local import LocalEnvironment
from minisweagent.models.test_models import DeterministicModel, make_output


def update_trajectory():
    traj_path = Path(__file__).parent / "local.traj.json"
    trajectory = json.loads(traj_path.read_text())

    def parse_command(text: str) -> list[dict]:
        match = re.search(r"```mswea_bash_command\s*\n(.*?)\n```", text, re.DOTALL)
        return [{"command": match.group(1)}] if match else []

    model_responses = [msg["content"] for msg in trajectory[2:] if msg["role"] == "assistant"]
    print(f"Got {len(model_responses)} model responses")

    agent = get_agent(
        DeterministicModel(outputs=[make_output(text, parse_command(text)) for text in model_responses]),
        LocalEnvironment(),
        {**get_config_from_spec(builtin_config_dir / "mini.yaml")["agent"], "output_path": traj_path},
        default_type="default",
    )
    agent.run("Blah blah blah")


if __name__ == "__main__":
    update_trajectory()
