import json

# 加载已有结果
with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# 添加第三方数据源
third_party = [
    {'code': 'shanghai', 'name': '上海市', 'dataset_count': 10753, 'type': '数据集', 'confidence': 'high', 'status': 'success', 'method': 'third_party:官方统计', 'source_url': 'https://data.sh.gov.cn/old/', 'note': '上海市公共数据开放平台官方统计：10,753个数据集'},
    {'code': 'zhejiang', 'name': '浙江省', 'dataset_count': 38000, 'type': '公共数据集', 'confidence': 'high', 'status': 'success', 'method': 'third_party:政府发布会', 'source_url': 'https://www.cls.cn/detail/2149055', 'note': '浙江省数据局副局长吴旭升，2025年9月18日新闻发布会'},
    {'code': 'tianjin', 'name': '天津市', 'dataset_count': 3344, 'type': '数据集', 'confidence': 'high', 'status': 'success', 'method': 'third_party:官方报告', 'source_url': 'https://tjdsj.tjcac.gov.cn/', 'note': '天津数港2023年4月报告：3,344个数据集'},
]

# 更新或添加
existing_codes = {r['code'] for r in results}
for tp in third_party:
    if tp['code'] in existing_codes:
        for i, r in enumerate(results):
            if r['code'] == tp['code']:
                results[i] = tp
                break
    else:
        results.append(tp)

# 保存
with open('data/v3_collection_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 统计
success = sum(1 for r in results if r['status'] == 'success')
print(f'总计成功采集: {success}/23个平台')
print()
print('所有成功平台（按数量排序）:')
for r in sorted(results, key=lambda x: x['dataset_count'] or 0, reverse=True):
    if r['status'] == 'success':
        source_type = '[自主]' if 'confirmed' in r.get('method', '') or 'homepage' in r.get('method', '') or 'dataset_page' in r.get('method', '') else '[第三方]'
        print(f'  {source_type} {r["name"]:12s}: {r["dataset_count"]:8,} | {r.get("type", ""):10s} | {r.get("method", "")}')
