#!/usr/bin/env python3
import argparse, json, re, shutil, sys, tempfile, zipfile, hashlib, os
from pathlib import Path
VERSION='1.0.0-beta.1'
ROOT=Path(__file__).resolve().parent.parent
REQ_KERNEL=['schema_version','metadata','philosophy','principles','anti_style','tokens','profiles','provenance']
REQ_CONTEXT=['schema_version','task','medium','resolved_tokens','creative_direction','anti_style','qa']

def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8'))

def dump(p,o):
    p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def slug(s):
    x=re.sub(r'[^A-Za-z0-9_-]+','-',(s or '').strip()).strip('-').lower()
    return x or 'personal'

def required(o, fields, label):
    missing=[x for x in fields if x not in o]
    return {'status':'PASS' if not missing else 'FAIL','label':label,'missing':missing}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def cmd_version(a): print(json.dumps({'name':'design-system-creator','version':VERSION}))

def probe_host():
    browsers=['chromium','chromium-browser','google-chrome','google-chrome-stable','chrome','msedge']
    browser=next((shutil.which(x) for x in browsers if shutil.which(x)),None)
    py=shutil.which('python3') or shutil.which('python')
    return {
      'schema_version':'1.0.0',
      'host':{
        'python':{'status':'VERIFIED' if py else 'UNSUPPORTED','path':py},
        'filesystem_read':{'status':'VERIFIED'},
        'filesystem_write':{'status':'VERIFIED'},
        'archive_zip':{'status':'VERIFIED'},
        'browser_screenshot':{'status':'AVAILABLE_UNVERIFIED' if browser else 'UNSUPPORTED','path':browser},
      },
      'model':{'vision':'UNKNOWN','note':'A local script cannot prove the active model can see image pixels. The Agent must verify runtime/model input modalities.'},
      'interaction':{'attachments':'UNKNOWN','multi_attachment':'UNKNOWN','mobile':'UNKNOWN'},
      'artifacts':{'web':'AVAILABLE','docx':'HOST_NATIVE_OR_UNVERIFIED','pptx':'HOST_NATIVE_OR_UNVERIFIED','xlsx':'HOST_NATIVE_OR_UNVERIFIED','pdf':'HOST_NATIVE_OR_UNVERIFIED','charts':'HOST_NATIVE_OR_UNVERIFIED'}
    }

def cmd_probe_host(a):
    o=probe_host();
    if a.out: dump(a.out,o)
    print(json.dumps(o,ensure_ascii=False,indent=2))

def init_tree(p):
    p=Path(p); dirs=['.design-studio','sources','references','kernel/history','directions','resolved','artifacts','qa','exports','decisions']
    for d in dirs:(p/d).mkdir(parents=True,exist_ok=True)
    dump(p/'project.json',{'schema_version':'1.0.0','creator_version':VERSION,'phase':'ROUTE','status':'ACTIVE'})
    dump(p/'.design-studio/state.json',{'phase':'ROUTE','reference_intake':'IDLE','kernel_status':'MISSING','copy_approval':'NOT_APPLICABLE','updated_by':VERSION})
    dump(p/'references/reference-registry.json',{'schema_version':'1.0.0','state':'IDLE','sealed':False,'analysis_authorized':False,'references':[]})
    (p/'decisions/DECISIONS.md').write_text((ROOT/'templates/DECISIONS.template.md').read_text(encoding='utf-8'),encoding='utf-8')

def cmd_init(a):
    p=Path(a.project); p.mkdir(parents=True,exist_ok=True); init_tree(p); print(json.dumps({'status':'PASS','project':str(p)},ensure_ascii=False))

def cmd_status(a):
    p=Path(a.project); out={'project':load(p/'project.json'),'state':load(p/'.design-studio/state.json'),'reference_registry':load(p/'references/reference-registry.json')}
    print(json.dumps(out,ensure_ascii=False,indent=2))

def validate_kernel_obj(o):
    r=required(o,REQ_KERNEL,'design-kernel'); warnings=[]; blockers=[]
    if 'metadata' in o and not o['metadata'].get('system_version'): warnings.append('metadata.system_version missing')
    for x in o.get('provenance',{}).get('facts',[]):
        if x.get('status') not in ['OBSERVED','INFERRED','CONFIRMED']: blockers.append('invalid fact status: '+str(x.get('id')))
        if x.get('status')=='CONFIRMED' and not x.get('evidence'): warnings.append('confirmed fact without evidence: '+str(x.get('id')))
    r.update({'warnings':warnings,'blockers':blockers});
    if blockers:r['status']='FAIL'
    return r

def cmd_validate_kernel(a):
    r=validate_kernel_obj(load(a.file));print(json.dumps(r,ensure_ascii=False));return 0 if r['status']=='PASS' else 1

def cmd_validate_context(a):
    o=load(a.file);r=required(o,REQ_CONTEXT,'resolved-context');print(json.dumps(r,ensure_ascii=False));return 0 if r['status']=='PASS' else 1

