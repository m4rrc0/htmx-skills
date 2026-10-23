# htmx-skills

**Opinionated, server-driven HTMX interaction skills for AI-assisted coding.**

> **Compatibility port.** This repository is a fork of [`khabaznak/htmx-skills`](https://github.com/khabaznak/htmx-skills) that adds agent-plugin packaging on top of the original work. **All credit for the skills, the philosophy, and the content goes to the original author, [khabaznak](https://github.com/khabaznak).** This fork keeps the author's intent and expertise 100% intact — it only adds packaging (plugin manifests, generated `SKILL.md` files) and upstream-sync tooling so the skills load directly in Devin, Claude Code, and other agents that understand the `skills/<name>/SKILL.md` convention.

`htmx-skills` is a collection of reusable interaction patterns (“skills”) designed to guide AI coding assistants toward **clean, server-driven HTMX solutions**, without defaulting to JavaScript or frontend frameworks.

This repository encodes *how to think* about HTMX—not just how to write it.

---

## Install as a Plugin

This fork ships the canonical skills in the cross-agent `skills/<name>/SKILL.md` layout, so the repository can be installed directly — no build step required.

- **Devin** — the repo is a valid Devin plugin (`.devin-plugin/plugin.json`). Install it from the Customize page or with `devin plugins install` pointing at this repository.
- **Claude Code** — the repo is a valid Claude plugin (`.claude-plugin/plugin.json`).
- **Other agents** — any agent that scans `skills/<name>/SKILL.md` (skills.sh, Agent Plugins-style loaders) can consume the generated skills directly or copy them into its own skills directory.
- **Codex** — use the Codex adapter: `python3 adapters/codex/build.py`, then copy `adapters/codex/dist/.codex/skills/*` into `.codex/skills/` or `~/.codex/skills/` (see [`adapters/codex/README.md`](./adapters/codex/README.md)).

The generated `skills/<name>/SKILL.md` files are committed and derived 1:1 from the canonical `skills/*.md` files by [`adapters/agent-skills/build.py`](./adapters/agent-skills/build.py).

---

## Syncing with Upstream

This fork tracks [`khabaznak/htmx-skills`](https://github.com/khabaznak/htmx-skills) as `upstream`.

- **Automated:** the [`Sync upstream`](./.github/workflows/sync-upstream.yml) GitHub Action runs weekly (and on demand via *Actions → Sync upstream → Run workflow*). It merges `upstream/main` into a `sync/upstream-*` branch, regenerates the agent skills, and opens a PR. On a merge conflict the run fails — resolve manually as below.
- **Manual:**

  ```bash
  git remote add upstream https://github.com/khabaznak/htmx-skills.git
  git fetch upstream
  git merge upstream/main          # resolve conflicts if any
  python3 adapters/agent-skills/build.py   # regenerate skills/<name>/SKILL.md
  git add skills/ && git commit
  ```

After every upstream merge, the generated `SKILL.md` files must be regenerated (a CI check enforces this). Canonical `skills/*.md` files are never edited by this fork — all port-specific additions live outside them (manifests, generated dirs, adapters, workflows).

---

## Why This Exists

Modern coding assistants are extremely capable, but they have strong defaults:
- client-side JavaScript
- JSON APIs for UI composition
- frontend frameworks for state and flow

HTMX takes a different approach.

When asked to implement common interactions (modals, inline edits, confirmations, form flows), AI assistants often reach for JavaScript even when a **simpler, more maintainable HTMX-native solution exists**.

This repository exists to correct that behavior.

---

## What Are “Skills”?

A **skill** is a repeatable interaction pattern defined by:
- a single user intent
- clear constraints
- explicit route responsibilities
- server-rendered HTML fragments
- declarative HTMX swaps

Skills are **not snippets** and **not full applications**.  
They are behavioral contracts that both humans and AI models can follow.

---

## Core Principles

- **Server-driven UI**
- **HTML as the primary contract**
- **No JavaScript by default**
- **Clear route responsibilities**
- **One skill = one user intent**
- **Progressive enhancement friendly**

These principles are enforced intentionally and consistently.

For deeper rationale, see [`philosophy.md`](./philosophy.md).

---

## Repository Structure

```
htmx-skills/
├── .devin-plugin/     # Devin plugin manifest (compat port addition)
├── .claude-plugin/    # Claude Code plugin manifest (compat port addition)
├── .github/workflows/ # Upstream sync + generated-files CI (compat port addition)
├── skills/            # Canonical skill definitions (one file per skill)
│   └── <name>/        #   + generated SKILL.md files (committed, derived)
├── adapters/          # Vendor-specific adapters (Codex, agent-skills, etc.)
├── templates/         # Templates for new skills and adapters
├── philosophy.md      # Design and governance principles
└── README.md
```

---

## Skills

Each skill:
- is expressed in plain language and structured markdown
- includes intent, constraints, UI structure, and route contracts
- avoids framework- or language-specific assumptions

### Example Skill
- `htmx_modal_form_flow`  
  A complete modal-based form submission pattern using pure HTMX, server-rendered partials, and out-of-band swaps—no JavaScript required.

---

## Adapters

Skills are **model-agnostic** by design.

Adapters translate the same skill definition into formats understood by:
- Codex
- Claude
- OpenAI Chat
- MCP-based agent frameworks

Adapters **do not redefine skills**.  
They only adapt them.

---

## What This Repository Is Not

This repository intentionally does **not** include:
- frontend frameworks
- JavaScript helpers
- full demo applications
- CSS systems or UI kits
- client-side state management

Those concerns distract from the core goal:
**teaching AI-assisted coding tools to behave correctly with HTMX.**

---

## Who This Is For

This repository is for:
- Developers who already use HTMX
- Teams frustrated by AI-generated JavaScript
- Anyone designing server-driven interfaces
- People who care about architectural discipline

It is *not* a beginner tutorial.

---

## Contributing

Contributions are welcome, but intentionally constrained.

A good contribution:
- encodes a clear interaction pattern
- removes the need for JavaScript
- improves AI behavior, not just convenience
- respects the philosophy of the repository

A contribution may be rejected if it:
- introduces JavaScript without necessity
- relies on frontend frameworks
- weakens existing constraints
- blurs server/client responsibilities

See [`philosophy.md`](./philosophy.md) before contributing.

---

## License

MIT License.  
Patterns should be shared freely.