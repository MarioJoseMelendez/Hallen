# Global configuration

!!! abstract "Configuring mini"

    * This guide shows how to configure the `mini` agent's global settings (API keys, default model, etc.).
      Basically anything that is set as environment variables or similar.
    * You should already be familiar with the [quickstart guide](../quickstart.md).
    * For more agent specific settings, see the [yaml configuration file guide](yaml_configuration.md).

!!! tip "Setting up models"

    Setting up models is also covered in the [quickstart guide](../quickstart.md).

## Setting global configuration

All global configuration can be either set as environment variables, or in the `.env` file inside the global config directory (`minisweagent.global_config_file`).
Environment variables take precedence over variables set in the `.env` file.

To set the default model and API keys, edit the `.env` file:

```bash
MSWEA_MODEL_NAME="anthropic/claude-sonnet-4-5-20250929"
ANTHROPIC_API_KEY="sk-..."
```

To set environment variables (recommended for temporary experimentation or API keys):

```bash
export KEY="value"
# windows:
setx KEY "value"
```

## Models, keys, costs

!!! tip "See also"

    Read the [quickstart guide](../quickstart.md) first—it already covers most of this.

```bash
# Default model name
# (default: not set)
MSWEA_MODEL_NAME="anthropic/claude-sonnet-4-5-20250929"
```

To ignore errors from cost tracking checks (for example for free models), set:

```bash
# CAREFUL: This can lead to unmanaged spending!
MSWEA_COST_TRACKING="ignore_errors"
```

To register extra models to litellm (see [local models](../models/local_models.md) for more details), you can either specify the path in the agent file, or set

```bash
LITELLM_MODEL_REGISTRY_PATH="/path/to/your/model/registry.json"
```

Global cost limits:

```bash
# Global limit on number of model calls (0 = no limit)
# (default: 0)
MSWEA_GLOBAL_CALL_LIMIT="100"

# Global cost limit in dollars (0 = no limit)
# (default: 0)
MSWEA_GLOBAL_COST_LIMIT="10.00"

# Number of retry attempts for model API calls
# (default: 10)
MSWEA_MODEL_RETRY_STOP_AFTER_ATTEMPT="10"
```

## Default config files

```bash
# Set a custom directory for agent config files in addition to the builtin ones
# This allows to specify them by names
MSWEA_CONFIG_DIR="/path/to/your/own/config/dir"
```

### Settings for environments

```bash
# Path/name to the singularity/apptainer executable
# (default: "singularity")
MSWEA_SINGULARITY_EXECUTABLE="singularity"

# Path/name to the docker executable
# (default: "docker")
MSWEA_DOCKER_EXECUTABLE="docker"

# Path/name to the bubblewrap executable
# (default: "bwrap")
MSWEA_BUBBLEWRAP_EXECUTABLE="bwrap"
```

{% include-markdown "_footer.md" %}
