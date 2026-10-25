# Capability Gate

Design System Creator must separate **Model Capability** from **Host Capability**.

- Model capability answers: does the active model actually receive and understand image pixels?
- Host capability answers: can the current App/Agent receive attachments, multiple images, read a folder, extract ZIP, render in a browser, take screenshots, or generate a real DOCX/PPTX/XLSX/PDF?

These are independent. An attachment button does not prove the model can see pixels. A vision model does not prove the host can read a local folder.

## Vision states

- `VISION_VERIFIED`: the active runtime explicitly supports image input / visual understanding. Visual analysis is allowed after Reference Intake is committed.
- `VISION_UNKNOWN`: image input capability cannot be verified. Do not describe or classify image content. Recommend switching to a current model/runtime that explicitly supports image input, or use a text-only path.
- `VISION_UNSUPPORTED`: the runtime explicitly lacks image understanding. Visual reference analysis is blocked; text descriptions may still be used as user-provided statements.

**Anti-hallucination contract:** if vision is not `VISION_VERIFIED`, **不得描述附件图片内容**；不得从 filename、path、alt text、attachment placeholder、previous assistant claims、or user expectation infer what the image contains.

## Host capability states
Use `VERIFIED / AVAILABLE_UNVERIFIED / UNSUPPORTED / UNVERIFIED` per capability. Track independently:
- `attachments`
- `multi_image`
- `filesystem_read`
- `filesystem_write`
- `archive_extract`
- `browser_render`
- `screenshot`
- `docx`
- `pptx`
- `xlsx`
- `pdf`

## Routing
- Folder mode appears only when `filesystem_read` is VERIFIED.
- ZIP/Archive mode appears only when `archive_extract` is VERIFIED.
- Mobile defaults to attachment/sequential attachment mode; never assume a phone file path is readable.
- Browser screenshot QA is PASS only after an actual screenshot succeeds.
- Office/PDF artifact generation is PASS only after the real artifact is created by a capable renderer.

Specific model names may be offered as current examples, but capability declaration is the primary rule. Do not make a model list a permanent source of truth.
