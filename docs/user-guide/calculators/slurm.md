# SLURM (`slurm://`, `slurm-array://`)

Two schemes submit cases to a SLURM cluster:

| | `slurm://` | `slurm-array://` |
|--|-----------|------------------|
| Submission | One blocking `srun` per case | One `sbatch --array` job for all cases submitted within a short window |
| Where fz runs | On a node with SLURM commands, or anywhere through SSH | On a node with `sbatch`/`sacct` (local only) |
| Parallel cases | One per calculator entry | All cases from one URI (optionally throttled) |
| Monitoring | `srun` returns when the job ends | One shared thread polls `sacct` (fallback `squeue`) |
| Default timeout | none | none |

## `slurm://`

```text
slurm://:partition/command                       # local SLURM
slurm://user@host:partition/command              # remote, through SSH
slurm://user@host:port:partition/command         # remote, custom SSH port
```

The partition is required and must be preceded by `:` (also in the local form).

```python
calculators = "slurm://:compute/bash /home/me/run.sh"
calculators = ["slurm://me@cluster.example.edu:compute/bash /home/me/run.sh"] * 8  # 8 jobs at a time
```

- Local: fz runs `srun --partition=<partition> [resources] <command> <input files>` in the
  case directory.
- Remote: fz connects by SSH (same authentication and host-key rules as
  [`ssh://`](ssh.md)), uploads the inputs by SFTP, runs `srun` there, downloads the
  results.
- Each entry runs one case at a time; repeat the URI to have several jobs in the queue.

## Job arrays (`slurm-array://`)

```python
calculators = "slurm-array://:compute/bash /home/me/run.sh?cores=4&mem=8G&time=01:00:00&maxrunning=20"
```

- Cases arriving within `FZ_SLURM_ARRAY_WINDOW` seconds (default 1) are submitted as one
  array; one calculator URI runs all of them concurrently.
- `maxrunning=M` limits simultaneously running tasks (`--array=0-N%M`).
- Each task changes into its case directory listed in a manifest file: the case
  directories must be on a filesystem **shared with the compute nodes**.
- `FZ_SLURM_POLL_INTERVAL` (default 2 s) sets the polling period.
- Remote job arrays are not supported: use `slurm://user@host:...` for a remote cluster.

## Resources

Both schemes accept resources as a query string at the end of the URI:

| Key | SLURM option |
|-----|--------------|
| `cores` | `--cpus-per-task` |
| `mem` | `--mem` |
| `time` | `--time` |
| `nodes` | `--nodes` |
| `ntasks` | `--ntasks` |
| `gres` | `--gres` |
| `account` | `--account` |
| `qos` | `--qos` |
| `maxrunning` | array throttle (`slurm-array://` only) |

Unknown keys are rejected; values must match `[A-Za-z0-9_.:,=-/]+`.

## Timeouts and interrupts

There is **no default timeout** for SLURM calculators (queue waits are unbounded); a
warning is logged. Set the model's `timeout` or `FZ_RUN_TIMEOUT` to bound a case,
including its time in the queue. Ctrl+C cancels the submitted jobs
([Interrupt & Resume](../running/interrupts.md)).

## Requirements

- Local: `srun` (and `sbatch`, `sacct`/`squeue` for arrays) on `PATH`.
- Remote: SSH access to a login node with `srun`.
- A job failing with a SLURM state such as `TIMEOUT`, `OUT_OF_MEMORY`, `NODE_FAIL`,
  `PREEMPTED` marks the case as failed (then retried).

## Check the cluster by hand first

```bash
sinfo -o "%P"                                   # partition names
srun --partition=compute bash /home/me/run.sh input.txt
```

## See also

[SSH](ssh.md) · [Remote HPC example](../../examples/hpc.md) ·
[Timeouts](../running/timeouts.md) ·
[Architecture note](https://github.com/Funz/fz/blob/main/doc/slurm-architecture.md)
