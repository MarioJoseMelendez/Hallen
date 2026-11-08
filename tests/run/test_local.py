import re

from minisweagent.agents import get_agent
from minisweagent.config import builtin_config_dir, get_config_from_spec
from minisweagent.environments.local import LocalEnvironment
from minisweagent.models.test_models import DeterministicModel, make_output
from tests.conftest import assert_observations_match


def _make_model_from_fixture(text_outputs: list[str], cost_per_call: float = 1.0, **kwargs) -> DeterministicModel:
    """Create a DeterministicModel from trajectory fixture data (raw text outputs)."""

    def parse_command(text: str) -> list[dict]:
        match = re.search(r"```mswea_bash_command\s*\n(.*?)\n```", text, re.DOTALL)
        return [{"command": match.group(1)}] if match else []

    return DeterministicModel(
        outputs=[make_output(text, parse_command(text), cost=cost_per_call) for text in text_outputs],
        cost_per_call=cost_per_call,
        **kwargs,
    )


def test_local_end_to_end(local_test_data):
    """Test the complete flow from config to final result using a real environment but deterministic model"""

    model_responses = local_test_data["model_responses"]
    expected_observations = local_test_data["expected_observations"]

    agent = get_agent(
        _make_model_from_fixture(model_responses),
        LocalEnvironment(),
        {**get_config_from_spec(builtin_config_dir / "mini.yaml")["agent"], "cost_limit": 10},
        default_type="default",
    )
    agent.run("Blah blah blah")

    messages = agent.messages

    # Verify we have the right number of messages
    # Should be: system + user (initial) + (assistant + user) * number_of_steps
    expected_total_messages = 2 + (len(model_responses) * 2)
    assert len(messages) == expected_total_messages, f"Expected {expected_total_messages} messages, got {len(messages)}"

    assert_observations_match(expected_observations, messages)

    assert agent.n_calls == len(model_responses), f"Expected {len(model_responses)} steps, got {agent.n_calls}"
