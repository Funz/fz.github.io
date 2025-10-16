# fzo - Parse Output Files

The `fzo` function reads and parses calculation results from output directories.

## Function Signature

```python
fz.fzo(output_dir, model)
```

## Parameters

- `output_dir` (str): Path to results directory
- `model` (dict): Model definition with output commands

## Returns

pandas DataFrame with results

## Example

```python
import fz

model = {
    "output": {
        "pressure": "grep 'Pressure:' output.txt | awk '{print $2}'"
    }
}

results = fz.fzo("results", model)
print(results)
```

See the [main FZ documentation](https://github.com/Funz/fz) for complete details.
