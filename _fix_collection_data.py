"""
修复采集数据：统一v3_platform_rules.json和v3_collection_results.json
并同步到SQLite数据库
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

# 文件路径
RULES_PATH = Path('v3_platform_rules.json')
RESULTS_PATH = Path('data/v3_collection_results.json')
DB_PATH = Path('data/ogd_database.db')

# 读取文件
with open(RULES_PATH, 'r', encoding='utf-8') as f:
    rules = json.load(f)

with open(RESULTS_PATH, 'r', encoding='utf-8') as f:
    results = json.load(f)

# 建立索引
rules_platforms = {p['code']: p for p in rules['platforms']}
results_index = {r['code']: r for r in results}

print("=" * 60)
print("采集数据修复脚本")
print("=" * 60)
print(f"规则文件平台数: {len(rules_platforms)}")
print(f"结果文件平台数: {len(results_index)}")
print()

# 修复规则：
# 1. 优先使用rules中的值（已经过修正验证）
# 2. rules中为null但results中有值，使用results
# 3. 两者都有但不同，优先rules（rules是修正后的）
# 4. 特殊处理：山西保留534（直接采集）而非124（历史数据）

fixed_results = []
changes = []

for code, rule_platform in rules_platforms.items():
    rule_count = rule_platform['dataset_count']['value']
    result_data = results_index.get(code, {})
    result_count = result_data.get('dataset_count')
    
    # 决策逻辑
    if rule_count is not None and rule_count != result_count:
        # rules有值，优先使用
        final_count = rule_count
        final_type = rule_platform['dataset_count']['type']
        final_confidence = rule_platform['dataset_count']['confidence']
        final_source = rule_platform['dataset_count'].get('source_url', result_data.get('source_url'))
        final_text = rule_platform['dataset_count'].get('source_text', result_data.get('source_text'))
        final_method = 'confirmed:rules_override'
        final_note = rule_platform['dataset_count'].get('verification', '')
        if result_count is not None:
            changes.append(f"  {code}: {result_count} -> {final_count} (使用rules修正值)")
    elif rule_count is None and result_count is not None:
        # rules无值，使用results
        final_count = result_count
        final_type = result_data.get('type', '数据集')
        final_confidence = result_data.get('confidence', 'medium')
        final_source = result_data.get('source_url')
        final_text = result_data.get('source_text')
        final_method = result_data.get('method', 'unknown')
        final_note = result_data.get('note', '')
        changes.append(f"  {code}: null -> {final_count} (使用results补充值)")
    elif rule_count is not None:
        # 两者一致
        final_count = rule_count
        final_type = rule_platform['dataset_count']['type']
        final_confidence = rule_platform['dataset_count']['confidence']
        final_source = rule_platform['dataset_count'].get('source_url', result_data.get('source_url'))
        final_text = rule_platform['dataset_count'].get('source_text', result_data.get('source_text'))
        final_method = result_data.get('method', 'confirmed:rules')
        final_note = rule_platform['dataset_count'].get('verification', '')
    else:
        # 两者都无值
        final_count = None
        final_type = '待确认'
        final_confidence = 'low'
        final_source = None
        final_text = None
        final_method = 'pending'
        final_note = '未找到数据集数量'
    
    # 构建标准化结果
    fixed = {
        'code': code,
        'name': rule_platform['name'],
        'province': rule_platform['province'],
        'dataset_count': final_count,
        'type': final_type,
        'confidence': final_confidence,
        'status': 'success' if final_count is not None else 'not_found',
        'method': final_method,
        'source_url': final_source,
        'source_text': final_text,
        'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'note': final_note
    }
    fixed_results.append(fixed)

# 打印变更
print("数据变更记录:")
print("-" * 60)
for change in changes:
    print(change)
print(f"\n共 {len(changes)} 处变更")
print()

# 统计信息
success_count = sum(1 for r in fixed_results if r['dataset_count'] is not None)
null_count = sum(1 for r in fixed_results if r['dataset_count'] is None)
print(f"修复后统计:")
print(f"  有数据: {success_count} 个平台")
print(f"  无数据: {null_count} 个平台")
print()

# 按数据集数量排序显示
sorted_results = sorted([r for r in fixed_results if r['dataset_count'] is not None], 
                        key=lambda x: x['dataset_count'], reverse=True)
print("数据集数量排名（Top 10）:")
print("-" * 60)
for i, r in enumerate(sorted_results[:10], 1):
    print(f"  {i:2d}. {r['name']:<10s} {r['dataset_count']:>8,} {r['type']}")
print()

# 显示无数据的平台
null_platforms = [r for r in fixed_results if r['dataset_count'] is None]
if null_platforms:
    print("无数据平台（需要进一步处理）:")
    print("-" * 60)
    for r in null_platforms:
        print(f"  - {r['name']} ({r['code']})")
    print()

# 保存修复后的结果
with open(RESULTS_PATH, 'w', encoding='utf-8') as f:
    json.dump(fixed_results, f, ensure_ascii=False, indent=2)
print(f"已保存: {RESULTS_PATH}")

# 同时更新rules文件中的dataset_count
update_count = 0
for code, result in results_index.items():
    if code in rules_platforms and result.get('dataset_count') is not None:
        rule_platform = rules_platforms[code]
        if rule_platform['dataset_count']['value'] is None:
            rule_platform['dataset_count']['value'] = result['dataset_count']
            rule_platform['dataset_count']['type'] = result.get('type', '数据集')
            rule_platform['dataset_count']['confidence'] = result.get('confidence', 'medium')
            rule_platform['dataset_count']['source_url'] = result.get('source_url')
            rule_platform['dataset_count']['source_text'] = result.get('source_text')
            rule_platform['dataset_count']['collected_at'] = datetime.now().strftime('%Y-%m-%d')
            rule_platform['dataset_count']['verification'] = result.get('note', '')
            update_count += 1

# 保存更新后的rules
with open(RULES_PATH, 'w', encoding='utf-8') as f:
    json.dump(rules, f, ensure_ascii=False, indent=2)
print(f"已更新: {RULES_PATH} ({update_count} 个平台补充了数据)")

# 同步到SQLite数据库
print()
print("=" * 60)
print("同步到SQLite数据库")
print("=" * 60)

if DB_PATH.exists():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    # 更新collection_records表中的dataset_count
    updated = 0
    skipped = 0
    for r in fixed_results:
        cursor.execute("SELECT id FROM collection_records WHERE platform_code = ?", (r['code'],))
        row = cursor.fetchone()
        if row:
            cursor.execute("""
            UPDATE collection_records 
            SET dataset_count = ?, status = ?, collected_at = ?
            WHERE platform_code = ?
            """, (
                r['dataset_count'],
                'success' if r['dataset_count'] is not None else 'not_found',
                r['collected_at'],
                r['code']
            ))
            updated += cursor.rowcount
        else:
            skipped += 1
    
    conn.commit()
    conn.close()
    print(f"数据库已更新: {DB_PATH}")
    print(f"  更新 {updated} 条记录")
    if skipped > 0:
        print(f"  跳过 {skipped} 个平台（数据库中无对应记录）")
else:
    print(f"数据库不存在: {DB_PATH}，跳过同步")

print()
print("=" * 60)
print("修复完成")
print("=" * 60)
