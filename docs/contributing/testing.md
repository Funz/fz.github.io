# Testing

FZ uses `pytest`. Tests live in `tests/` in the [main repository](https://github.com/Funz/fz).

## Running the Suite

```bash
pip install -e ".[dev]"

python -m pytest tests/ -v                 # everything
python -m pytest tests/test_fzd.py -v      # one file
python -m pytest tests/ -k parallel -v     # by keyword
FZ_LOG_LEVEL=DEBUG python -m pytest tests/test_interrupt_handling.py -v
```

## Notable Test Areas

| File(s) | Covers |
|---------|--------|
| `test_parallel.py` | Concurrent execution, load balancing |
| `test_interrupt_handling.py` | Ctrl+C graceful shutdown, resume |
| `test_fzd*.py` | Design of experiments, vector / multi-objective outputs |
| `test_static_files*.py` | `input_static` (local and real SFTP over `ssh://`) |
| `test_vector_outputs.py` | Array-valued `output` entries across `fzo` / `fzr` |
| `shell-free-outputs.yml` (CI) | `python://` / `jq://` / `yq://` / `xpath://` across platforms, incl. Windows without bash |
| `ssh-localhost.yml` (CI) | Real SSH/SFTP against localhost |
| `test_examples_*.py` | The runnable examples under `examples/` |

## Writing a Test for Your Own Model

```python
import fz, tempfile
from pathlib import Path

def test_my_model():
    with tempfile.TemporaryDirectory() as tmp:
        inp = Path(tmp) / "input.txt"
        inp.write_text("Parameter: $param\n")

        calc = Path(tmp) / "calc.sh"
        calc.write_text('#!/bin/bash\nsource "$1"\necho "result=$param" > output.txt\n')
        calc.chmod(0o755)

        model = {
            "varprefix": "$",
            "output": {"result": "grep 'result=' output.txt | cut -d= -f2"},
        }

        results = fz.fzr(
            str(inp), {"param": [1, 2, 3]}, model,
            calculators=f"sh://bash {calc}",
            results_dir=str(Path(tmp) / "results"),
        )

        assert len(results) == 3
        assert list(results["result"]) == [1, 2, 3]
        assert all(results["status"] == "done")
```

## See Also

- [Development](development.md)
- [Troubleshooting](../reference/troubleshooting.md) — `FZ_LOG_LEVEL=DEBUG` for execution traces