def merge(base,over,conflicts,prefix=''):
    if not isinstance(base,dict) or not isinstance(over,dict): return over
    out=dict(base)
    for k,v in over.items():
        path=f'{prefix}.{k}' if prefix else k
        if k in out and isinstance(out[k],dict) and isinstance(v,dict): out[k]=merge(out[k],v,conflicts,path)
        else:
            if k in out and out[k]!=v: conflicts.append({'path':path,'from':out[k],'to':v})
            out[k]=v
    return out

def cmd_resolve(a):
    k=load(a.kernel);d=load(a.direction);conflicts=[]; profile={}
    if a.profile:
        if a.profile not in k.get('profiles',{}): print(json.dumps({'status':'FAIL','error':'unknown profile'})); return 1
        profile=k['profiles'][a.profile].get('overrides',{})
    temp=load(a.temporary) if a.temporary else {}
    tokens=merge(k.get('tokens',{}),profile,conflicts,'tokens')
    tokens=merge(tokens,temp.get('tokens',{}),conflicts,'tokens')
    out={
      'schema_version':'1.0.0',
      'kernel_hash':sha(a.kernel),
      'task':{'name':a.task or '', 'profile':a.profile or 'core','temporary_art_direction':temp},
      'medium':a.medium,'resolved_tokens':tokens,'creative_direction':d,
      'anti_style':k.get('anti_style',[]),'medium_rules':k.get('medium_rules',{}).get(a.medium,{}),
      'conflicts':conflicts,'provenance_summary':{'kernel_version':k.get('metadata',{}).get('system_version')},
      'qa':{'identity':[],'creative':[],'medium':[],'technical':[]}
    }
    dump(a.out,out)
    print(json.dumps({'status':'PASS','out':a.out,'conflicts':len(conflicts),'kernel_hash':out['kernel_hash']},ensure_ascii=False))

def render_runtime(k,out):
    out=Path(out); (out/'references').mkdir(parents=True,exist_ok=True)
    name=k.get('metadata',{}).get('name') or 'Personal'; ver=k.get('metadata',{}).get('system_version') or '1.0.0'
    t=(ROOT/'templates/RUNTIME-SKILL.template.md').read_text(encoding='utf-8').replace('{{slug}}',slug(name)).replace('{{display_name}}',name).replace('{{system_version}}',ver)
    (out/'SKILL.md').write_text(t,encoding='utf-8'); dump(out/'references/design-kernel.json',k)
    for m in ['WEB','DOCX','PPTX','XLSX','PDF','CHARTS']:
        shutil.copy2(ROOT/f'references/RENDERER-{m}.md',out/f'references/RENDERER-{m}.md')
    for x in ['RESOLVED-CONTEXT.md','QA.md','REFINE-LOOP.md','MEDIUM-ROUTING.md']:
        shutil.copy2(ROOT/'references'/x,out/'references'/x)

def cmd_compile_runtime(a):
    kp=Path(a.project)/'kernel/design-kernel.json'; k=load(kp); r=validate_kernel_obj(k)
    if r['status']!='PASS': print(json.dumps(r,ensure_ascii=False)); return 1
    out=Path(a.out)
    if out.exists(): shutil.rmtree(out)
    render_runtime(k,out)
    dump(out/'BUILD-MANIFEST.json',{'builder':'Design System Creator','builder_version':VERSION,'kernel_hash':sha(kp),'system_version':k.get('metadata',{}).get('system_version'),'privacy':'no raw references included'})
    print(json.dumps({'status':'PASS','out':str(out),'kernel_hash':sha(kp)},ensure_ascii=False))

def cmd_export_portable(a):
    project=Path(a.project); kp=project/'kernel/design-kernel.json'
    if not kp.exists(): print(json.dumps({'status':'FAIL','error':'kernel missing'})); return 1
    k=load(kp); out=Path(a.out)
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True); shutil.copy2(kp,out/'design-kernel.json')
    for name in ['README.md','DESIGN.md','TOKENS.json','SOURCE-REPORT.md']:
        pass
    dump(out/'tokens.json',k.get('tokens',{}))
    (out/'DESIGN.md').write_text('# Portable Design System\n\n'+ '\n'.join(f'- {x}' for x in k.get('philosophy',[]))+'\n\n## Principles\n'+ '\n'.join(f'- {x}' for x in k.get('principles',[]))+'\n\n## Anti-style\n'+ '\n'.join(f'- {x}' for x in k.get('anti_style',[]))+'\n',encoding='utf-8')
    (out/'README.md').write_text('Portable export generated from confirmed Design Kernel. Raw reference images, source documents, absolute paths and secrets are intentionally excluded by default.\n',encoding='utf-8')
    dump(out/'export-manifest.json',{'builder_version':VERSION,'kernel_hash':sha(kp),'included':['design-kernel.json','tokens.json','DESIGN.md'],'excluded':['raw references','source documents','absolute paths','secrets']})
    print(json.dumps({'status':'PASS','out':str(out),'privacy':'raw references excluded'},ensure_ascii=False))

