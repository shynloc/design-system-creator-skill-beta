# Visual Pitch

Use when visual direction is not already locked and seeing alternatives materially improves the decision.

## Rule
A visual pitch is a **real, inspectable prototype**, not a list of adjectives or palette swatches. Web pitches should be actual HTML. For Office/PDF work, use the best host-native preview or representative sample pages/slides/sheets.

## Candidate count
- Quick: usually 2 materially different candidates.
- Studio/important identity work: usually 3.
- User already specified direction: 1 focused candidate can be enough.

## Material difference
At least 3 of these should differ: composition/grid, typography hierarchy, visual subject/asset language, density, motion/interaction, information architecture. Color-only variants do not qualify.

Each candidate records:
- why it fits the content and Design Kernel;
- three visual signature rules;
- where it works best;
- tradeoffs / performance / accessibility;
- what it deliberately avoids.

## Review
Show actual outputs/screenshots where the host permits. User may select, reject, combine, or explicitly delegate selection. Visual approval does not imply factual/copy approval or publishing authorization.

`scripts/build_visual_pitch.py` is a deterministic three-direction smoke-test generator. Its built-in variants prove workflow plumbing; they are not universal production templates.
