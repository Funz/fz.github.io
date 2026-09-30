# Security Model

fz does **not** sandbox what it runs. This is a deliberate choice of the project: a
restricted formula language was evaluated and rejected because it would break existing
usage (`#@ import`, multi-line Python/R formulas, shell output parsers, `python -c`
calculators).

## What runs as code, with your privileges

| Element | Where it comes from | Executed by |
|---------|---------------------|-------------|
| `#@` context lines and `@{...}` formulas | Input templates | Python `exec`/`eval`, or R |
| Output extractors (shell, `python://`, callables) | Model `output` | bash / Python |
| Calculator commands | Calculator URIs and aliases, installed wrappers' scripts | bash, locally or remotely |
| Algorithm classes | `fzd` algorithm files | Python / R |
| `#require:` lines of algorithms | Algorithm files | `pip install` of the listed packages |

Running a model, an algorithm or a calculator alias from a source is equivalent to
running a shell script from that source. `fz install` from a network source prints a
reminder of this.

## Measures in place

- Case directory names are percent-encoded, and fz refuses to create a case directory
  outside `results_dir` (protects against values such as `../../x`).
- Remote commands built by fz (`mkdir`, `cd`, `rm -rf`, file names) are shell-quoted;
  remote cleanup is refused outside fz's `.fz/tmp/fz_calc_*` / `fz_slurm_*` directories.
- Remote `out.txt`/`err.txt`/`log.txt` are written from the fetched data, not through a
  remote heredoc.
- Passwords embedded in `ssh://` / `slurm://` URIs are masked in the DataFrame,
  `info.txt`, `history.txt`, logs and `manifest.json`.
- SLURM resource values in URIs are validated against a whitelist.

These measures protect fz's own command construction. They do not restrict the user's
commands, formulas or extractors.

## SSH

- With key authentication, unknown host keys are added without fingerprint check;
  populate `~/.ssh/known_hosts` when host identity matters.
- A password in a URI remains in your scripts and in memory; prefer keys.

## AI agents (`fz-mcp`)

Access to `fz-mcp` in its default mode is equivalent to shell access for the agent,
including through prompt injection in files it reads. Mitigations: `FZ_MCP_ROOT`
(path confinement, always on), `FZ_MCP_TRUSTED=0` (only installed aliases), stdio only
unless a network transport is explicitly allowed. Tool annotations are advisory. See
[AI Agents](../user-guide/ai-agents.md#mcp-server-fz-mcp).

## Recommendations

- Read third-party models, calculator aliases, runner scripts and algorithms before use.
- Run untrusted studies in a container or a dedicated account.
- Keep `.fz/` directories under version control to see what changed.
