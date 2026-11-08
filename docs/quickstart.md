# Quick start

Hallen is a library. Install it and call the agent from your own code.

```bash
pip install -e .
```

## Your first run

```python
from minisweagent.agents.default import DefaultAgent
from minisweagent.environments.local import LocalEnvironment
from minisweagent.models.litellm_model import LitellmModel

agent = DefaultAgent(
    LitellmModel(model_name="anthropic/claude-sonnet-4-5-20250929"),
    LocalEnvironment(),
)
agent.run("Implement a Sudoku solver in python in the `sudoku` folder.")
```

Pass `output_path` to the agent to save the trajectory as JSON.

## Models

Set your provider API key in the environment, for example `ANTHROPIC_API_KEY`. Hallen also reads keys from its global config file. See the [model setup quickstart](models/quickstart.md) and the [local models guide](models/local_models.md).

Always include the provider in the model name, e.g. `anthropic/claude-sonnet-4-5-20250929`.

## Development

```bash
pip install -e '.[dev]'
pip install pre-commit && pre-commit install
pytest -n auto
```

Some extra dependencies live in `.../extra/...` folders and are not installed by default. Install `.[full]` if you need them.

{% include-markdown "_footer.md" %}
