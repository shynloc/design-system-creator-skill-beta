# Design System Creator 1.0.0-beta.1 — Full-chain E2E Test Plan

Beta means feature-complete for this planned scope but awaiting real user/host feedback. Do not mark a case PASS without actual evidence. Record `PASS / FAIL / BLOCKED / NOT_TESTED`, host/app, active model, input mode, artifact paths, screenshots, and UX friction.

## T01 — Capability Gate
Use a session with visual input, then (if possible) a non-vision/unknown model. Verify model vision and host attachment/filesystem/archive/browser abilities are treated independently. Unknown vision must block image-content claims.

## T02 — Mobile sequential reference intake
On mobile, announce that 9 images will be sent, then send them one at a time. The Skill must only acknowledge/registry-update for all 9. Send `上传完成`: it validates but does not analyze. Send `开始分析`: only then may analysis begin.

## T03 — Reference weighting
Provide core, positive, negative and partial references. For a partial reference say “只喜欢配色，不喜欢排版”. Verify dimensional positive/negative evidence remains distinct.

## T04 — Design Kernel creation
Build a persistent Kernel from references + interview. Check philosophy, principles, anti-style, tokens, profiles, medium rules, provenance and maturity. Every durable conclusion must be OBSERVED/INFERRED/CONFIRMED; AI must not self-confirm.

## T05 — Visual Pitch / Creative Direction
Use one real content source. Request 2–3 candidates. They must differ in composition/type/assets/interaction, not only color. Inspect actual prototypes or representative sample artifacts; choose/reject/combine one direction.

## T06 — Web production
Generate a responsive Web artifact from the chosen direction. Verify content-specific visual subject, desktop/mobile reflow, reduced-motion fallback, links/interactions, no generic repeated cards, and actual screenshots where browser capability exists.

## T07 — DOCX production
Generate a real DOCX with cover, H1/H2/H3, long Chinese body text, quote, table, image, caption, page number/header/footer. Open/render it. Verify long-form reading behavior, page breaks, font fallback and that it does not look like a web page pasted into Word.

## T08 — PPTX production
Generate a real deck containing Cover, Section, Statement, Evidence, Data, Comparison, Process/Timeline, Image-led and Conclusion layouts. Render to images/PDF and inspect rhythm, overflow, repeated layouts, chart readability and safe margins.

## T09 — XLSX production
Generate a real workbook containing inputs, formulas, outputs, KPI, structured table, conditional format, chart and dashboard. Open/recalculate; verify formulas, formats, chart ranges, semantic colors and scan efficiency.

## T10 — PDF delivery
Produce PDF from a DOCX/PPTX/HTML source. Inspect representative pages for embedded/substituted fonts, raster quality, page size/margins, links, page numbers and visual continuity.

## T11 — Temporary Art Direction isolation
Record Kernel SHA-256. Apply a one-off temporary direction and make an artifact. Re-hash the Kernel. Hash must be unchanged unless the user explicitly asked to promote that change into the long-term system.

## T12 — Precise refine loop
Pick a stable scene/slide/element and request a small change. Verify minimum scope, rollback/version trace, unchanged source facts, and new screenshots/render for the affected region.

## T13 — Runtime Skill compiler
Compile the confirmed Kernel into a Runtime Skill, install/load it in a new session, then create two different media (for example PPTX + DOCX). Verify both share identity while adapting to the medium and task.

## T14 — Portable export privacy
Export Portable Design System. Verify no private reference images, raw source documents, absolute paths, credentials or restricted fonts/assets are included by default.

## T15 — Versioned regression
Confirm one durable token/rule change. Bump design-system version, record decision, rebuild representative Web/DOCX/PPTX/XLSX samples, then compare identity/medium QA. Verify unrelated rules did not drift.

## Suggested evidence bundle
`TEST-REPORT.md`, `results.json`, screenshots/renders, generated artifacts, Kernel before/after hashes, Runtime Skill ZIP, Portable Export ZIP, and a short UX log: what felt slow, confusing, repetitive, or unexpectedly good.
