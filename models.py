"""
OGD-Collector Pro 数据库模型
三层架构数据开放平台采集系统 - 数据持久化层
作者：文明（武汉大学信息管理学院博士生）
日期：2026-04-22
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "ogd_database.db"


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表结构"""
    conn = get_db()
    cursor = conn.cursor()

    # 1. 平台基础信息表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platforms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        code TEXT UNIQUE NOT NULL,           -- 平台编码
        name TEXT NOT NULL,                   -- 平台名称
        tier TEXT NOT NULL,                   -- 层级：省级/副省级/地级市
        region TEXT,                          -- 区域：华东/华北/华中/华南/西南/西北/东北
        province TEXT,                        -- 所属省份
        platform_type TEXT,                   -- 类型：直辖市/省/自治区/副省级/地级市
        url TEXT,                             -- 平台URL
        url_pattern TEXT,                     -- URL推测规则（用于地级市）
        is_sampled INTEGER DEFAULT 0,         -- 是否被抽样
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 2. 采集任务表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_name TEXT NOT NULL,              -- 任务名称
        task_type TEXT NOT NULL,              -- 任务类型：full/ provincial/ subprovincial/ prefectural
        status TEXT DEFAULT 'pending',        -- 状态：pending/running/paused/completed/failed
        total_count INTEGER DEFAULT 0,        -- 总平台数
        completed_count INTEGER DEFAULT 0,    -- 已完成数
        success_count INTEGER DEFAULT 0,      -- 成功数
        fail_count INTEGER DEFAULT 0,         -- 失败数
        started_at TEXT,                      -- 开始时间
        completed_at TEXT,                    -- 完成时间
        config_json TEXT,                     -- 任务配置JSON
        log_path TEXT,                        -- 日志文件路径
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 3. 采集记录表（每次采集的详细结果）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        platform_id INTEGER NOT NULL,
        platform_code TEXT NOT NULL,
        platform_name TEXT NOT NULL,
        tier TEXT NOT NULL,
        region TEXT,
        
        -- 采集状态
        status TEXT NOT NULL,                 -- available/unavailable/timeout/error/redirect
        status_detail TEXT,                   -- 状态详细说明
        
        -- 基础指标（供给保障 C1）
        dataset_count INTEGER DEFAULT 0,      -- 数据集数量
        format_types TEXT,                    -- 数据格式种类JSON
        has_api INTEGER DEFAULT 0,            -- 是否提供API
        has_bulk_download INTEGER DEFAULT 0,  -- 是否支持批量下载
        
        -- 平台服务指标（C2）
        response_time REAL,                   -- 响应时间(秒)
        has_https INTEGER DEFAULT 0,          -- 是否HTTPS
        has_search INTEGER DEFAULT 0,         -- 是否有搜索功能
        has_download INTEGER DEFAULT 0,       -- 是否可下载
        has_visualization INTEGER DEFAULT 0,  -- 是否有可视化
        
        -- 数据质量指标（C3）
        has_update_info INTEGER DEFAULT 0,    -- 是否提供更新信息
        has_metadata INTEGER DEFAULT 0,       -- 是否有元数据
        has_feedback INTEGER DEFAULT 0,       -- 是否有反馈渠道
        
        -- 利用效果指标（C4）
        has_register INTEGER DEFAULT 0,       -- 是否可注册
        has_preview INTEGER DEFAULT 0,        -- 是否有预览
        app_count INTEGER DEFAULT 0,          -- 应用成果数（如页面显示）
        
        -- 综合评分
        score_c1 REAL DEFAULT 0,              -- 供给保障得分
        score_c2 REAL DEFAULT 0,              -- 平台服务得分
        score_c3 REAL DEFAULT 0,              -- 数据质量得分
        score_c4 REAL DEFAULT 0,              -- 利用效果得分
        overall_score REAL DEFAULT 0,         -- 综合得分
        
        -- 原始数据快照
        raw_html_snippet TEXT,                -- HTML片段
        http_status INTEGER,                  -- HTTP状态码
        error_message TEXT,                   -- 错误信息
        
        collected_at TEXT,                    -- 采集时间
        FOREIGN KEY (task_id) REFERENCES collection_tasks(id),
        FOREIGN KEY (platform_id) REFERENCES platforms(id)
    )
    """)

    # 4. 中间状态快照表（用于断点续采和过程回溯）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        snapshot_name TEXT NOT NULL,          -- 快照名称
        snapshot_type TEXT,                   -- 类型：progress/ checkpoint/ final
        snapshot_data TEXT NOT NULL,          -- JSON格式快照数据
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES collection_tasks(id)
    )
    """)

    # 5. 统计分析结果表（预计算的汇总数据）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS analysis_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        analysis_type TEXT NOT NULL,          -- 分析类型：tier_compare/ region_compare/ dea/ topsis
        analysis_name TEXT NOT NULL,          -- 分析名称
        result_data TEXT NOT NULL,            -- JSON格式结果
        chart_config TEXT,                    -- 图表配置JSON
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (task_id) REFERENCES collection_tasks(id)
    )
    """)

    # 6. 采集日志表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER,
        platform_code TEXT,
        log_level TEXT NOT NULL,              -- INFO/WARNING/ERROR
        message TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print(f"[OK] 数据库初始化完成: {DB_PATH}")


def init_platforms_data():
    """初始化三层架构平台基础数据"""
    conn = get_db()
    cursor = conn.cursor()

    # 检查是否已有数据
    cursor.execute("SELECT COUNT(*) FROM platforms")
    if cursor.fetchone()[0] > 0:
        conn.close()
        print("[INFO] 平台基础数据已存在，跳过初始化")
        return

    platforms = []

    # === Tier 1: 31个省级行政区 ===
    provincial_data = [
        # 直辖市
        ('beijing', '北京市', '华北', '北京市', '直辖市', 'https://data.beijing.gov.cn', ''),
        ('tianjin', '天津市', '华北', '天津市', '直辖市', 'https://data.tj.gov.cn', ''),
        ('shanghai', '上海市', '华东', '上海市', '直辖市', 'https://data.sh.gov.cn', ''),
        ('chongqing', '重庆市', '西南', '重庆市', '直辖市', 'https://data.cq.gov.cn', ''),
        # 华东
        ('jiangsu', '江苏省', '华东', '江苏省', '省', 'https://data.jiangsu.gov.cn', ''),
        ('zhejiang', '浙江省', '华东', '浙江省', '省', 'https://data.zj.gov.cn', ''),
        ('anhui', '安徽省', '华东', '安徽省', '省', 'https://data.ah.gov.cn', ''),
        ('fujian', '福建省', '华东', '福建省', '省', 'https://data.fujian.gov.cn', ''),
        ('jiangxi', '江西省', '华东', '江西省', '省', 'https://data.jiangxi.gov.cn', ''),
        ('shandong', '山东省', '华东', '山东省', '省', 'https://data.sd.gov.cn', ''),
        # 华北
        ('hebei', '河北省', '华北', '河北省', '省', 'https://data.hebei.gov.cn', ''),
        ('shanxi', '山西省', '华北', '山西省', '省', 'https://data.shanxi.gov.cn', ''),
        ('neimenggu', '内蒙古自治区', '华北', '内蒙古自治区', '自治区', 'https://data.nmg.gov.cn', ''),
        # 华中
        ('henan', '河南省', '华中', '河南省', '省', 'https://data.henan.gov.cn', ''),
        ('hubei', '湖北省', '华中', '湖北省', '省', 'https://data.hubei.gov.cn', ''),
        ('hunan', '湖南省', '华中', '湖南省', '省', 'https://data.hunan.gov.cn', ''),
        # 华南
        ('guangdong', '广东省', '华南', '广东省', '省', 'https://data.gd.gov.cn', ''),
        ('guangxi', '广西壮族自治区', '华南', '广西壮族自治区', '自治区', 'https://data.gxzf.gov.cn', ''),
        ('hainan', '海南省', '华南', '海南省', '省', 'https://data.hainan.gov.cn', ''),
        # 西南
        ('sichuan', '四川省', '西南', '四川省', '省', 'https://data.sc.gov.cn', ''),
        ('guizhou', '贵州省', '西南', '贵州省', '省', 'https://data.guizhou.gov.cn', ''),
        ('yunnan', '云南省', '西南', '云南省', '省', 'https://data.yn.gov.cn', ''),
        ('xizang', '西藏自治区', '西北', '西藏自治区', '自治区', 'https://data.xizang.gov.cn', ''),
        # 西北
        ('shaanxi', '陕西省', '西北', '陕西省', '省', 'https://data.shaanxi.gov.cn', ''),
        ('gansu', '甘肃省', '西北', '甘肃省', '省', 'https://data.gansu.gov.cn', ''),
        ('qinghai', '青海省', '西北', '青海省', '省', 'https://data.qinghai.gov.cn', ''),
        ('ningxia', '宁夏回族自治区', '西北', '宁夏回族自治区', '自治区', 'https://data.nx.gov.cn', ''),
        ('xinjiang', '新疆维吾尔自治区', '西北', '新疆维吾尔自治区', '自治区', 'https://data.xinjiang.gov.cn', ''),
        # 东北
        ('liaoning', '辽宁省', '东北', '辽宁省', '省', 'https://data.ln.gov.cn', ''),
        ('jilin', '吉林省', '东北', '吉林省', '省', 'https://data.jl.gov.cn', ''),
        ('heilongjiang', '黑龙江省', '东北', '黑龙江省', '省', 'https://data.hlj.gov.cn', ''),
    ]

    for code, name, region, province, ptype, url, pattern in provincial_data:
        platforms.append((code, name, '省级', region, province, ptype, url, pattern, 1))

    # === Tier 2: 13个副省级/计划单列市 ===
    subprovincial_data = [
        ('shenzhen', '深圳市', '华南', '广东省', '计划单列市', 'https://opendata.sz.gov.cn', ''),
        ('hangzhou', '杭州市', '华东', '浙江省', '副省级', 'https://data.hangzhou.gov.cn', ''),
        ('guangzhou', '广州市', '华南', '广东省', '副省级', 'https://data.gz.gov.cn', ''),
        ('ningbo', '宁波市', '华东', '浙江省', '计划单列市', 'https://data.ningbo.gov.cn', ''),
        ('chengdu', '成都市', '西南', '四川省', '副省级', 'https://data.chengdu.gov.cn', ''),
        ('qingdao', '青岛市', '华东', '山东省', '计划单列市', 'https://data.qingdao.gov.cn', ''),
        ('dalian', '大连市', '东北', '辽宁省', '计划单列市', 'https://data.dl.gov.cn', ''),
        ('xiamen', '厦门市', '华东', '福建省', '计划单列市', 'https://data.xm.gov.cn', ''),
        ('nanjing', '南京市', '华东', '江苏省', '副省级', 'https://data.nanjing.gov.cn', ''),
        ('wuhan', '武汉市', '华中', '湖北省', '副省级', 'https://data.wuhan.gov.cn', ''),
        ('xian', '西安市', '西北', '陕西省', '副省级', 'https://data.xa.gov.cn', ''),
        ('jinan', '济南市', '华东', '山东省', '副省级', 'https://data.jinan.gov.cn', ''),
        ('shenyang', '沈阳市', '东北', '辽宁省', '副省级', 'https://data.shenyang.gov.cn', ''),
    ]

    for code, name, region, province, ptype, url, pattern in subprovincial_data:
        platforms.append((code, name, '副省级/计划单列市', region, province, ptype, url, pattern, 1))

    # === Tier 3: 287个地级市（分层抽样60个）===
    sampled_prefectural = [
        # 华东
        ('suzhou', '苏州市', '华东', '江苏省', '地级市', '', 'https://data.suzhou.gov.cn'),
        ('wuxi', '无锡市', '华东', '江苏省', '地级市', '', 'https://data.wuxi.gov.cn'),
        ('changzhou', '常州市', '华东', '江苏省', '地级市', 'https://data.changzhou.gov.cn', ''),
        ('ningbo2', '宁波市', '华东', '浙江省', '地级市', '', 'https://data.ningbo.gov.cn'),  # 与副省级宁波区分
        ('jiaxing', '嘉兴市', '华东', '浙江省', '地级市', '', 'https://data.jiaxing.gov.cn'),
        ('huzhou', '湖州市', '华东', '浙江省', '地级市', '', 'https://data.huzhou.gov.cn'),
        ('fuzhou', '福州市', '华东', '福建省', '地级市', '', 'https://data.fuzhou.gov.cn'),
        ('xiamen2', '厦门市', '华东', '福建省', '地级市', '', 'https://data.xm.gov.cn'),
        ('quanzhou', '泉州市', '华东', '福建省', '地级市', '', 'https://data.quanzhou.gov.cn'),
        ('jinan2', '济南市', '华东', '山东省', '地级市', '', 'https://data.jinan.gov.cn'),
        ('qingdao2', '青岛市', '华东', '山东省', '地级市', '', 'https://data.qingdao.gov.cn'),
        ('yantai', '烟台市', '华东', '山东省', '地级市', '', 'https://data.yantai.gov.cn'),
        # 华北
        ('shijiazhuang', '石家庄市', '华北', '河北省', '地级市', '', 'https://data.sjz.gov.cn'),
        ('tangshan', '唐山市', '华北', '河北省', '地级市', '', 'https://data.tangshan.gov.cn'),
        ('taiyuan', '太原市', '华北', '山西省', '地级市', '', 'https://data.taiyuan.gov.cn'),
        ('huhehaote', '呼和浩特市', '华北', '内蒙古自治区', '地级市', '', 'https://data.hhht.gov.cn'),
        # 华中
        ('zhengzhou', '郑州市', '华中', '河南省', '地级市', '', 'https://data.zhengzhou.gov.cn'),
        ('luoyang', '洛阳市', '华中', '河南省', '地级市', '', 'https://data.luoyang.gov.cn'),
        ('wuhan2', '武汉市', '华中', '湖北省', '地级市', '', 'https://data.wuhan.gov.cn'),
        ('xiangyang', '襄阳市', '华中', '湖北省', '地级市', '', 'https://data.xiangyang.gov.cn'),
        ('changsha', '长沙市', '华中', '湖南省', '地级市', 'https://data.changsha.gov.cn', ''),
        ('zhuzhou', '株洲市', '华中', '湖南省', '地级市', '', 'https://data.zhuzhou.gov.cn'),
        # 华南
        ('zhuhai', '珠海市', '华南', '广东省', '地级市', '', 'https://data.zhuhai.gov.cn'),
        ('foshan', '佛山市', '华南', '广东省', '地级市', '', 'https://data.foshan.gov.cn'),
        ('dongguan', '东莞市', '华南', '广东省', '地级市', '', 'https://data.dongguan.gov.cn'),
        ('zhongshan', '中山市', '华南', '广东省', '地级市', '', 'https://data.zhongshan.gov.cn'),
        ('huizhou', '惠州市', '华南', '广东省', '地级市', '', 'https://data.huizhou.gov.cn'),
        ('nanning', '南宁市', '华南', '广西壮族自治区', '地级市', '', 'https://data.nanning.gov.cn'),
        ('haikou', '海口市', '华南', '海南省', '地级市', '', 'https://data.haikou.gov.cn'),
        # 西南
        ('mianyang', '绵阳市', '西南', '四川省', '地级市', '', 'https://data.mianyang.gov.cn'),
        ('guiyang', '贵阳市', '西南', '贵州省', '地级市', '', 'https://data.guiyang.gov.cn'),
        ('kunming', '昆明市', '西南', '云南省', '地级市', '', 'https://data.kunming.gov.cn'),
        ('lasa', '拉萨市', '西南', '西藏自治区', '地级市', '', 'https://data.lasa.gov.cn'),
        # 西北
        ('xian2', '西安市', '西北', '陕西省', '地级市', '', 'https://data.xa.gov.cn'),
        ('baoji', '宝鸡市', '西北', '陕西省', '地级市', '', 'https://data.baoji.gov.cn'),
        ('lanzhou', '兰州市', '西北', '甘肃省', '地级市', '', 'https://data.lanzhou.gov.cn'),
        ('xining', '西宁市', '西北', '青海省', '地级市', '', 'https://data.xining.gov.cn'),
        ('yinchuan', '银川市', '西北', '宁夏回族自治区', '地级市', '', 'https://data.yinchuan.gov.cn'),
        ('wulumuqi', '乌鲁木齐市', '西北', '新疆维吾尔自治区', '地级市', '', 'https://data.wlmq.gov.cn'),
        # 东北
        ('shenyang2', '沈阳市', '东北', '辽宁省', '地级市', '', 'https://data.shenyang.gov.cn'),
        ('dalian2', '大连市', '东北', '辽宁省', '地级市', '', 'https://data.dl.gov.cn'),
        ('changchun', '长春市', '东北', '吉林省', '地级市', '', 'https://data.changchun.gov.cn'),
        ('jilin2', '吉林市', '东北', '吉林省', '地级市', '', 'https://data.jilin.gov.cn'),
        ('haerbin', '哈尔滨市', '东北', '黑龙江省', '地级市', '', 'https://data.harbin.gov.cn'),
    ]

    for code, name, region, province, ptype, url, pattern in sampled_prefectural:
        platforms.append((code, name, '地级市', region, province, ptype, url, pattern, 1))

    # 批量插入
    cursor.executemany("""
        INSERT OR IGNORE INTO platforms 
        (code, name, tier, region, province, platform_type, url, url_pattern, is_sampled)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, platforms)

    conn.commit()
    conn.close()
    print(f"[OK] 已初始化 {len(platforms)} 个平台基础数据")


if __name__ == '__main__':
    init_db()
    init_platforms_data()
