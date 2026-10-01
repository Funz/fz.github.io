# SSH (`ssh://`)

`ssh://` runs each case on a remote host: inputs are uploaded by SFTP into a remote
temporary directory, the command runs there, results are downloaded, and the outputs
are parsed locally. Uses `paramiko` (installed with fz). fz itself is not needed on the
remote host.

```text
ssh://[user[:password]@]host[:port]/command [arguments]
```

```python
calculators = "ssh://john@compute.example.edu/bash /home/john/run.sh"
calculators = "ssh://john@compute.example.edu:2222/bash /home/john/run.sh"
calculators = [                                    # 2 hosts, 2 cases at a time
    "ssh://user@node1/bash /opt/code/run.sh",
    "ssh://user@node2/bash /opt/code/run.sh",
]
```

Use **absolute remote paths** in the command. As with `sh://`, the input file names are
appended to the command line.

## Authentication

| Method | How |
|--------|-----|
| SSH key / agent (recommended) | `ssh://user@host/...` — keys from `~/.ssh/` and the agent are used |
| Password in URI | `ssh://user:pw@host/...` — keys and agent are then not tried; the password is masked in results, logs and manifests, but visible in your scripts |

There is no interactive password prompt. When `user@` is omitted, the user name is
`$SSH_USER`, else the local user name.

## Host keys

| Situation | Behavior |
|-----------|----------|
| Key authentication, unknown host | Key added automatically (no fingerprint check) |
| Password in URI, unknown host | Interactive prompt `Accept this host key? [y/N/fingerprint]` — blocks unattended runs |
| `FZ_SSH_AUTO_ACCEPT_HOSTKEYS=1` | Key added automatically in all cases |

When host identity matters, fill `~/.ssh/known_hosts` beforehand and check the
fingerprint.

## Settings

| Variable | Default | Meaning |
|----------|---------|---------|
| `FZ_SSH_KEEPALIVE` | `300` | Keepalive interval (s) |
| `FZ_SSH_AUTO_ACCEPT_HOSTKEYS` | `0` | See above |
| `FZ_RUN_TIMEOUT` | unset → **no timeout** for `ssh://` | Set it (or the model's `timeout`) to bound remote runs |

## Safety measures

- Remote directory names and file names are shell-quoted.
- Remote cleanup (`rm -rf`) is refused outside fz's own `.fz/tmp/fz_calc_*` directories.
- The calculator command itself is run as written: it is your code.

## Static files

Relative `input_static` files are uploaded for each case; absolute ones must already
exist at the same path on the remote host (shared storage).

## See also

[SLURM](slurm.md) · [Remote HPC example](../../examples/hpc.md) ·
[Timeouts](../running/timeouts.md)
