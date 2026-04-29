# fsQCA 组态路径分析脚本
# 使用 R 语言进行模糊集定性比较分析

# 安装和加载必要的包
# install.packages("QCA")
library(QCA)

# 1. 读取校准数据
cal_data <- read.csv("fsqca_truth_table.csv", stringsAsFactors = FALSE)
print("=")
print("fsQCA 组态路径分析")
print("=")
print(paste("案例数:", nrow(cal_data)))
print(paste("条件变量:", "政策环境(PL), 开放程度(OG), 平台能力(PC), 数据质量(DQ), 应用效果(AE), 运营保障(OP)"))

# 2. 变量校准（已在CSV中完成直接法校准）
# 校准锚点：完全隶属=0.8, 交叉点=0.5, 完全不隶属=0.2

# 3. 构建真值表
tt <- truthTable(
  cal_data,
  outcome = "校准值_结果",
  conditions = c("PL", "OG", "PC", "DQ", "AE", "OP"),
  incl.cut = 0.80,      # 一致性阈值
  n.cut = 1,            # 案例频数阈值
  pri.cut = 0.70,       # PRI一致性阈值
  sort.by = "incl"
)

print("\n[步骤1] 真值表构建完成")
print(tt)

# 4. 布尔最小化 - 标准分析
# 分析高绩效路径 (结果 = 1)
result_high <- minimize(
  tt,
  details = TRUE,
  show.cases = TRUE,
  dir.exp = c(1,1,1,1,1,1)  # 方向期望：所有条件正向
)

print("\n[步骤2] 高绩效路径分析完成")
print(result_high)

# 5. 分析非高绩效路径 (结果 = 0)
result_low <- minimize(
  tt,
  outcome = "~校准值_结果",  # 非集
  details = TRUE,
  show.cases = TRUE
)

print("\n[步骤3] 非高绩效路径分析完成")
print(result_low)

# 6. 结果汇总
print("\n=")
print("分析结果汇总")
print("=")
cat("\n高绩效路径 (结果 = 1):\n")
print(result_high$solution)
cat("\n解的一致性:", result_high$IC$incl.cov[1,"incl"])
cat("\n解的覆盖度:", result_high$IC$incl.cov[1,"cov"])

cat("\n\n非高绩效路径 (结果 = 0):\n")
print(result_low$solution)

# 保存结果
write.csv(result_high$solution, "fsqca_high_performance_paths.csv", row.names = FALSE)
write.csv(result_low$solution, "fsqca_low_performance_paths.csv", row.names = FALSE)

cat("\n[完成] 结果已保存至 fsqca_high_performance_paths.csv 和 fsqca_low_performance_paths.csv\n")
