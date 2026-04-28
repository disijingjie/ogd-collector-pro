import sys, json
d = json.load(sys.stdin)
runs = d.get('workflow_runs', [])
for r in runs[:3]:
    name = r['name']
    status = r['status']
    conclusion = r.get('conclusion', 'N/A')
    commit = r['head_commit']['message'][:40]
    print(f'{name} | status={status} | conclusion={conclusion} | commit={commit}')