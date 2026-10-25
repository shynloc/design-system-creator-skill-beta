# Workflow States

Design System Creator hides modes from the user unless they help. Internal state prevents premature analysis and accidental long-term mutation.

## Project phases
`ROUTE → CAPABILITY → SOURCE → IDENTITY → CONTENT → DIRECTION → REVIEW → RESOLVE → RENDER → QA → DELIVER`

Entry shortcuts:
- existing confirmed Kernel: enter at CONTENT;
- quick one-off creation: use TEMPORARY_CONTEXT and enter at CONTENT;
- refine existing artifact: load source + current Resolved Context, then enter REFINE/QA;
- audit: load artifact + Kernel/Context and enter QA.

## Reference intake state
`IDLE → COLLECTING → SEALED → VALIDATING → READY → ANALYZING`

Only explicit user intent can cause:
- `COLLECTING → SEALED`: “上传完成” or semantically equivalent explicit completion.
- `READY → ANALYZING`: “开始分析” or semantically equivalent explicit authorization.

Never infer completion from silence, attachment count, elapsed time, or “probably enough”.

## Design fact state
`OBSERVED → INFERRED → CONFIRMED`

- OBSERVED: directly visible/readable fact, with evidence locator.
- INFERRED: interpretation or preference hypothesis.
- CONFIRMED: user explicitly accepts it as durable design-system truth.

No confidence score automatically upgrades INFERRED to CONFIRMED.
