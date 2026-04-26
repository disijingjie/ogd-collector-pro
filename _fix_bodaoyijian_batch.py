# -*- coding: utf-8 -*-
"""
博导意见批量修复脚本 v1.0
处理：术语统一、英文摘要更新、章节编号、数据一致性（22→23等）
"""
import re

md_path = "docs/博士论文_最终定稿版_v10.md"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

orig_len = len(text)
changes = []

# ========== 1. 英文摘要全面更新 ==========
old_abstract = """**Abstract:** Open Government Data (OGD) is an important component of digital government construction and a key pathway for data value release. However, existing evaluation systems suffer from a structural bias of "emphasizing supply over effect," failing to comprehensively measure the actual performance of data openness. Based on the 4E evaluation framework (Supply Assurance-Platform Service-Data Quality-Utilization Effect-Equity), this study constructs an evaluation system covering 5 first-level dimensions, 9 second-level dimensions, and 24 specific indicators. Using AHP-entropy weight combination method to determine indicator weights, and entropy-weighted TOPSIS method to evaluate the comprehensive performance of 22 provincial government data open platforms in China. Meanwhile, DEA-BCC method is used to evaluate resource allocation efficiency, DEMATEL method to identify key influencing factors, and fsQCA method to reveal multiple equivalent paths of high performance. The findings indicate: (1) significant performance differences among 22 platforms, with Sichuan, Beijing, and Liaoning ranking top three; (2) 8 platforms are DEA-efficient, indicating some medium-low performance platforms have high resource allocation efficiency; (3) DEMATEL analysis shows "supply assurance" is the most critical causal factor and "utilization effect" is the key result factor; (4) fsQCA reveals three core configuration paths for high performance. Based on these findings, differentiated optimization strategies and a four-stage quality improvement path are proposed."""

new_abstract = """**Abstract:** Open Government Data (OGD) is an important component of digital government construction and a key pathway for data value release. However, existing evaluation systems suffer from a structural bias of "emphasizing supply over effect," failing to comprehensively measure the actual performance of data openness. Based on the 4E evaluation framework (Supply Assurance-Platform Service-Data Quality-Utilization Effect-Equity), this study constructs an evaluation system covering 5 first-level dimensions, 9 second-level dimensions, and 24 specific indicators. Using AHP-entropy weight combination method to determine indicator weights, and equal-weighted TOPSIS method to evaluate the comprehensive performance of 23 provincial government data open platforms in China. Meanwhile, DEA-BCC method is used to evaluate resource allocation efficiency, DEMATEL method to identify key influencing factors, and fsQCA method to reveal multiple equivalent paths of high performance. The findings indicate: (1) significant performance differences among 23 platforms, with Shandong ranking first (0.955) followed by Sichuan and Liaoning, exhibiting a "head concentration" pattern; (2) only 1 platform (Shandong) is DEA-efficient, indicating that complete correspondence between high performance and high efficiency is extremely rare; (3) DEMATEL analysis reveals that all four dimensions are result factors, forming a networked structure of mutual causality without distinct cause-result hierarchy; (4) fsQCA reveals two core configuration paths for high performance—"full-factor driven" (coverage 81%) and "service-quality-effect driven" (coverage 19%). Based on these findings, differentiated platform optimization strategies and a four-stage quality improvement path are proposed."""

if old_abstract in text:
    text = text.replace(old_abstract, new_abstract)
    changes.append("[必须] 英文摘要全面更新（22→23、排名、DEA、DEMATEL、fsQCA）")
else:
    changes.append("[警告] 英文摘要旧文本未匹配，可能需要手动更新")

# ========== 2. 术语统一：效果导向 vs 效果性 ==========
# "效果性"在4E框架中特指Effectiveness维度，"效果导向"描述评估范式
# 策略：将混用的"效果性"在描述评估范式时改为"效果导向"
# 保持4E维度名称"利用效果"不变

count = text.count("效果性")
# 这个需要上下文判断，先记录
changes.append(f"[建议] 全文出现'效果性' {count} 次，需人工确认使用场景")

