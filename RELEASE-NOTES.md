# Design System Creator 1.0.0-beta.1 Release Notes

This is the first complete-beta integration build. “Beta” means the planned workflow is present end-to-end and is ready for real use testing; it does not mean a deliberately reduced feature set.

## Included
- natural-language intent routing: Discover / Build / Create / Refine / Audit / Export;
- Capability Gate separating model vision from host/file/artifact capabilities;
- transactional reference intake with explicit `上传完成` and `开始分析` gates;
- reference weighting and dimensional partial preference;
- OBSERVED / INFERRED / CONFIRMED evidence discipline;
- persistent Design Kernel, profiles, anti-style, maturity and provenance;
- temporary art direction isolated from the long-term Kernel;
- Content Semantics + Creative Direction + Visual Pitch;
- shared Resolved Design Context;
- Web, DOCX, PPTX, XLSX, PDF and Charts renderer contracts;
- asset/copy/privacy protocols;
- unified Identity / Creative / Medium / Technical QA;
- Runtime Skill compiler;
- Portable Design System export that excludes raw private references by default;
- two-level package flattening for constrained skill hosts;
- deterministic CLI smoke tests and full-chain E2E test plan.

## Deliberate architecture boundary
DOCX/PPTX/XLSX/PDF generation is delegated to a real host-native artifact renderer when one exists. The Skill never fakes an Office/PDF file by renaming text or HTML. If a host lacks a required renderer, it must produce a structured handoff and mark artifact generation BLOCKED.

## Beta feedback targets
Real mobile sequential uploads; capability discovery wording; interview pacing; quality of inferred Design DNA; visual-pitch usefulness; cross-medium identity consistency; Office/PDF renderer handoff; refine-loop scope control; long-term drift; and the amount of user interruption/approval friction.
