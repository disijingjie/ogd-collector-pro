import json

with open('data/v3_collection_results.json', 'r', encoding='utf-8') as f:
    v3 = json.load(f)

print("=== v3采集结果 ===")
print(f"{'平台':<15} {'数据集数':<10} {'类型':<15} {'置信度':<8} {'状态':<10}")
for item in v3:
    print(f"{item['code']:<15} {str(item['dataset_count']):<10} {item.get('type',''):<15} {item.get('confidence',''):<8} {item.get('status',''):<10}")
