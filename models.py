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

    # 7. 访问日志表（隐私保护 + 使用分析）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS access_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ip TEXT,
        path TEXT,
        method TEXT,
        user_agent TEXT,
        accessed_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 8. 采集统计表（按日/按任务汇总，用于趋势分析）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stat_date TEXT NOT NULL,              -- 统计日期 YYYY-MM-DD
        task_id INTEGER,
        tier TEXT,                            -- 层级
        total_platforms INTEGER DEFAULT 0,    -- 平台总数
        available_count INTEGER DEFAULT 0,    -- 可用数
        unavailable_count INTEGER DEFAULT 0,  -- 不可用数
        avg_score REAL DEFAULT 0,             -- 平均得分
        avg_c1 REAL DEFAULT 0,                -- 供给保障平均分
        avg_c2 REAL DEFAULT 0,                -- 平台服务平均分
        avg_c3 REAL DEFAULT 0,                -- 数据质量平均分
        avg_c4 REAL DEFAULT 0,                -- 利用效果平均分
        new_datasets INTEGER DEFAULT 0,       -- 新增数据集数
        total_api_calls INTEGER DEFAULT 0,    -- API调用次数统计
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 9. 平台架构与特征表（丰富数据维度）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platform_features (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform_id INTEGER NOT NULL,
        platform_code TEXT NOT NULL,
        -- 技术架构
        cms_type TEXT,                        -- CMS类型：自建/省级统建/第三方
        framework TEXT,                       -- 技术框架
        has_mobile_version INTEGER DEFAULT 0, -- 是否有移动端
        -- 数据维度
        data_categories TEXT,                 -- 数据分类JSON
        update_frequency TEXT,                -- 更新频率
        earliest_data_date TEXT,              -- 最早数据日期
        -- 互动功能
        has_feedback INTEGER DEFAULT 0,       -- 是否有反馈
        has_data_request INTEGER DEFAULT 0,   -- 是否可申请数据
        has_app_showcase INTEGER DEFAULT 0,   -- 是否有应用展示
        -- 外部引用
        cited_by_count INTEGER DEFAULT 0,     -- 被引用次数（如学术论文）
        third_party_apps INTEGER DEFAULT 0,   -- 第三方应用数
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (platform_id) REFERENCES platforms(id)
    )
    """)

    # 10. 每日自动采集任务配置表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auto_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        schedule_name TEXT NOT NULL,
        cron_expression TEXT NOT NULL,        -- cron表达式
        task_type TEXT NOT NULL,              -- full/provincial/subprovincial/prefectural
        is_active INTEGER DEFAULT 1,          -- 是否启用
        last_run_at TEXT,
        next_run_at TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 11. 平台健康检查详细记录表（每次探测的完整指标）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS platform_health_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform_id INTEGER NOT NULL,
        platform_code TEXT NOT NULL,
        platform_name TEXT,
        check_time TEXT DEFAULT CURRENT_TIMESTAMP,  -- 检查时间戳
        -- 可达性指标
        is_reachable INTEGER DEFAULT 0,       -- 是否可达
        http_status INTEGER,                  -- HTTP状态码
        response_time_ms INTEGER,             -- 响应时间(毫秒)
        dns_resolve_time_ms INTEGER,          -- DNS解析时间
        ssl_valid INTEGER DEFAULT 0,          -- SSL证书是否有效
        ssl_expire_days INTEGER,              -- SSL证书剩余天数
        -- 内容指标
        page_size_kb REAL,                    -- 页面大小(KB)
        charset TEXT,                         -- 字符编码
        server_header TEXT,                   -- Server响应头
        -- 异常记录
        error_type TEXT,                      -- 错误类型：timeout/dns_error/ssl_error/http_error
        error_detail TEXT,                    -- 错误详情
        -- 原始响应摘要
        response_snippet TEXT,                -- 响应内容前500字符
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 12. API端点监测表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_endpoint_checks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        platform_id INTEGER NOT NULL,
        platform_code TEXT NOT NULL,
        endpoint_url TEXT NOT NULL,           -- API端点URL
        endpoint_type TEXT,                   -- 类型：dataset_list/search/download/api_doc
        check_time TEXT DEFAULT CURRENT_TIMESTAMP,
        is_available INTEGER DEFAULT 0,       -- 是否可用
        http_status INTEGER,                  -- HTTP状态码
        response_time_ms INTEGER,             -- 响应时间(毫秒)
        response_format TEXT,                 -- 返回格式：JSON/XML/HTML/其他
        response_size_bytes INTEGER,          -- 响应体大小
        rate_limit_headers TEXT,              -- 限速头信息
        error_message TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 13. 数据来源记录表（外部数据源，用于论文数据溯源）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS data_provenance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_name TEXT NOT NULL,            -- 来源名称
        source_name_en TEXT,                  -- 英文名称
        source_type TEXT NOT NULL,            -- 类型：政府平台/学术数据库/国际组织/新闻媒体/企业数据/实地调研
        source_category TEXT,                 -- 类别：政策法规/平台数据/统计数据/案例数据/文献数据
        -- 访问信息
        url TEXT,                             -- 来源URL
        access_method TEXT,                   -- 获取方式：API/爬虫/手工采集/公开下载/问卷/访谈
        -- 时间范围
        data_start_date TEXT,                 -- 数据起始日期
        data_end_date TEXT,                  -- 数据结束日期
        -- 数据描述
        data_description TEXT,                -- 数据内容描述
        data_format TEXT,                     -- 数据格式：JSON/XML/CSV/Excel/PDF/数据库
        record_count INTEGER,                 -- 记录数量
        -- 质量信息
        update_frequency TEXT,                -- 更新频率
        last_access_time TEXT,                -- 最后访问时间
        reliability_score INTEGER,            -- 可靠性评分 1-5
        -- 论文引用
        cited_in_chapter TEXT,                -- 引用于第几章
        citation_note TEXT,                   -- 引用说明
        -- 元数据
        license_type TEXT,                    -- 许可证类型
        contact_info TEXT,                    -- 联系方式
        notes TEXT,                           -- 备注
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 14. 采集数据归集快照表（每日完整数据归集，可复查可导出）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_date TEXT NOT NULL,          -- 快照日期 YYYY-MM-DD
        snapshot_time TEXT NOT NULL,          -- 快照时间 HH:MM:SS
        snapshot_type TEXT NOT NULL,          -- 类型：daily/midday/evening/weekly
        task_id INTEGER,
        -- 汇总统计
        total_platforms INTEGER DEFAULT 0,
        reachable_count INTEGER DEFAULT 0,
        unreachable_count INTEGER DEFAULT 0,
        avg_response_time_ms INTEGER DEFAULT 0,
        -- 4E维度汇总
        avg_score_c1 REAL DEFAULT 0,
        avg_score_c2 REAL DEFAULT 0,
        avg_score_c3 REAL DEFAULT 0,
        avg_score_c4 REAL DEFAULT 0,
        avg_overall_score REAL DEFAULT 0,
        -- 数据集汇总
        total_datasets INTEGER DEFAULT 0,
        total_api_endpoints INTEGER DEFAULT 0,
        -- 快照数据（JSON格式，包含当日所有平台详细数据）
        snapshot_data_json TEXT,
        -- 校验信息
        checksum TEXT,                        -- 数据校验和
        file_size_kb INTEGER,                 -- 快照大小KB
        -- 元数据
        collector_version TEXT,               -- 采集器版本
        export_path TEXT,                     -- 导出文件路径
        is_verified INTEGER DEFAULT 0,        -- 是否已核验
        verified_by TEXT,                     -- 核验人
        verified_at TEXT,                     -- 核验时间
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # 15. 采集指标实时记录表（每次单个平台采集的详细指标）
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS collection_metrics_detail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER NOT NULL,
        platform_id INTEGER NOT NULL,
        platform_code TEXT NOT NULL,
        platform_name TEXT,
        tier TEXT,
        region TEXT,
        -- 时间戳（精确到秒）
        collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
        -- 可达性
        is_reachable INTEGER DEFAULT 0,
        http_status INTEGER,
        response_time_ms INTEGER,
        -- 供给保障 C1
        dataset_count INTEGER DEFAULT 0,
        dataset_categories INTEGER DEFAULT 0,
        format_types TEXT,
        has_api INTEGER DEFAULT 0,
        has_bulk_download INTEGER DEFAULT 0,
        open_license_count INTEGER DEFAULT 0,
        -- 平台服务 C2
        has_https INTEGER DEFAULT 0,
        has_search INTEGER DEFAULT 0,
        has_filter INTEGER DEFAULT 0,
        has_preview INTEGER DEFAULT 0,
        has_visualization INTEGER DEFAULT 0,
        has_sdk INTEGER DEFAULT 0,
        -- 数据质量 C3
        has_metadata INTEGER DEFAULT 0,
        has_update_info INTEGER DEFAULT 0,
        has_quality_report INTEGER DEFAULT 0,
        machine_readable_rate REAL DEFAULT 0,
        update_frequency_score REAL DEFAULT 0,
        -- 利用效果 C4
        has_register INTEGER DEFAULT 0,
        has_feedback INTEGER DEFAULT 0,
        has_data_request INTEGER DEFAULT 0,
        app_showcase_count INTEGER DEFAULT 0,
        download_count INTEGER DEFAULT 0,
        -- 综合评分
        score_c1 REAL DEFAULT 0,
        score_c2 REAL DEFAULT 0,
        score_c3 REAL DEFAULT 0,
        score_c4 REAL DEFAULT 0,
        overall_score REAL DEFAULT 0,
        -- 原始数据
        raw_metadata TEXT,
        error_message TEXT,
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


def init_provenance_data():
    """初始化论文外部数据来源记录"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM data_provenance")
    if cursor.fetchone()[0] > 0:
        conn.close()
        print("[INFO] 数据来源数据已存在，跳过初始化")
        return

    sources = [
        # 政府平台数据
        ("国家数据局", "National Data Bureau", "政府平台", "政策法规",
         "https://www.nda.gov.cn", "公开下载", "2020-01", "2025-12",
         "国家数据局发布的公共数据资源开发利用相关政策文件、指导意见",
         "PDF/HTML", 45, "不定期", "2025-03", 5,
         "第一章、第六章", "政策演进分析的核心依据", "政府公开", "", ""),
        ("复旦大学数字与移动治理实验室", "Fudan DMG Lab", "政府平台", "统计数据",
         "https://opendata.fudan.edu.cn", "公开下载", "2017-01", "2025-09",
         "《中国地方政府数据开放报告》《中国开放数林指数》年度报告",
         "PDF/Excel", 8, "年度", "2025-03", 5,
         "第一章、第五章", "平台数量与数据集统计的权威来源", "CC BY", "", ""),
        ("中国政府网", "Gov.cn", "政府平台", "政策法规",
         "https://www.gov.cn", "公开下载", "2015-01", "2025-12",
         "国务院及各部委发布的数字政府、数据开放相关政策文件",
         "PDF/HTML", 120, "实时", "2025-03", 5,
         "第一章、第六章", "政策文本分析的主要来源", "政府公开", "", ""),
        ("各省级政府数据开放平台", "Provincial OGD Platforms", "政府平台", "平台数据",
         "", "API/爬虫", "2015-01", "2025-03",
         "31个省级政府数据开放平台的网站数据，包括数据集数量、格式、API等",
         "HTML/JSON", 331, "实时", "2025-03", 5,
         "第三至六章", "4E评估框架实证分析的核心数据", "开放许可", "", ""),

        # 学术数据库
        ("中国知网(CNKI)", "CNKI", "学术数据库", "文献数据",
         "https://www.cnki.net", "数据库检索", "2009-01", "2025-03",
         "政府数据开放、数字政府、公共数据相关中文学术论文",
         "数据库", 504, "实时", "2025-03", 5,
         "第一章、第二章", "文献综述与理论基础的主要来源", "订阅", "", ""),
        ("Web of Science", "Web of Science", "学术数据库", "文献数据",
         "https://www.webofscience.com", "数据库检索", "2009-01", "2025-03",
         "Open Government Data、Open Data、Digital Government相关英文文献",
         "数据库", 200, "实时", "2025-03", 5,
         "第一章、第二章", "国际文献综述与理论框架构建", "订阅", "", ""),
        ("Scopus", "Scopus", "学术数据库", "文献数据",
         "https://www.scopus.com", "数据库检索", "2009-01", "2025-03",
         "政府数据开放领域国际学术论文",
         "数据库", 180, "实时", "2025-03", 5,
         "第一章、第二章", "国际文献补充检索", "订阅", "", ""),

        # 国际组织
        ("OECD开放政府数据", "OECD OGD", "国际组织", "统计数据",
         "https://www.oecd.org/gov/digital-government/open-government-data.htm", "公开下载", "2014-01", "2024-12",
         "OECD发布的开放政府数据报告、比较研究与国际排名",
         "PDF/Excel", 15, "年度", "2025-03", 5,
         "第一章、第五章", "国际比较与评估标准参考", "开放许可", "", ""),
        ("世界银行开放数据", "World Bank Open Data", "国际组织", "统计数据",
         "https://data.worldbank.org", "API下载", "2010-01", "2025-03",
         "全球开放数据指数、各国数字政府发展水平指标",
         "API/CSV", 50, "年度", "2025-03", 5,
         "第一章、第五章", "国际发展水平比较", "CC BY", "", ""),
        ("Open Data Barometer", "Open Data Barometer", "国际组织", "统计数据",
         "https://opendatabarometer.org", "公开下载", "2013-01", "2021-12",
         "全球开放数据评估指数，覆盖115个国家的开放数据成熟度评估",
         "PDF/Excel", 4, "年度(已停更)", "2025-03", 4,
         "第一章", "国际评估体系比较", "CC BY", "", ""),
        ("Global Open Data Index", "Global Open Data Index", "国际组织", "统计数据",
         "https://index.okfn.org", "公开下载", "2013-01", "2016-12",
         "OKF发布的全球开放数据指数，评估各国关键数据集开放程度",
         "Web", 4, "年度(已停更)", "2025-03", 4,
         "第一章", "早期国际评估参考", "开放许可", "", ""),

        # 实地调研
        ("平台实地访问与观察", "Platform Field Observation", "实地调研", "案例数据",
         "", "手工采集", "2024-06", "2024-09",
         "对30个省级平台进行实地访问，记录平台功能、数据质量、用户体验",
         "笔记/截图", 30, "一次性", "2024-09", 5,
         "第三至五章", "4E评估框架指标验证的一手数据", "原创", "", ""),
        ("专家问卷调查", "Expert Survey", "实地调研", "统计数据",
         "", "问卷星", "2024-07", "2024-08",
         "面向30位政府数据开放领域专家的问卷，收集指标权重与评估标准意见",
         "Excel", 30, "一次性", "2024-08", 4,
         "第三章", "指标体系权重确定的数据基础", "原创", "", ""),
        ("平台用户访谈", "User Interview", "实地调研", "案例数据",
         "", "访谈录音", "2024-08", "2024-09",
         "对15位平台深度用户（开发者、研究者、企业人员）的半结构化访谈",
         "录音/笔记", 15, "一次性", "2024-09", 4,
         "第五章", "利用效果评估的定性数据", "原创", "", ""),

        # 新闻媒体
        ("新华社", "Xinhua News", "新闻媒体", "案例数据",
         "https://www.xinhuanet.com", "公开下载", "2015-01", "2025-03",
         "数字政府建设、数据开放相关新闻报道与政策解读",
         "HTML", 80, "实时", "2025-03", 4,
         "第一章", "政策背景与社会语境分析", "公开", "", ""),
        ("人民日报", "People's Daily", "新闻媒体", "案例数据",
         "https://www.people.com.cn", "公开下载", "2015-01", "2025-03",
         "数据要素、数字中国建设相关报道",
         "HTML", 60, "实时", "2025-03", 4,
         "第一章、第六章", "政策演进与社会关注分析", "公开", "", ""),

        # 企业/第三方数据
        ("天眼查", "Tianyancha", "企业数据", "统计数据",
         "https://www.tianyancha.com", "API查询", "2024-01", "2025-03",
         "数据开放相关企业注册信息、知识产权、司法风险等",
         "API/Excel", 500, "实时", "2025-03", 3,
         "第五章", "平台生态与企业参与分析", "商业", "", ""),
        ("百度指数", "Baidu Index", "企业数据", "统计数据",
         "https://index.baidu.com", "公开查询", "2015-01", "2025-03",
         '"政府数据开放""数据要素"等关键词的搜索热度趋势',
         "Web", 120, "实时", "2025-03", 3,
         "第一章", "社会关注度与公众认知分析", "商业", "", ""),
    ]

    cursor.executemany("""
        INSERT INTO data_provenance
        (source_name, source_name_en, source_type, source_category, url, access_method,
         data_start_date, data_end_date, data_description, data_format, record_count,
         update_frequency, last_access_time, reliability_score, cited_in_chapter,
         citation_note, license_type, contact_info, notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, sources)
    conn.commit()
    conn.close()
    print(f"[OK] 已初始化 {len(sources)} 条数据来源记录")





if __name__ == '__main__':
    init_db()
    init_platforms_data()
