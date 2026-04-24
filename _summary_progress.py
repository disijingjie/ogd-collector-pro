import json

# 读取第一轮结果
with open('data/platform_analysis_v2.json', 'r', encoding='utf-8') as f:
    v2 = json.load(f)

# 读取深度采集结果
with open('data/deep_collect_results.json', 'r', encoding='utf-8') as f:
    deep = json.load(f)

# 读取验证结果
with open('data/verification_results.json', 'r', encoding='utf-8') as f:
    verify = json.load(f)

# 构建最终确认表
confirmed = {}

# 第一轮已确认的（需修正）
for r in v2:
    if r.get('dataset_count_homepage'):
        confirmed[r['code']] = {
            'name': r['name'],
            'value': r['dataset_count_homepage'],
            'source': 'homepage_v2',
            'confidence': 'medium'
        }

# 深度采集成功的
depp_map = {r['code']: r for r in deep if r['status'] == 'success'}

# 验证结果
verify_map = {r['code']: r for r in verify if r['status'] == 'success'}

# 人工修正
confirmed['chongqing'] = {'name': '重庆市', 'value': 22550, 'source': 'homepage_verified', 'confidence': 'high'}
confirmed['liaoning'] = {'name': '辽宁省', 'value': 4120, 'source': 'homepage_verified', 'confidence': 'high', 'note': '数据目录数'}

# 深度采集中确认的湖南
if 'hunan' in depp_map:
    confirmed['hunan'] = {'name': '湖南省', 'value': 634, 'source': 'dataset_page', 'confidence': 'high'}

# 福建：第一轮4851，验证未找到，需要进一步验证
if 'fujian' in confirmed:
    confirmed['fujian']['confidence'] = 'low'
    confirmed['fujian']['note'] = '需验证，CSS选择器.num提取，无明确上下文'

# 四川：第一轮3465为访问次数，验证未找到
deep_sichuan = depp_map.get('sichuan')
if deep_sichuan:
    confirmed['sichuan'] = {'name': '四川省', 'value': deep_sichuan['dataset_count'], 'source': 'dataset_page', 'confidence': 'low', 'note': '疑似访问次数，需进一步验证'}

# 广西：第一轮10037为访问次数
deep_guangxi = depp_map.get('guangxi')
if deep_guangxi:
    confirmed['guangxi'] = {'name': '广西壮族自治区', 'value': deep_guangxi['dataset_count'], 'source': 'dataset_page', 'confidence': 'low', 'note': '疑似访问次数，需进一步验证'}

print('=' * 80)
print('省级平台数据集数量采集状态（截至2026-04-25 第一轮）')
print('=' * 80)
print()
print('%-12s | %-8s | %-10s | %s' % ('平台', '数量', '置信度', '说明'))
print('-' * 80)

codes = ['beijing', 'tianjin', 'hebei', 'shanxi', 'neimenggu', 'liaoning', 'jilin', 'heilongjiang',
         'shanghai', 'jiangsu', 'zhejiang', 'anhui', 'fujian', 'jiangxi', 'shandong', 'henan',
         'hubei', 'hunan', 'guangdong', 'guangxi', 'hainan', 'chongqing', 'sichuan', 'guizhou',
         'yunnan', 'shaanxi', 'gansu', 'qinghai', 'ningxia', 'xinjiang', 'xizang']

for code in codes:
    if code in confirmed:
        c = confirmed[code]
        note = c.get('note', '')
        print('%-12s | %-8s | %-10s | %s' % (c['name'], c['value'], c['confidence'], note))
    else:
        name = code
        for r in v2:
            if r['code'] == code:
                name = r['name']
                break
        for r in v2:
            if r['code'] == code and r['status'] == 'error':
                print('%-12s | %-8s | %-10s | %s' % (name, 'N/A', 'URL失效', r.get('error', '')[:30]))
                break
        else:
            print('%-12s | %-8s | %-10s | %s' % (name, 'N/A', '未找到', ''))

print()
print('=' * 80)
high_conf = sum(1 for c in confirmed.values() if c['confidence'] == 'high')
medium_conf = sum(1 for c in confirmed.values() if c['confidence'] == 'medium')
low_conf = sum(1 for c in confirmed.values() if c['confidence'] == 'low')
print('高置信度: %d | 中置信度: %d | 低置信度: %d | 未找到/失效: %d' % (
    high_conf, medium_conf, low_conf, 31 - len(confirmed)))
print('=' * 80)
