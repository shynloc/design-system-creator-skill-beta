#!/usr/bin/env python3
import argparse,json
REQ=['asset_id','purpose','origin','fallback','alt_text']
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--plan',required=True);ap.add_argument('--production',action='store_true');a=ap.parse_args();o=json.loads(open(a.plan,encoding='utf-8').read());items=o.get('assets',o if isinstance(o,list) else []);errors=[]
    for i,x in enumerate(items):
        miss=[k for k in REQ if not x.get(k)]
        if miss: errors.append({'index':i,'missing':miss})
        if a.production and x.get('origin') in ['unknown','generated-external','licensed-stock'] and not x.get('source_or_license'): errors.append({'index':i,'rights':'source_or_license required'})
    print(json.dumps({'status':'PASS' if not errors else 'FAIL','errors':errors},ensure_ascii=False)); return 0 if not errors else 1
if __name__=='__main__': raise SystemExit(main())
