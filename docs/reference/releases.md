# Release Notes

## Version 1.1 (2026-06-15)

### New Features

#### `fzd` CLI — `--input_path` / `--input_variables` Aliases
`fzd` (and `fz design`) now accept the same flag names used by `fzi`, `fzc`, and `fzr`:
`--input_path` (alias for `--input_dir`) and `--input_variables` / `--variables` (aliases for `--input_vars`).
All flag forms remain accepted for backward compatibility.

#### `fzd` — Calculator Auto-Discovery
`fzd` now auto-discovers the installed calculator alias that matches the model id, exactly like `fzr`.
When a model wrapper has been installed with `fz install model <code>`, you can omit `calculators`
in `fzd` calls and the correct calculator is selected automatically.

#### Calculator Bare Alias Names
`--calculators <alias>` now works in all commands. Previously only full URIs were accepted.

#### Script-Friendly Output Streams
Results are printed to **stdout**; logs, progress bar, and errors go to **stderr**.
The progress bar is automatically suppressed when stderr is not a terminal (CI pipelines, redirected output).

```bash
fzr input.txt --model perfectgas --variables '{"x": [1,2]}' \
    --calculator "sh://bash calc.sh" --format json > results.json 2> run.log
```

Exit codes: `0` on success, non-zero on argument/file errors. `fzr` exits `1` when no case
succeeded; partial success exits `0` with per-case details in the `status` column.

### Bug Fixes

#### Recursive Directory Staging
Case subdirectories are now correctly staged into and out of the run directory. Studies
whose input is organized as a directory tree (e.g. OpenFOAM cases) no longer silently
drop nested files.

#### `fzd` / `fz design` CLI Argument Forwarding
Arguments were incorrectly forwarded to the core `fzd()` function, causing unexpected
errors. The CLI now filters and maps arguments correctly.

#### `fzd` Results Directory
The `--results_dir` flag was ignored in some code paths; it is now consistently applied.

#### Calculator Discovery
Several bugs in model/calculator alias resolution have been fixed, making `fz list --check`
and alias-based calculator lookup more reliable.

#### Funz UDP Discovery Fallback
A UDP discovery miss (no Funz server found on the network) no longer counts as a hard
calculator failure. `fzr`/`fzd` now fall back to the next calculator in the list.

---

## Version 1.0 (2026-04-27)

### New Features

#### `fzd` — Batch Deduplication
Duplicate design points proposed by an algorithm within the same iteration are evaluated only once; results are re-mapped to all occurrences.

#### `fzd` — Cross-Iteration Caching
Results from previous iterations are automatically reused — a point evaluated in iteration 2 is never re-run in iteration 5. No extra configuration required.

#### `fzd` — Re-Run Resume
If `analysis_dir` already exists it is renamed with a timestamp suffix and its cached results are still consulted, so a re-run with different options benefits from all prior computations.

### Bug Fixes

#### Formula variable prefix (`interpreter.py`)
`evaluate_formulas` now uses the model's configured `varprefix` (and `var_delim`) when replacing variables inside `@{...}` expressions, instead of the previously hardcoded `$`.

---

## Version 0.9.1 (2026-01-25)

### New Features

#### `fzd` - Design of Experiments with Adaptive Algorithms
- **New function and CLI command**: `fzd` (or `fz design`) for iterative design of experiments
- Algorithm-driven exploration: algorithms choose which points to evaluate next
- Variable ranges: `{"x": "[0;10]"}` instead of fixed value lists
- Custom output expressions: combine multiple outputs with math operators
- Pluggable algorithm interface with `get_initial_design`, `get_next_design`, `get_analysis`
- Built-in algorithms: Random Sampling, Brent's Method (1D), BFGS (multi-D), Monte Carlo
- Algorithm options via dict, JSON string, or JSON file
- Full CLI support: `fzd -i input/ -v '{"x": "[-2;2]"}' -e "result" -a algorithm.py`
- Analysis results with HTML reports and plots

#### `fzl` Command - List and Validate Models/Calculators
- **New CLI command**: `fzl` (or `fz list`) for listing and validating installed models and calculators
- Supports glob patterns for filtering: `fzl --models "perfect*" --calculators "ssh*"`
- Validation mode with `--check` flag to verify model/calculator integrity
- Multiple output formats: JSON, Markdown (default), Table
- Shows supported calculators for each model
- Example usage:
  ```bash
  fzl --models "*" --calculators "*" --check --format markdown
  ```

#### Enhanced Calculator Support

**SLURM Workload Manager Integration**
- New calculator type: `slurm://[user@host[:port]]:partition/script`
- Supports both local and remote SLURM execution
- Local: `slurm://:compute/bash script.sh`
- Remote: `slurm://user@cluster.edu:gpu/bash script.sh`
- Automatic partition scheduling and job management
- Interrupt handling (Ctrl+C terminates SLURM jobs)

**Funz Server Protocol Support**
- New calculator type: `funz://[host]:<port>/<code>`
- Compatible with legacy Java Funz calculator servers
- TCP socket-based communication with reservation/unreservation
- Automatic file upload/download
- UDP discovery support for automatic server detection
- Example: `funz://:5555/R` or `funz://server.example.com:5555/Python`

#### Shell Path Configuration (FZ_SHELL_PATH)
- **New environment variable**: `FZ_SHELL_PATH` for custom binary resolution
- Overrides system PATH for shell commands in models and calculators
- Essential for Windows users with MSYS2, Git Bash, or custom tool locations
- Format: Semicolon-separated on Windows, colon-separated on Unix/Linux
- Example: `SET FZ_SHELL_PATH=C:\msys64\usr\bin;C:\msys64\mingw64\bin`
- Automatic `.exe` extension handling on Windows
- Binary path caching for performance

