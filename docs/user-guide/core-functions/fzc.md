# fzc - Compile Input Files

The `fzc` function compiles input files by substituting variable values and evaluating formulas.

## Function Signature

```python
fz.fzc(input_path, input_variables, model, output_dir)
```

## Parameters

- `input_path` (str): Path to input file or directory
- `input_variables` (dict): Variable values (scalar or list)
- `model` (dict): Model definition
- `output_dir` (str): Output directory path

## Example

```python
import fz

model = {"varprefix": "$", "formulaprefix": "@"}

fz.fzc(
    "input.txt",
    {"temperature": [100, 200], "pressure": 1.0},
    model,
    "compiled"
)
```

See the [main FZ documentation](https://github.com/Funz/fz) for complete details.
