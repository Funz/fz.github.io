# AI Agents (Claude Code, MCP)

fz provides two integrations for AI coding agents: a **Claude Code plugin** (an Agent
Skill and slash commands) and an **MCP server** (`fz-mcp`) usable by any MCP client.

## Claude Code plugin

```text
/plugin marketplace add Funz/fz
/plugin install fz@funz
```

| Component | Content |
|-----------|---------|
| Agent Skill `fz` | The wrapping workflow (check for an existing `fz-<code>` wrapper, parameterize, define the model, verify `fzi` → `fzc` → one manual run → `fzo`, then `fzr`/`fzd`), a condensed API/CLI reference, the algorithm interface, a wrapper authoring guide |
| `/fz:wrap` | Wrap a simulation code and verify it step by step |
| `/fz:run` | Run a parametric study (`fzr`) and report the results |
| `/fz:design` | Adaptive design of experiments, optimization, calibration (`fzd`) |
| `/fz:install` | Find and install an official `fz-<code>` wrapper or algorithm |

The skill loads automatically when a request mentions fz, Funz, parameter sweeps,
design of experiments over a simulation, or running many cases locally, over SSH or on
SLURM. Its content is in the fz repository under
[`skills/fz/`](https://github.com/Funz/fz/tree/main/skills/fz) and is tested against the
code (CLI flags, environment variables, defaults, signatures).

The skill can also be copied into a project without the plugin system:
`cp -r fz/skills/fz .claude/skills/`.

## MCP server (`fz-mcp`)

```bash
pip install 'funz-fz[mcp]'          # Python >= 3.10
claude mcp add fz -- fz-mcp         # example: register with Claude Code
```

`fz-mcp` exposes `fzi`, `fzc`, `fzr`, `fzo` and `fzl` as MCP tools over **stdio**.

!!! danger "Trusted mode = shell access"
    By default the agent can pass any model and calculator: templates, formulas, output
    commands and calculator commands run as code with your privileges. Register it only
    for agents and inputs you trust.

| Setting | Effect |
|---------|--------|
| `FZ_MCP_ROOT` | All file paths are confined to this directory (default: working directory) |
| `FZ_MCP_TRUSTED=0` | Restricted mode: models and calculators must be installed aliases (no inline model, no `sh://`/`ssh://` URI). Does not sandbox formula evaluation inside fz |
| `FZ_MCP_TRANSPORT` + `FZ_MCP_ALLOW_NETWORK_TRANSPORT=1` | Required together to start a network transport (`sse`, `streamable-http`); otherwise fz-mcp refuses to start. It does not authenticate clients |

Tool annotations: `fzc`/`fzr` are `destructiveHint`/`openWorldHint`, `fzi`/`fzo`/`fzl`
are `readOnlyHint`. They are hints for well-behaved clients, not a security boundary.
`fzd` is not exposed.

## Machine-readable documentation

The fz repository ships [`llms.txt`](https://github.com/Funz/fz/blob/main/llms.txt), an
index of the documentation for LLMs, and the modular
[`doc/`](https://github.com/Funz/fz/tree/main/doc) directory.

## See also

[Security Model](../reference/security.md) · [Environment Variables](../reference/environment.md#mcp-server)
