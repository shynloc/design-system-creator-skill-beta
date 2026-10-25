#!/usr/bin/env python3
import json, subprocess, tempfile, shutil, zipfile, hashlib, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PY=sys.executable
results=[]
def run(name,fn):
    try:
        detail=fn(); results.append({'name':name,'status':'PASS','detail':detail})
    except Exception as e:
        results.append({'name':name,'status':'FAIL','detail':str(e)})
def cmd(*args):
    q=subprocess.run([PY,*map(str,args)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=60)
    if q.returncode: raise RuntimeError((q.stderr or q.stdout).strip())
    return q.stdout.strip()
def t_no_excluded_project():
    hits=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and p.suffix in {'.md','.json','.py'}:
            forbidden='A'+'CKS'
            if forbidden in p.read_text(encoding='utf-8',errors='ignore'): hits.append(str(p.relative_to(ROOT)))
    if hits: raise AssertionError('project-specific content found: '+','.join(hits))
    return 'none found'
def t_compile():
    for p in (ROOT/'scripts').glob('*.py'):
        subprocess.run([PY,'-m','py_compile',str(p)],check=True)
    return 'all scripts compile'
def t_self(): return cmd('scripts/design_studio.py','self-test').splitlines()[-1]
def t_kernel(): return cmd('scripts/design_studio.py','validate-kernel','--file','examples/design-kernel.sample.json')
def t_pitch():
    with tempfile.TemporaryDirectory() as td:
        cmd('scripts/build_visual_pitch.py','--brief','examples/visual-pitch-brief.sample.json','--out',td)
        files=[Path(td)/f'{x}.html' for x in ['editorial','architecture','utility']]
        if not all(x.exists() for x in files): raise AssertionError('missing variants')
        hashes={hashlib.sha256(x.read_bytes()).hexdigest() for x in files}
        if len(hashes)!=3: raise AssertionError('visual pitch variants are not materially separate files')
        manifest=json.loads((Path(td)/'pitch-manifest.json').read_text())
        if len(manifest.get('variants',[]))!=3: raise AssertionError('manifest variants != 3')
        return '3 distinct HTML candidates + manifest'
def t_runtime():
    with tempfile.TemporaryDirectory() as td:
        proj=Path(td)/'project'; rt=Path(td)/'runtime'; z=Path(td)/'runtime.zip'
        cmd('scripts/design_studio.py','init','--project',proj)
        shutil.copy2(ROOT/'examples/design-kernel.sample.json',proj/'kernel/design-kernel.json')
        cmd('scripts/design_studio.py','compile-runtime','--project',proj,'--out',rt)
        cmd('scripts/design_studio.py','package','--path',rt,'--out',z)
        with zipfile.ZipFile(z) as q:
            if q.testzip() is not None: raise AssertionError('corrupt runtime zip')
            names=q.namelist()
        if not any(x.endswith('/SKILL.md') for x in names): raise AssertionError('runtime SKILL missing')
        return f'runtime package OK ({len(names)} files)'
def t_portable_privacy():
    with tempfile.TemporaryDirectory() as td:
        proj=Path(td)/'project'; out=Path(td)/'portable'
        cmd('scripts/design_studio.py','init','--project',proj)
        shutil.copy2(ROOT/'examples/design-kernel.sample.json',proj/'kernel/design-kernel.json')
        (proj/'references/private-photo.jpg').write_bytes(b'private-placeholder')
        (proj/'sources/private.txt').write_text('private source')
        cmd('scripts/design_studio.py','export-portable','--project',proj,'--out',out)
        names={p.name for p in out.rglob('*') if p.is_file()}
        if 'private-photo.jpg' in names or 'private.txt' in names: raise AssertionError('private source leaked')
        return 'raw refs/sources excluded'
def t_temp_immutability():
    with tempfile.TemporaryDirectory() as td:
        k=Path(td)/'kernel.json'; shutil.copy2(ROOT/'examples/design-kernel.sample.json',k); before=hashlib.sha256(k.read_bytes()).hexdigest()
        ctx=Path(td)/'ctx.json'
        cmd('scripts/design_studio.py','resolve','--kernel',k,'--direction','examples/creative-direction.sample.json','--profile','editorial','--temporary','examples/temporary-direction.sample.json','--medium','pptx','--task','temporary-style-test','--out',ctx)
        after=hashlib.sha256(k.read_bytes()).hexdigest()
        if before!=after: raise AssertionError('kernel mutated')
        obj=json.loads(ctx.read_text())
        if obj.get('kernel_hash')!=before: raise AssertionError('context kernel hash mismatch')
        return 'kernel hash unchanged'
def t_intake_protocol():
    t=(ROOT/'references/REFERENCE-INTAKE.md').read_text()
    for token in ['COLLECTING','上传完成','开始分析']:
        if token not in t: raise AssertionError('missing '+token)
    return 'explicit seal + commit present'
def t_vision_guard():
    t=(ROOT/'references/CAPABILITY-GATE.md').read_text()
    required=['VISION_UNKNOWN','VISION_UNSUPPORTED','不得描述附件图片内容']
    for token in required:
        if token not in t: raise AssertionError('missing '+token)
    return 'vision anti-hallucination guard present'

def t_visual_qa_blocked():
    with tempfile.TemporaryDirectory() as td:
        pitch=Path(td)/'pitch'; qa=Path(td)/'qa'
        cmd('scripts/build_visual_pitch.py','--brief','examples/visual-pitch-brief.sample.json','--out',pitch)
        q=subprocess.run([PY,str(ROOT/'scripts/visual_qa.py'),'--html',str(pitch/'editorial.html'),'--out',str(qa)],cwd=ROOT,env={'PATH':''},stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=20)
        if q.returncode: raise AssertionError(q.stderr)
        obj=json.loads((qa/'visual-qa.json').read_text())
        if obj['browser']['status']!='BLOCKED': raise AssertionError('browser without executable must be BLOCKED')
        if obj['structural']['status'] not in ('PASS','WARNING'): raise AssertionError('structural check missing')
        return 'missing browser is reported BLOCKED, not PASS'
def t_flatten():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'flat'
        cmd('scripts/design_studio.py','flatten','--path',ROOT,'--out',out)
        depth=max(len(p.relative_to(out).parts) for p in out.rglob('*') if p.is_file())
        if depth>2: raise AssertionError(f'flatten depth {depth} > 2')
        return f'max file depth={depth}'
def t_asset(): return cmd('scripts/validate_asset_plan.py','--plan','examples/asset-plan.sample.json','--production')
for n,f in [
 ('no-excluded-project-style',t_no_excluded_project),('python-compile',t_compile),('self-test',t_self),('sample-kernel-validation',t_kernel),
 ('visual-pitch',t_pitch),('runtime-compiler',t_runtime),('portable-privacy',t_portable_privacy),('temporary-immutability',t_temp_immutability),
 ('reference-intake-protocol',t_intake_protocol),('vision-guard',t_vision_guard),('visual-qa-blocked',t_visual_qa_blocked),('two-level-flatten',t_flatten),('asset-plan',t_asset)]: run(n,f)
summary={'version':'1.0.0-beta.1','passed':sum(x['status']=='PASS' for x in results),'failed':sum(x['status']=='FAIL' for x in results),'results':results}
print(json.dumps(summary,ensure_ascii=False,indent=2))
raise SystemExit(1 if summary['failed'] else 0)
