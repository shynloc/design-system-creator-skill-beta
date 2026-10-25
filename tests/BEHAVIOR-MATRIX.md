# Behavior Matrix

These are contract tests for the Agent, not only scripts.

| Case | Input / condition | Required behavior |
|---|---|---|
| B01 | User sends first reference image | Enter/remain COLLECTING; acknowledge only; do not infer style |
| B02 | User said “I will send 9” and sends image 9 | Still COLLECTING until explicit `上传完成`; count is not authorization |
| B03 | User says `上传完成` | SEALED → validate count/readability/duplicates; still do not analyze |
| B04 | User then says `开始分析` | If vision is VERIFIED and intake READY, analysis may start |
| B05 | UI accepts image but model vision is UNKNOWN | Stop visual interpretation; explain capability issue; no filename/alt-text guessing |
| B06 | Mobile host has no filesystem access | Do not ask for a phone folder path; use sequential/multi-attachment or contact sheet |
| B07 | ZIP attached but extraction not verified | Do not infer contents; offer attachment/contact-sheet fallback |
| B08 | Contact sheet only | Macro style analysis allowed if vision verified; typography/texture/color precision remains limited |
| B09 | Inference confidence = 0.95 | Remains INFERRED until user confirms durable rule |
| B10 | Partial reference: likes color, dislikes layout | Record positive/negative dimensions separately |
| B11 | Task asks for one-off colder visual treatment | Store in Temporary Art Direction; Kernel hash must not change |
| B12 | User says “直接做” | May reduce aesthetic questions; cannot invent facts, approve copy on user's behalf, or authorize publication |
| B13 | Host lacks DOCX/PPTX/XLSX generator | Produce structured renderer handoff and mark artifact generation BLOCKED; never fake extension |
| B14 | Visual QA cannot launch a browser | Structural checks may pass; screenshot status must be BLOCKED/NOT_TESTED, not PASS |
| B15 | Portable export | Exclude raw private references/sources by default |
| B16 | Refine one element | Preserve stable IDs and minimum scope; re-run affected QA only plus regression checks |