#### R Interpreter Support
- **Formula evaluation with R**: Set interpreter to "R" for statistical computing
- Configure via `model["interpreter"] = "R"` or `set_interpreter("R")`
- Supports R statistical functions: `mean()`, `sd()`, `median()`, `rnorm()`, etc.
- Multi-line R function definitions in formula context
- Requires `rpy2` package and R system installation
- Example:
  ```text
  #@ samples <- rnorm($n, mean=$mu, sd=$sigma)
  Mean: @{mean(samples)}
  ```

#### Variable Default Values
- **New syntax**: `${var~default}` for specifying default values
- Falls back to default when variable not provided in `input_variables`
- Useful for configuration templates with sensible defaults
- Example: `${host~localhost}`, `${port~8080}`
- Warning issued when default value is used

#### Old Funz Syntax Compatibility
- Support for legacy Java Funz variable syntax: `?var` (equivalent to `$var`)
- Backward compatibility for existing Funz users migrating to Python
- Automatic detection and replacement
- Example: `Temperature: ?T_celsius` → `Temperature: 25`

#### Progress Callbacks
- **New callback system** for monitoring execution progress
- Callback functions receive events: `case_start`, `case_complete`, `case_failed`
- Real-time progress tracking for long-running calculations
- Custom progress bars, logging, or UI updates
- Example:
  ```python
  def progress_callback(event_type, case_info):
      if event_type == "case_complete":
          print(f"✓ Case {case_info['case_name']} done")
  
  fzr(..., callbacks=[progress_callback])
  ```

### Improvements

#### Protocol-Specific Error Reporting
- Descriptive error messages for each calculator protocol (shell, SSH, SLURM, Funz)
- Error classification: connection, authentication, timeout, execution, file transfer
- Error details recorded in `history/info.txt` for each case
- Error context preserved in DataFrame `error` column

#### Enhanced Argument Parsing
- CLI arguments now support three formats:
  1. **Inline JSON**: `--model '{"varprefix": "$"}'`
  2. **JSON file**: `--model model.json`
  3. **Alias**: `--model perfectgas` (loads from `.fz/models/perfectgas.json`)
- Automatic detection with fallback and helpful error messages
- Better type validation with detailed warnings
- Consistent behavior across all CLI commands

#### Calculator-Model Compatibility
- Automatic validation that calculators support specified models
- Prevents incompatible calculator/model combinations
- Clear error messages when model not supported by calculator
- Alias resolution for both models and calculators

#### Timeout Configuration
- Flexible timeout settings at multiple levels:
  - Environment variable: `FZ_EXECUTION_TIMEOUT`
  - Model configuration: `model["timeout"]`
  - Calculator URI: `sh://script.sh?timeout=300`
- Per-calculator timeout overrides
- Default timeout handling for long-running calculations

#### Better Error Handling
- Comprehensive error messages with context
- Automatic help display on TypeError (missing/wrong arguments)
- Detailed warnings for argument parsing failures
- Stack trace preservation for debugging

#### Code Quality & Sanitization
- Extensive code cleanup and refactoring
- Improved type hints and docstrings
- Better separation of concerns
- Enhanced test coverage (100+ new tests)
- Fixed unsafe bash command replacement vulnerabilities

### Bug Fixes

- Fixed Windows path separator handling in file operations
- Fixed unsafe bash command string replacement (security issue)
- Fixed PATH environment variable not respecting FZ_SHELL_PATH priority
- Fixed SLURM URI parsing for local execution (`:partition` prefix required)
- Fixed scalar value result extraction in various contexts
- Fixed calculator XML configuration for Funz integration
- Fixed missing JSON files during model/plugin installation
- Fixed OSError handling in Windows script execution
- Fixed R interpreter initialization and expression evaluation
- Fixed cache matching when outputs are None
- Fixed directory structure creation when no input variables specified

### Breaking Changes

- **fzr directory structure**: Now creates subdirectories in `results_dir` as long as any `input_variable` is set up
  - No subdirectories only when `input_variables={}`
  - More consistent with user expectations
  - Better organization for parametric studies

---

## Version 0.9.0 (2025-11-27)

Initial release of FZ - Parametric Scientific Computing Framework.

### Core Features

- Four core functions: `fzi`, `fzc`, `fzo`, `fzr`
- Command-line interface with dedicated commands
- Parametric study automation with Cartesian product
- Parallel execution with thread pool
- Smart caching based on input file hashes
- Retry mechanism with calculator fallback
- Remote execution via SSH
- Interrupt handling (Ctrl+C) with graceful shutdown
- DataFrame output with automatic type casting
- Formula evaluation with Python interpreter
- Model and calculator aliases
- Comprehensive test suite
- BSD 3-Clause License

### Calculator Types

- Local shell execution (`sh://`)
- SSH remote execution (`ssh://`)
- Cache calculator (`cache://`)

### Model Definition

- Variable substitution with `$var` syntax
- Formula evaluation with `@{expression}` syntax
- Comment-based formula context
- Output command specification
- Model aliasing with JSON files

### Installation

- PyPI package: `funz-fz`
- pipx support for CLI tools
- Optional dependencies: `paramiko`, `pandas`

---

For the latest updates and detailed changelog, visit the [GitHub repository](https://github.com/Funz/fz).
