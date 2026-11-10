from minisweagent.environments.local import LocalEnvironment
from minisweagent.models.test_models import DeterministicModel, make_output
from minisweagent.run.prompt import run_prompt


def test_run_prompt_reports_success():
    model = DeterministicModel(
        outputs=[
            make_output("Echo", [{"command": "echo hello world"}], cost=0.1),
            make_output("Submit", [{"command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"}], cost=0.1),
        ]
    )

    result = run_prompt("Say hello and submit", model=model, env=LocalEnvironment(), cost_limit=10)

    assert result["success"] is True
    assert result["exit_status"] == "Submitted"
    assert result["n_calls"] == 2
    assert result["cost"] == 0.2


def test_run_prompt_reports_failure():
    model = DeterministicModel(outputs=[make_output("Echo", [{"command": "echo hello world"}], cost=1.0)])

    result = run_prompt("Loop", model=model, env=LocalEnvironment(), cost_limit=0.5)

    assert result["success"] is False
    assert result["exit_status"] == "LimitsExceeded"


def test_run_prompt_saves_trajectory(tmp_path):
    model = DeterministicModel(
        outputs=[make_output("Submit", [{"command": "echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT"}], cost=0.1)]
    )
    output_path = tmp_path / "trajectory.json"

    result = run_prompt("Submit", model=model, env=LocalEnvironment(), output_path=output_path)

    assert result["trajectory_path"] == str(output_path)
    assert output_path.exists()
