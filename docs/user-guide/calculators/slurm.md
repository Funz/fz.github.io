# SLURM Calculator

The SLURM calculator allows FZ to execute calculations on HPC clusters using the SLURM Workload Manager.

## Overview

SLURM (Simple Linux Utility for Resource Management) is a widely-used job scheduler for HPC clusters. The FZ SLURM calculator provides seamless integration for submitting and managing jobs on SLURM-enabled systems.

## URI Format

```
slurm://[user@host[:port]]:partition/script
```

### Components

- **user** (optional): Username for remote SLURM clusters
- **host** (optional): Hostname for remote SLURM clusters
- **port** (optional): SSH port for remote access (default: 22)
- **partition** (required): SLURM partition name (e.g., compute, gpu, debug)
- **script**: Shell command or script to execute

## Local SLURM Execution

For local SLURM clusters (when FZ runs on the cluster login node):

```python
import fz

results = fz.fzr(
    "input.txt",
    {"param1": [1, 2, 3]},
    model,
    calculators="slurm://:compute/bash script.sh",
    results_dir="results"
)
```

Example with GPU partition:

```python
calculators = "slurm://:gpu/python simulation.py"
```

## Remote SLURM Execution

For remote SLURM clusters accessed via SSH:

```python
calculators = "slurm://username@cluster.example.edu:gpu/bash run.sh"
```

With custom SSH port:

```python
calculators = "slurm://user@cluster.edu:2222:compute/python script.py"
```

## Features

### Automatic Job Management

- Submits jobs to SLURM scheduler using `sbatch`
- Monitors job status using `squeue`
- Retrieves results when jobs complete
- Handles job failures and retries

### Interrupt Handling

Press `Ctrl+C` to gracefully terminate SLURM jobs:

- Cancels all running SLURM jobs using `scancel`
- Cleans up temporary files
- Preserves completed results

### File Transfer

For remote execution:

- Automatically uploads input files to the cluster
- Downloads output files after job completion
- Uses SSH/SCP for secure file transfer

## Configuration

### SLURM Script Headers

The calculator automatically adds appropriate SLURM directives to job scripts:

```bash
#!/bin/bash
#SBATCH --job-name=fz_case_001
#SBATCH --output=output_%j.log
#SBATCH --error=error_%j.log
#SBATCH --partition=compute
```

### Custom SLURM Options

You can specify additional SLURM options in your model configuration:

```python
model = {
    "varprefix": "$",
    "slurm_options": {
        "nodes": 1,
        "ntasks": 4,
        "time": "01:00:00",
        "mem": "8GB"
    }
}
```

## Examples

### Basic Parametric Study

```python
import fz

model = {
    "varprefix": "$",
    "output": {
        "result": "grep 'Result:' output.txt | awk '{print $2}'"
    }
}

results = fz.fzr(
    "simulation.input",
    {
        "temperature": [300, 350, 400, 450],
        "pressure": [1.0, 2.0, 3.0]
    },
    model,
    calculators="slurm://:compute/bash run_simulation.sh",
    results_dir="slurm_results",
    n_parallel=6  # Submit up to 6 jobs simultaneously
)
```

### Multiple Partitions

Use different partitions for different job types:

```python
calculators = [
    "slurm://:compute/bash short_job.sh",  # Quick jobs
    "slurm://:gpu/bash gpu_job.sh"         # GPU-intensive jobs
]
```

### Remote HPC Cluster

```python
calculators = "slurm://myuser@hpc.university.edu:compute/python analyze.py"
```

## Requirements

- SLURM commands must be available: `sbatch`, `squeue`, `scancel`
- For remote execution: SSH access with key-based authentication
- Python `paramiko` package for remote SSH connections

## Limitations

- Requires SLURM workload manager installed
- Job scheduling may introduce delays depending on cluster load
- Remote execution requires SSH key authentication (password auth not supported)

## Troubleshooting

### Job Submission Fails

Check that SLURM is available:

```bash
which sbatch
sinfo  # Check partition availability
```

### Partition Not Found

Verify partition names:

```bash
sinfo -o "%P"
```

### Remote Connection Issues

Test SSH connection:

```bash
ssh user@cluster.example.edu
```

Ensure SSH key authentication is configured.

## See Also

- [SSH Calculator](ssh.md) - For remote execution without SLURM
- [Local Shell Calculator](shell.md) - For local execution
- [Environment Variables](../../reference/environment.md) - Configuration options
