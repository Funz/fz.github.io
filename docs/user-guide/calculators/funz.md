# Funz Server (`funz://`)

`funz://` sends cases to a legacy **Java Funz calculator** (the execution daemon of the
Java Funz framework). The calculator is located by **UDP discovery**, then driven over
TCP.

```text
funz://[host]:<udp_port>/<code>
```

| Part | Meaning |
|------|---------|
| `host` | Host for the TCP connection (default `localhost`) |
| `udp_port` | **UDP port on which calculators broadcast their availability** (required). The TCP port is read from the broadcast |
| `code` | Code the calculator must offer (`R`, `Python`, `Modelica`, `bash`, ...) |

```python
calculators = "funz://:19001/R"
calculators = ["funz://:19001/R"] * 3            # up to 3 calculators in parallel
```

## How a case runs

1. **Discovery**: listen on `udp_port` for up to 10 s; pick an idle calculator offering
   `code` (else any offering it, else the first seen).
2. **Reservation** on the advertised TCP port.
3. Upload of the input files, execution, download of the results.
4. Release of the calculator.

## Discovery from Python

```python
from fz import discover_funz_servers

servers = discover_funz_servers(19001, listen_duration=10)
# [{'host': '192.168.1.100', 'tcp_port': 5555, 'name': 'calc1', 'os': 'Linux 6.1',
#   'activity': 'idle', 'idle': True, 'codes': ['R', 'Python']}, ...]

idle_r = [s for s in servers if s["idle"] and "R" in s["codes"]]
```

A broadcast is a newline-separated message: calculator name, TCP port, start timestamp,
operating system, activity (`idle` when free), number of codes, then one code per line.

## Requirements

- A running Java Funz calculator: helper scripts `tools/setup_funz_calculator.sh`,
  `tools/start_funz_calculator.sh` in the fz repository.
- UDP broadcasts from the calculator must reach the machine running fz (same network,
  firewall open), and its TCP port must be reachable.
- Default timeout 3600 s ([Timeouts](../running/timeouts.md)).

## See also

- [Funz protocol description](https://github.com/Funz/fz/blob/main/doc/funz-protocol.md)
- [Calculators overview](overview.md)
