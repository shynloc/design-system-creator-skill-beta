#!/usr/bin/env python3
import argparse,json,shutil,subprocess,os
from pathlib import Path
BROWSERS=['chromium','chromium-browser','google-chrome','google-chrome-stable','chrome','msedge']
def browser():
    return next((shutil.which(b) for b in BROWSERS if shutil.which(b)),None)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--html',required=True); ap.add_argument('--out',required=True); a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True); hp=Path(a.html).resolve()
    t=hp.read_text(encoding='utf-8',errors='replace'); issues=[]
    if 'viewport' not in t: issues.append('missing viewport meta')
    if '<!doctype html>' not in t.lower() and '<html' not in t.lower(): issues.append('missing html/doctype')
    b=browser(); report={'structural':{'status':'PASS' if not issues else 'WARNING','issues':issues},'browser':{'status':'BLOCKED','reason':'no browser found' if not b else 'not attempted'},'screenshots':[]}
    if b:
        ok_all=True; attempts=[]
        for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
            p=out/f'{name}.png'; cmd=[b,'--headless','--disable-gpu','--disable-dev-shm-usage','--hide-scrollbars',f'--window-size={w},{h}',f'--screenshot={p}',hp.as_uri()]
            if hasattr(os,'geteuid') and os.geteuid()==0: cmd.insert(2,'--no-sandbox')
            try:
                q=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=6)
                ok=q.returncode==0 and p.exists() and p.stat().st_size>0
                err=(q.stderr or '')[-600:]
            except subprocess.TimeoutExpired:
                ok=False; err='browser screenshot timed out'
            ok_all &= ok
            attempts.append({'id':name,'status':'PASS' if ok else 'BLOCKED','path':str(p) if ok else None,'note':err if not ok else None})
        report['screenshots']=attempts
        report['browser']={'status':'PASS' if ok_all else 'BLOCKED','executable':b,'reason':None if ok_all else 'browser exists but screenshot runtime is unavailable or timed out'}
    (out/'visual-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False)); return 0
if __name__=='__main__': raise SystemExit(main())
