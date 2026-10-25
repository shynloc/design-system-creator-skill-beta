#!/usr/bin/env python3
from pathlib import Path
import hashlib,sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve(); rows=[]
for p in sorted(root.rglob('*')):
    if p.is_file() and p.name!='SHA256SUMS.txt': rows.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}')
(root/'SHA256SUMS.txt').write_text('\n'.join(rows)+'\n',encoding='utf-8'); print(len(rows))
