import json

# 加载已有结果
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# 更新江苏数据
for i, r in enumerate(results):
    if r['code'] == 'jiangsu':
        results[i] = {
            'code': 'jiangsu',
            'name': '江苏省',
            'dataset_count': 644,
            'type': '数据目录',
            'confidence': 'high',
            'status': 'success',
            'method': 'homepage:新URL访问',
            'source_url': 'https://data.jszwfw.gov.cn:8118/extranet/openportal/pages/default/index.html',
            'note': '通过新URL成功访问，数据目录总量644个，省级数据总量16975.2万条',
            'collected_at': '2026-04-25 11:35:00'
        }
        break

# 更新河南数据
for i, r in enumerate(results):
    if r['code'] == 'henan':
        results[i] = {
            'code': 'henan',
            'name': '河南省',
            'dataset_count': 931,
            'type': '数据产品',
            'confidence': 'medium',
            'status': 'success',
            'method': 'dataset_page:产品中心',
            'source_url': 'https://hndataops.com/portal/product',
            'note': '平台转型为运营服务平台，统计的是数据产品数量（约931个），由公司承接运营',
            'collected_at': '2026-04-25 11:35:00'
        }
        break

# 保存
with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

success_count = sum(1 for r in results if r['status'] == 'success')
print(f'总计成功: {success_count}/23个平台')

print('\n所有成功平台（按数量排序）:')
for r in sorted(results, key=lambda x: x['dataset_count'] or 0, reverse=True):
    if r['status'] == 'success':
        source_mark = '[自主]' if 'confirmed' in r.get('method', '') or 'homepage' in r.get('method', '') or 'dataset_page' in r.get('method', '') or 'api' in r.get('method', '') else '[第三方]'
        name = r['name']
        count = r['dataset_count']
        dtype = r.get('type', '')
        method = r.get('method', '')
        print(f'  {source_mark} {name:12s}: {count:8,} | {dtype:10s} | {method}')

print('\n待确认平台:')
for r in results:
    if r['status'] != 'success':
        print(f'  [X] {r["name"]:12s}: {r.get("note", "")}')
