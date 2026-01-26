# Calculator Overview

Calculators define where and how calculations are executed. FZ supports multiple calculator types for different execution environments.

## Available Calculator Types

### Local Execution
- **[Local Shell](shell.md)** - Execute on local machine using shell commands
- **[Cache](cache.md)** - Reuse previous results based on input hashes

### Remote Execution
- **[SSH Remote](ssh.md)** - Execute on remote servers via SSH
- **[SLURM](slurm.md)** - Execute on HPC clusters with SLURM workload manager
- **[Funz Server](funz.md)** - Connect to legacy Java Funz calculator servers

## URI Format

Each calculator type uses a specific URI format:

- Shell: `sh://[path/to/]script`
- SSH: `ssh://user@host[:port]/script`
- SLURM: `slurm://[user@host[:port]]:partition/script`
- Funz: `funz://[host]:<port>/<code>`
- Cache: `cache://`

## New in Version 0.9.1

- **SLURM Calculator**: Full support for HPC workload management
- **Funz Calculator**: Backward compatibility with Java Funz servers
- **Shell Path Configuration**: Custom binary resolution via `FZ_SHELL_PATH`

See individual calculator documentation for detailed usage and examples.

