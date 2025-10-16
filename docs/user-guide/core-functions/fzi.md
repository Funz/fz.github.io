# fzi - Parse Input Variables

The `fzi` function parses input files to identify all variables.

## Function Signature

```python
fz.fzi(input_path, model)
```

## Parameters

- `input_path` (str): Path to input file or directory
- `model` (dict): Model definition with varprefix

## Returns

Dictionary with variable names as keys (values are None)

## Example

```python
import fz

model = {"varprefix": "$"}
variables = fz.fzi("input.txt", model)
print(variables)
# {'temperature': None, 'pressure': None}
```

See the [main FZ documentation](https://github.com/Funz/fz) for complete details.
