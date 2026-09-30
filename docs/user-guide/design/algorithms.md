# Writing Algorithms for fzd

An `fzd` algorithm is a Python (or R) file defining **one class** that proposes points,
receives their results, and decides when to stop. Examples:
[`examples/algorithms/`](https://github.com/Funz/fz/tree/main/examples/algorithms) in the
fz repository.

## File template

```python title=".fz/algorithms/myalgo.py"
#title: My Algorithm
#author: Name
#type: optimization
#options: max_iter=100;tol=1e-6
#require: numpy;scipy

class MyAlgo:
    def __init__(self, **options):
        # values from #options and algorithm_options arrive as strings: cast them
        self.max_iter = int(options.get("max_iter", 100))
        self.tol = float(options.get("tol", 1e-6))
        self.iteration = 0

    def get_initial_design(self, input_vars, output_vars):
        """input_vars: {"x": (min, max), ...}; output_vars: list of output names.
        Returns a list of points: [{"x": 0.5, "y": 1.0}, ...]"""
        self.bounds = input_vars
        return [{v: (lo + hi) / 2 for v, (lo, hi) in input_vars.items()}]

    def get_next_design(self, previous_input_vars, previous_output_values):
        """All points evaluated so far and their outputs (None = failed point).
        Returns the next list of points, or [] to stop."""
        self.iteration += 1
        if self.iteration >= self.max_iter:
            return []
        valid = [(x, y) for x, y in zip(previous_input_vars, previous_output_values)
                 if y is not None]
        ...
        return [next_point]

    def get_analysis(self, input_vars, output_values):
        """Final result: a dict with "text" (summary) and "data" (values)."""
        valid = [(y, x) for x, y in zip(input_vars, output_values) if y is not None]
        best_y, best_x = min(valid, key=lambda t: t[0])
        return {"text": f"best {best_y} at {best_x}",
                "data": {"best_output": best_y, "best_input": best_x}}

    def get_analysis_tmp(self, input_vars, output_values):   # optional
        """Called after each iteration to report progress."""
        return {"text": f"{len(input_vars)} points evaluated"}
```

## Header lines

| Header | Effect |
|--------|--------|
| `#title`, `#author`, `#type` | Descriptive metadata |
| `#options: k=v;k2=v2` | Default options, passed to `__init__(**options)` as strings; overridden by `algorithm_options` |
| `#require: pkg1;pkg2` | Python packages imported by the algorithm. **Missing packages are pip-installed automatically** into the current environment when the algorithm is loaded |

## Rules

- Points are plain dicts of floats; outputs are floats (or lists of floats for a
  list-valued `output_expression`), and `None` for failed points — always filter them.
- Several points per batch are evaluated in parallel on the available calculators;
  duplicates are evaluated once.
- Already evaluated points are served from cache, across iterations and across re-runs.
- Fixed variables (non-range strings in `input_variables`) are not passed to the
  algorithm; fz merges them into every point.

## Analysis content

`get_analysis()` / `get_analysis_tmp()` return a dict. Its `"text"` is inspected and
saved in `analysis_dir`: HTML → `analysis_<i>.html`, JSON → `analysis_<i>.json`,
`key=value` lines → parsed dict, otherwise plain text; `"data"` is returned as-is in
`result["analysis"]`. Details:
[fzd content formats](https://github.com/Funz/fz/blob/main/doc/fzd_content_format.md).

## R algorithms

An `.R` file defining the same methods is supported through `rpy2` (install
`funz-fz[r]` and R). Template: [Funz/fz-AlgorithmR](https://github.com/Funz/fz-AlgorithmR).

## Packaging as `fz-<name>`

To make the algorithm installable with `fz install algorithm <name>`:

```text
fz-myalgo/                  # GitHub repository, default branch "main"
├── .fz/algorithms/myalgo.py
├── tests/                  # a small end-to-end fzd case
└── README.md               # options, what it optimizes/samples, quick start
```

`fz install algorithm myalgo` downloads `https://github.com/Funz/fz-myalgo` (any git URL
or local zip also works) and copies the files of `.fz/algorithms/` into
`./.fz/algorithms/` (`--global`: `~/.fz/algorithms/`). Template repository:
[Funz/fz-Algorithm](https://github.com/Funz/fz-Algorithm).

## Testing

```bash
fz install algorithm ./fz-myalgo.zip
ls .fz/algorithms/                     # fz list shows models and calculators only
fzd --input_dir tests/input.txt --model MyCode \
    --input_vars '{"x": "[0;10]"}' --output_expression result \
    --algorithm myalgo --options '{"max_iter": 20}'
```

Choose a test problem with a known answer (e.g. a quadratic with a known minimum) and
check it in `result["analysis"]`.

## See also

[fzd](../core-functions/fzd.md) · [Installing Models & Algorithms](../installing.md) ·
[Security Model](../../reference/security.md) — an algorithm file is executed code, and
`#require` installs packages
