# Funz Calculator

The Funz calculator provides compatibility with legacy Java Funz calculator servers, enabling FZ to leverage existing Funz infrastructure.

## Overview

Funz is a Java-based framework for computational experiments. The FZ Funz calculator allows Python FZ to communicate with Java Funz calculator servers, providing backward compatibility and integration with existing Funz deployments.

## URI Format

```
funz://[host]:<port>/<code>
```

### Components

- **host** (optional): Hostname of the Funz server (default: localhost)
- **port** (required): TCP port number of the Funz server
- **code**: Model/language code supported by the server (e.g., R, Python, bash)

## Examples

### Local Funz Server

```python
import fz

results = fz.fzr(
    "input.txt",
    {"param1": [1, 2, 3]},
    model,
    calculators="funz://:5555/R",
    results_dir="results"
)
```

### Remote Funz Server

```python
calculators = "funz://server.example.com:5555/Python"
```

### Multiple Funz Servers

Load balance across multiple calculator servers:

```python
calculators = [
    "funz://server1.example.com:5555/R",
    "funz://server2.example.com:5555/R",
    "funz://server3.example.com:5555/R"
]
```

## Protocol

The Funz calculator uses TCP socket communication with a specific protocol:

### Reservation

Before executing a calculation, FZ reserves the calculator:

```
RESERVE <code>
```

Server responds with:
```
OK
```

### Execution

Files are uploaded and execution is requested:

```
EXECUTE <working_dir>
FILE <filename> <size_bytes>
<file_content>
...
```

### Result Retrieval

After execution, results are downloaded:

```
GET <filename>
```

Server responds with file content.

### Unreservation

After completion, the calculator is released:

```
UNRESERVE
```

## UDP Discovery

Funz servers can advertise themselves via UDP broadcast. FZ can automatically discover available Funz calculators on the local network.

### Discovery Process

1. FZ sends UDP broadcast on port 21001: `WHO`
2. Funz servers respond with: `FUNZ <host>:<port> <codes>`
3. FZ automatically configures discovered calculators

### Automatic Discovery

```python
# FZ automatically discovers Funz servers
results = fz.fzr(
    "input.txt",
    variables,
    model,
    calculators="funz",  # Auto-discover
    results_dir="results"
)
```

## Calculator Configuration

Funz calculators can be configured via JSON files in `.fz/calculators/`:

```json
{
  "uri": "funz://:5555",
  "models": {
    "R": "R",
    "Python": "Python"
  }
}
```

## Features

### File Transfer

- Automatic upload of input files to Funz server
- Download of output files after execution
- Binary file support

### Job Management

- Calculator reservation system prevents conflicts
- Automatic retry on calculator failure
- Graceful cleanup on interruption (Ctrl+C)

### Multi-Language Support

Funz servers can support multiple languages/codes:

- R statistical computing
- Python scripting
- Bash shell scripts
- MATLAB/Octave
- Custom calculation codes

## Requirements

- Java Funz calculator server running and accessible
- Network connectivity to Funz server
- Port not blocked by firewall

## Setting Up a Funz Server

To start a Java Funz calculator server:

```bash
java -jar Funz-Calculator.jar \
  -code R \
  -port 5555 \
  -verbose
```

For multiple codes:

```bash
java -jar Funz-Calculator.jar \
  -code R,Python,bash \
  -port 5555
```

## Model Compatibility

The Funz calculator requires that the model is compatible with the specified code:

```python
model = {
    "varprefix": "$",
    "code": "R",  # Must match calculator code
    "output": {
        "result": "cat output.txt"
    }
}

calculators = "funz://:5555/R"  # Code must match
```

## Examples

### R Statistical Analysis

```python
import fz

model = {
    "varprefix": "$",
    "code": "R",
    "output": {
        "mean": "grep 'Mean:' output.txt | awk '{print $2}'"
    }
}

results = fz.fzr(
    "analysis.R",
    {
        "sample_size": [100, 500, 1000],
        "mean": [0, 10, 20],
        "sd": [1, 2, 5]
    },
    model,
    calculators="funz://:5555/R",
    results_dir="r_results"
)
```

### Python Simulation

```python
calculators = "funz://compute-server.local:5555/Python"

results = fz.fzr(
    "simulation.py",
    {"iterations": [1000, 5000, 10000]},
    model,
    calculators=calculators,
    results_dir="sim_results"
)
```

### Load Balancing

Distribute calculations across multiple Funz servers:

```python
calculators = [
    "funz://node1:5555/R",
    "funz://node2:5555/R",
    "funz://node3:5555/R",
    "funz://node4:5555/R"
]

results = fz.fzr(
    "model.R",
    large_parameter_grid,
    model,
    calculators=calculators,
    n_parallel=4  # Use all 4 servers
)
```

## Troubleshooting

### Connection Refused

Check that the Funz server is running:

```bash
telnet hostname 5555
```

Verify firewall rules allow the connection.

### Code Not Supported

Ensure the Funz server supports the requested code:

```bash
echo "WHO" | nc -u hostname 21001
```

Check the server's code list in the response.

### File Transfer Fails

Large files may require timeout adjustments:

```python
model = {
    "varprefix": "$",
    "timeout": 300  # 5 minutes
}
```

### Calculator Reserved

If a calculator is stuck in reserved state, restart the Funz server:

```bash
# Kill existing server
pkill -f "Funz-Calculator"

# Restart
java -jar Funz-Calculator.jar -code R -port 5555
```

## See Also

- [SSH Calculator](ssh.md) - For remote SSH execution
- [SLURM Calculator](slurm.md) - For HPC cluster execution
- [Calculator Overview](overview.md) - Overview of all calculator types
- [Funz Protocol Documentation](https://github.com/Funz/fz/blob/main/FUNZ_UDP_DISCOVERY.md) - Detailed protocol specification
