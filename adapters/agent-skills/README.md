# Agent Skills Adapter

This adapter generates installable `SKILL.md` files from the canonical
skill definitions in `/skills`, following the cross-agent SKILL.md
convention (`skills/<name>/SKILL.md` with `name` + `description` frontmatter).

The generated layout is consumed natively by:

- **Devin** — via `.devin-plugin/plugin.json` (this repo installs directly as a plugin)
- **Claude Code** — via `.claude-plugin/plugin.json`
- **skills.sh / Agent Plugins-style loaders** — bare `skills/<name>/SKILL.md` layout
- Any agent that scans `skills/<name>/SKILL.md`

## Generate

From repo root:

```bash
python3 adapters/agent-skills/build.py
```

Unlike the Codex adapter, the output is written to `skills/<name>/SKILL.md`
at the repository root and **is committed**, so the repository can be
installed directly as a plugin without a local build step.

Re-run after any change to `skills/*.md` — most importantly after merging
upstream changes (see `Syncing with upstream` in the root README).

## Notes

- Canonical filenames use `snake_case` (`htmx_modal_form_flow.md`); generated
  skill directories use `kebab-case` (`htmx-modal-form-flow/`) because the
  SKILL.md `name` spec allows only lowercase letters, numbers, and hyphens.
- Generated files carry a `generated-by` marker in their frontmatter
  metadata. Do not edit them by hand — edit the canonical file in
  `skills/*.md` and regenerate.
- The generator removes stale generated directories whose canonical source
  no longer exists (identified by the marker), so deletions upstream
  propagate cleanly.
