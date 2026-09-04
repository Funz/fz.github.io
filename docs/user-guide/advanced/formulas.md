# Formula Evaluation

Use Python or R expressions in input templates. See the [main FZ documentation](https://github.com/Funz/fz#formula-evaluation) for complete details.

## Basic Syntax

```text
Temperature: $T_celsius C
# formula context line (evaluated before the formulas below)
#@ import math
T_kelvin: @{$T_celsius + 273.15}
area: @{math.pi * $r ** 2}
```

The formula prefix (`@`), delimiters (`{}`), variable prefix (`$`) and comment marker
(`#`) are all configurable per model.

## Number Formatting (updated in 1.2)

Append `| <pattern>` inside the delimiters to format the result, where `<pattern>` is a
`java.text.DecimalFormat`-style pattern (the same one the original Java Funz used). It
works with both the Python and R interpreters and with any preceding expression.

| Pattern token | Meaning |
|---------------|---------|
| `0` | Always show this digit, zero-padded (fixed number of decimals) |
| `#` | Show this digit only if significant — insignificant trailing zeros are stripped |
| `E` | Scientific notation; digits after `E` set the minimum exponent digits, digits after `.` set the mantissa decimals |

**Template**

```text
pi_value=@{3.14159265 | 0.000}
third=@{1/3 | 0.0000}
trimmed=@{3.1 | #.###}
whole=@{3.0 | #.###}
sci=@{123456.789 | 0.00E00}
```

**Result**

```text
pi_value=3.142
third=0.3333
trimmed=3.1
whole=3
sci=1.23E05
```

## R Interpreter

Set `model["interpreter"] = "R"` (or `FZ_INTERPRETER=R`) to evaluate formulas with R —
`mean()`, `sd()`, `rnorm()`, and multi-line function definitions in `#@` context lines.
Requires the `rpy2` package and an R installation.
