# SSH Remote Calculator (`ssh://`)

The `ssh://` calculator runs each case on a remote host over SSH. Input files are
uploaded by SFTP, the command runs in a remote temporary directory, and result files are
downloaded back before the outputs are parsed.

Requires the `paramiko` package (`pip install paramiko`).

## URI Syntax

```
ssh://[user[:password]@]host[:port]/command [arguments]
```

```python
# Key-based auth (recommended) — uses your ~/.ssh keys / agent
calculators = "ssh://john@compute.edu/bash /home/john/run.sh"

# Custom port
calculators = "ssh://john@server.edu:2222/bash /path/to/script.sh"

# Several remote nodes in parallel
calculators = [
    "ssh://user@node1.cluster.edu/bash /path/run.sh",
    "ssh://user@node2.cluster.edu/bash /path/run.sh",
]
```

!!! warning "Use absolute paths for remote commands"
    `ssh://user@host/bash script.sh` may not resolve on the remote side. Prefer
    `ssh://user@host/bash /absolute/path/to/script.sh`.

## How It Works

1. Open an SSH connection (key, agent, URI password, or interactive prompt).
2. Create a remote temporary directory.
3. SFTP-upload the compiled input files (and relative [`input_static`](../core-functions/fzr.md#shared-static-files-new-in-12) files).
4. Run the command remotely in that directory.
5. SFTP-download the result files.
6. Remove the remote temp directory.

## Authentication

| Method | How |
|--------|-----|
| SSH key / agent | `ssh://user@host/...` — keys from `~/.ssh/` are tried automatically (recommended) |
| Interactive password | `ssh://user@host/...` — FZ prompts if key auth fails |
| Password in URI | `ssh://user:password@host/...` — insecure, avoid in production |

### Host Key Verification

On first connection to an unknown host, FZ shows the fingerprint and asks whether to
accept it. To skip the prompt (use with care):

```bash
export FZ_SSH_AUTO_ACCEPT_HOSTKEYS=1
```

## Configuration

| Variable | Purpose | Default |
|----------|---------|---------|
| `FZ_SSH_KEEPALIVE` | Keepalive interval, seconds | `300` |
| `FZ_SSH_AUTO_ACCEPT_HOSTKEYS` | Auto-accept unknown host keys | `0` |
| `FZ_RUN_TIMEOUT` | Per-case timeout, seconds | `3600` |

## Remote Script Example

```bash title="/home/user/run.sh (on the server)"
#!/bin/bash
source input.txt

module load gcc/11.2 openmpi/4.1
mpirun -np 16 ./simulation input.txt
# results written to output.txt, downloaded by FZ
```

## See Also

- [Local Shell](shell.md) · [SLURM](slurm.md) (SSH + `srun`) · [Funz Server](funz.md) · [Cache](cache.md)
- [Remote HPC Example](../../examples/hpc.md)
- [Environment Variables](../../reference/environment.md#ssh-configuration)