# ========== 3. 章节编号统一：删除重复 ==========
# "第1章 第一章" → "第一章"
for i in range(1, 10):
    old = f"第{i}章 第{i}章"
    new = f"第{i}章"
    if old in text:
        text = text.replace(old, new)
        changes.append(f"[必须] 修复章节编号重复：'{old}' → '{new}'")

# ========== 4. 数据一致性：残留22→23 ==========
# 检查可能残留的"22个平台"在分析章节中
# 排除合理的引用（如历史数据、对比数据）
pattern_22 = re.compile(r'22个(?:样本|省级|有效)?平台')
matches = pattern_22.findall(text)
if matches:
    changes.append(f"[警告] 仍发现 {len(matches)} 处'22个平台'残留：{set(matches)}")

# ========== 5. "核心内容" → "重要组成部分"（博导4意见） ==========
count_core = text.count("核心内容")
# 仅替换部分非引用性质的
# 保持引用原文的部分不变
changes.append(f"[建议] 全文'核心内容'出现 {count_core} 次，建议核实后改为'重要组成部分'")

# ========== 6. "价值化释放" → "价值释放"（博导1意见） ==========
count_value = text.count("价值化释放")
if count_value > 0:
    text = text.replace("价值化释放", "价值释放")
    changes.append(f"[必须] 修复'价值化释放'→'价值释放'，共 {count_value} 处")

# ========== 7. 口语化表述检测 ==========
colloquial = ["花小钱办大事", "有劲使错地方", "显然", "无疑", "众所周知"]
for phrase in colloquial:
    count = text.count(phrase)
    if count > 0:
        changes.append(f"[建议] 口语化表述'{phrase}'出现 {count} 次，建议改为学术表述")

# ========== 8. "背离" → "挑战"（博导4意见） ==========
# 仅在特定语境下替换
count_beili = text.count('"背离"')
if count_beili > 0:
    changes.append(f"[建议] 情绪化表述'背离'出现 {count_beili} 次，建议改为'挑战'")

# ========== 9. 概念混淆：OGD与数字政府关系 ==========
changes.append("[建议] 核实OGD与'数字政府'的关系表述，明确OGD是数字政府的子集/组成部分")

# ========== 10. FAIR原则引用缺失（博导2意见） ==========
if "Wilkinson" in text:
    changes.append("[建议] 补充Wilkinson等(2016)FAIR原则原始文献引用")

# ========== 11. 统计表述规范化（博导3意见） ==========
# Spearman相关系数补充样本量
old_spear = 'Spearman秩相关系数ρ=0.52（p<0.01）'
new_spear = 'Spearman秩相关系数ρ=0.52，n=23，p<0.01（双尾检验）'
if old_spear in text:
    text = text.replace(old_spear, new_spear)
    changes.append("[必须] Spearman统计表述规范化（补充n和检验类型）")

# ========== 12. 方法描述严谨性（博导3意见） ==========
old_fsqca = '将原始数据转化为0-1之间的模糊集隶属度分数'
new_fsqca = '将原始数据校准为模糊集隶属度分数（理论上介于0-1之间）'
if old_fsqca in text:
    text = text.replace(old_fsqca, new_fsqca)
    changes.append("[必须] fsQCA校准描述严谨化")

# ========== 13. 因果关系过度表述（博导3意见） ==========
if '"决定性影响"' in text:
    text = text.replace('"决定性影响"', '"显著影响"')
    changes.append("[必须] DEMATEL因果关系表述修正：'决定性'→'显著'")

# ========== 14. DEMATEL旧结论残留检查 ==========
if '"原因因素"' in text and '"结果因素"' in text:
    changes.append("[警告] 文中仍出现'原因因素/结果因素'分层表述，需核实是否已更新为网络化结构")

# ========== 15. 保存 ==========
with open(md_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"批量修复完成。原始长度: {orig_len} → 新长度: {len(text)}")
print(f"共执行/检测到 {len(changes)} 项修改：")
for c in changes:
    print(f"  - {c}")

# 输出需要人工确认的项目
manual_items = [c for c in changes if c.startswith("[警告]") or c.startswith("[建议]")]
if manual_items:
    print(f"\n[注意] 需要人工确认的项（{len(manual_items)}项）：")
    for m in manual_items:
        print(f"  - {m}")
