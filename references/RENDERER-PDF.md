# PDF Renderer

PDF is normally a final delivery layer derived from DOCX, PPTX or HTML/print layout. Preserve the source medium's semantics rather than inventing a separate visual identity.

Check page size, margins/bleed if relevant, font embedding/substitution, vector/raster quality, link behavior, page numbering, bookmarks where appropriate, accessibility/tagging where supported, and print-safe contrast.

Use a real PDF generation/render path. Visually inspect representative pages. If PDF creation cannot be executed, state BLOCKED instead of producing a fake extension.
