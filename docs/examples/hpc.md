# Remote HPC Example

Run a parametric study on an HPC cluster without leaving your Python script. FZ uploads
the compiled inputs, launches the job, downloads the results, and returns a DataFrame.

## Direct SSH

Each case runs immediately on the login/compute node the URI points at:

```python
import fz

model = {
    "varprefix": "$",
    "output": {"keff": "python://grep(r'k-eff = (\\S+)', 'out.txt')"},
}

results = fz.fzr(
    "reactor.inp",
    {"enrichment": [3.0, 4.0, 5.0], "radius": [8.5, 9.0]},
    model,
    calculators="ssh://user@cluster.edu/bash /scratch/user/run_case.sh",
    results_dir="hpc_results",
)
print(results[["enrichment", "radius", "keff", "status"]])
```

```bash title="/scratch/user/run_case.sh (on the cluster)"
#!/bin/bash
source reactor.inp
module load gcc/11.2 openmpi/4.1
mpirun -np 32 ./solver reactor.inp > out.txt
```

## Through SLURM

Submit each case as a SLURM job on a named partition (local cluster, or remote via SSH):

```python
results = fz.fzr(
    "reactor.inp",
    {"enrichment": [3.0, 4.0, 5.0]},
    model,
    calculators="slurm://user@cluster.edu:compute/bash /scratch/user/run_case.sh",
    results_dir="slurm_results",
)
```

See [SLURM Calculator](../user-guide/calculators/slurm.md) for partition syntax and
remote-vs-local rules.

## Parallelism, Failover, Caching

```python
results = fz.fzr(
    "reactor.inp",
    {"enrichment": [3.0, 3.5, 4.0, 4.5, 5.0]},
    model,
    calculators=[
        "cache://slurm_results",                              # reuse anything already done
        "slurm://user@cluster.edu:compute/bash run_case.sh",  # then submit
        "slurm://user@cluster.edu:compute/bash run_case.sh",  # 2 concurrent jobs
        "ssh://user@fallback.edu/bash /scratch/run_case.sh",  # last resort
    ],
    results_dir="slurm_results",
)
```

Shared, read-only inputs (a common cross-section library, a mesh) belong in
[`input_static`](../user-guide/core-functions/fzr.md#shared-static-files-new-in-12) —
give an **absolute path** when the file is already on the cluster's shared storage, so
FZ only hashes it rather than transferring a copy per case.

## Tips

- Use **absolute paths** in remote calculator commands.
- Set `FZ_SSH_KEEPALIVE=300` for long jobs; `FZ_RUN_TIMEOUT` bounds each case (default 1 h since 1.2).
- Test the script by hand first: `ssh user@host "bash /scratch/user/run_case.sh reactor.inp"`.
- **Ctrl+C** cancels submitted jobs and cleans up remote temp dirs; resume with a `cache://` entry.

## See Also

- [SSH Remote Calculator](../user-guide/calculators/ssh.md) · [SLURM Calculator](../user-guide/calculators/slurm.md)
- [Parallel Execution](../user-guide/advanced/parallel.md) · [Caching Strategy](../user-guide/advanced/caching.md)
