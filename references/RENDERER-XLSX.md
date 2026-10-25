# XLSX Renderer

Spreadsheet design prioritizes correct data semantics, scan efficiency, editability and error resistance.

## Zones
Differentiate input, formula/calculation, output, assumptions, status, totals and notes through semantic styles—not decoration. Define number/date/percentage/currency formats explicitly.

Tables should use clear headers, restrained borders, frozen panes/filters where useful, sensible column widths and consistent alignment. Conditional formats must encode meaning. Charts inherit Kernel typography/color but optimize for data distinction and accessible reading.

## Host execution
Use the host's native spreadsheet/XLSX capability when available, preserving formulas and cell semantics. Without it, provide workbook specification/data tables and mark XLSX generation BLOCKED.

## QA
Open/recalculate workbook where possible; verify formulas, references, formats, hidden cells/sheets, print areas, chart ranges, legends, axes/units and that style never obscures negative/zero/missing values.
