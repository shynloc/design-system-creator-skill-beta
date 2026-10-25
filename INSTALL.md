# Install / Deploy

Design System Creator is designed so the **repository root is the Skill root**. An Agent should install or copy the **entire repository**, not only `SKILL.md`.

## Fastest route

Give your Agent this GitHub repository URL and say:

```text
Install this repository as an Agent Skill. Treat the repository root as the Skill root.
Read SKILL.md and START-HERE.md first, preserve references/, schemas/, templates/, scripts/, examples/ and tests/, then run the local self-test before declaring the installation successful.
Do not install only SKILL.md.
If your host has a native GitHub/Skill installer, use it. Otherwise clone or download the repository into the host's supported Skill directory.
Do not invent a successful installation: if the host cannot install Skills or execute the validation command, tell me exactly what is blocked.
```

## Verification

From the installed Skill root:

```bash
python scripts/design_studio.py version
python scripts/design_studio.py self-test
python tests/run_tests.py
```

Expected local contract result for this beta: **13 PASS / 0 FAIL**.

## If the host cannot run Python

The methodology in `SKILL.md` and `references/` remains usable, but deterministic compiler/validation steps must be marked **UNVALIDATED** rather than silently skipped.

## Important

- Image analysis requires a model/runtime that actually exposes image pixels to the Agent.
- Folder and ZIP workflows require real filesystem/archive capability.
- Office/PDF output requires a genuine renderer in the host; the Skill must not fake a generated file when no renderer exists.
