# fzl - List and Validate Models/Calculators

The `fzl` function (or `fz list` command) lists and validates installed models and calculators.

## Command Signature

```bash
fzl [--models PATTERN] [--calculators PATTERN] [--check] [--format FORMAT]
```

Or using the main `fz` command:

```bash
fz list [--models PATTERN] [--calculators PATTERN] [--check] [--format FORMAT]
```

## Options

- `--models PATTERN` - Glob pattern to filter models (default: "*")
- `--calculators PATTERN` - Glob pattern to filter calculators (default: "*")
- `--check` - Validate model/calculator integrity
- `--format FORMAT` - Output format: `markdown` (default), `json`, or `table`

## Returns

Lists installed models and calculators with:
- Model names and supported calculators
- Calculator URIs and supported models
- Validation status (when `--check` is used)

## Examples

### List All Models and Calculators

```bash
fzl --models "*" --calculators "*"
```

### List Specific Models

```bash
fzl --models "perfect*"
```

### Validate Models and Calculators

```bash
fzl --models "*" --calculators "*" --check
```

### JSON Output

```bash
fzl --models "*" --calculators "*" --format json
```

### Table Format

```bash
fzl --models "*" --calculators "*" --format table
```

## Use Cases

- **Discovery**: Find available models and calculators
- **Validation**: Check that models and calculators are properly configured
- **Integration**: Verify calculator-model compatibility
- **Debugging**: Identify configuration issues

## Example Output

```markdown
# Models

## perfectgas
- Supported calculators: localhost_perfectgas, ssh://remote/perfectgas

## mcnp
- Supported calculators: localhost_MCNP, ssh://remote/MCNP

# Calculators

## localhost_perfectgas
- URI: sh://bash calculate.sh
- Supported models: perfectgas

## localhost_MCNP
- URI: sh://bash mcnp.sh
- Supported models: mcnp
```

## See Also

- [fzi](fzi.md) - Parse input variables
- [fzc](fzc.md) - Compile input files
- [fzo](fzo.md) - Parse output files
- [fzr](fzr.md) - Run parametric study
