# Remote HPC Example

Execute FZ calculations on HPC clusters via SSH.

## Example

```python
import fz

results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators="ssh://user@cluster.edu/bash /path/to/script.sh",
    results_dir="hpc_results"
)
```

See the [main FZ documentation](https://github.com/Funz/fz) for complete details.