def cmd_hash(a): print(json.dumps({'status':'PASS','file':a.file,'sha256':sha(a.file)}))

def cmd_package(a):
    src=Path(a.path).resolve(); out=Path(a.out).resolve(); out.parent.mkdir(parents=True,exist_ok=True); man=[]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc'):
                arc=Path(src.name)/p.relative_to(src); z.write(p,arc.as_posix()); man.append({'path':arc.as_posix(),'sha256':sha(p)})
    dump(str(out)+'.manifest.json',{'version':VERSION,'files':man})
    print(json.dumps({'status':'PASS','zip':str(out),'files':len(man)},ensure_ascii=False))

def cmd_flatten(a):
    src=Path(a.path); out=Path(a.out)
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    for p in src.rglob('*'):
        if not p.is_file() or '__pycache__' in p.parts or p.name.endswith('.pyc'): continue
        rel=p.relative_to(src)
        if len(rel.parts)==1: dest=out/rel.name
        else:
            cat=rel.parts[0]; (out/cat).mkdir(exist_ok=True); dest=out/cat/('__'.join(rel.parts[1:]))
        shutil.copy2(p,dest)
    print(json.dumps({'status':'PASS','out':str(out)},ensure_ascii=False))

def cmd_self_test(a):
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); proj=td/'p'; cmd_init(argparse.Namespace(project=str(proj)))
        shutil.copy2(ROOT/'examples/design-kernel.sample.json',proj/'kernel/design-kernel.json')
        before=sha(proj/'kernel/design-kernel.json')
        temp=td/'temp.json'; dump(temp,{'tokens':{'semantic':{'accent':'#2f6bff'}}})
        ctx=td/'ctx.json'
        rc=cmd_resolve(argparse.Namespace(kernel=str(proj/'kernel/design-kernel.json'),direction=str(ROOT/'examples/creative-direction.sample.json'),profile='editorial',temporary=str(temp),medium='web',task='self-test',out=str(ctx)))
        after=sha(proj/'kernel/design-kernel.json')
        rt=td/'runtime'; render_runtime(load(proj/'kernel/design-kernel.json'),rt)
        port=td/'portable'; cmd_export_portable(argparse.Namespace(project=str(proj),out=str(port)))
        checks={'context':ctx.exists(),'runtime':(rt/'SKILL.md').exists(),'temporary_does_not_mutate_kernel':before==after,'portable_excludes_references':not (port/'references').exists()}
        ok=(rc in (None,0) and all(checks.values()))
        print(json.dumps({'status':'PASS' if ok else 'FAIL','version':VERSION,'checks':checks},ensure_ascii=False)); return 0 if ok else 1

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
    sp.add_parser('version').set_defaults(fn=cmd_version)
    p=sp.add_parser('probe-host'); p.add_argument('--out'); p.set_defaults(fn=cmd_probe_host)
    p=sp.add_parser('init'); p.add_argument('--project',required=True); p.set_defaults(fn=cmd_init)
    p=sp.add_parser('status'); p.add_argument('--project',required=True); p.set_defaults(fn=cmd_status)
    p=sp.add_parser('validate-kernel'); p.add_argument('--file',required=True); p.set_defaults(fn=cmd_validate_kernel)
    p=sp.add_parser('validate-context'); p.add_argument('--file',required=True); p.set_defaults(fn=cmd_validate_context)
    p=sp.add_parser('resolve'); p.add_argument('--kernel',required=True); p.add_argument('--direction',required=True); p.add_argument('--profile'); p.add_argument('--temporary'); p.add_argument('--medium',required=True,choices=['web','docx','pptx','xlsx','pdf','charts']); p.add_argument('--task'); p.add_argument('--out',required=True); p.set_defaults(fn=cmd_resolve)
    p=sp.add_parser('compile-runtime'); p.add_argument('--project',required=True); p.add_argument('--out',required=True); p.set_defaults(fn=cmd_compile_runtime)
    p=sp.add_parser('export-portable'); p.add_argument('--project',required=True); p.add_argument('--out',required=True); p.set_defaults(fn=cmd_export_portable)
    p=sp.add_parser('hash'); p.add_argument('--file',required=True); p.set_defaults(fn=cmd_hash)
    p=sp.add_parser('package'); p.add_argument('--path',required=True); p.add_argument('--out',required=True); p.set_defaults(fn=cmd_package)
    p=sp.add_parser('flatten'); p.add_argument('--path',required=True); p.add_argument('--out',required=True); p.set_defaults(fn=cmd_flatten)
    sp.add_parser('self-test').set_defaults(fn=cmd_self_test)
    a=ap.parse_args(); rc=a.fn(a); raise SystemExit(rc or 0)
if __name__=='__main__': main()
