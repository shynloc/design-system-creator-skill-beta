#!/usr/bin/env python3
from pathlib import Path
import hashlib,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); rows=[]
for p in sorted(root.rglob('*')):
    rel=p.relative_to(root) if p.exists() else None
    if not p.is_file() or p.name=='SHA256SUMS.txt': continue
    if '.git' in rel.parts or '__pycache__' in rel.parts or p.suffix=='.pyc': continue
    rows.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {rel.as_posix()}')
(root/'SHA256SUMS.txt').write_text('\n'.join(rows)+'\n',encoding='utf-8'); print(len(rows))
