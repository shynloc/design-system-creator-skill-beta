# DOCX Renderer

DOCX is a long-form reading and editing medium, not a screenshot of a webpage.

## Required adaptation
- Create named styles: Title, Subtitle, H1/H2/H3, Body, Caption, Quote, List, Table Header/Body, Note.
- Resolve page size, margins, baseline rhythm, line spacing, paragraph spacing, widow/orphan/page-break behavior.
- Preserve editable text and semantic headings; use actual tables, captions, page numbers, header/footer where appropriate.
- Prefer typographic hierarchy, rules and whitespace to web-card decoration.
- Apply Kernel color sparingly: headings, rules, table semantics, callouts—not every paragraph.
- Images: consistent crop/caption/credit; avoid low-resolution stretching.

## Host execution
Use the host's native document/DOCX capability when available. Pass the Resolved Design Context and this spec into that renderer. If no DOCX-capable renderer exists, deliver the structured source/spec and mark artifact generation BLOCKED; never rename HTML/text as `.docx`.

## QA
Open/render the generated DOCX/PDF preview when possible. Check page breaks, style consistency, font substitution, table overflow, image anchors, TOC/page numbers, long Chinese paragraphs and print readability.
