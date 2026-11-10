# Run scripts

Hallen is a library, so there is no human facing entry point. The scripts in this folder are called from your own code or with `python -m`.

## Agent

* `prompt.py` - `run_prompt(prompt)` builds the model, environment and agent, runs one task and returns the result with a `success` flag.

## Benchmarks

* `benchmarks/swebench.py` - Batch evaluation on SWE-bench.
* `benchmarks/swebench_single.py` - Evaluation on a single SWE-bench instance.
* `benchmarks/programbench.py` - Batch evaluation on ProgramBench.
