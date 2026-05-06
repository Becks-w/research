#!/usr/bin/env python3
"""
build_index.py - Becks 研报库自动索引生成器

用法:
    python build_index.py

工作流程:
    1. 扫描 stocks/ weekly/ daily/ 三个文件夹下所有 HTML 文件
    2. 从每份 HTML 中自动提取：标题、数据日期、摘要
    3. 按时间倒序生成主页 index.html
    4. 主页支持分类筛选和搜索

每次新增报告后，运行此脚本即可更新主页。
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from html import escape

# === 配置项 ===
ROOT_DIR = Path(__file__).parent.parent  # 脚本在 scripts/ 下，根目录是上一级
CATEGORIES = {
    'stocks': {'label': '个股分析', 'icon': '📈', 'color': '#58a6ff'},
    'weekly': {'label': '市场周报', 'icon': '📊', 'color': '#95d048'},
    'daily':  {'label': '每日简报', 'icon': '📰', 'color': '#f5a623'},
    'features': {'label': '专题报道', 'icon': '🔍', 'color': '#d2a8ff'},
}


def extract_metadata(html_path: Path) -> dict:
    """从 HTML 文件中提取元信息（标题、日期、摘要）"""
    try:
        content = html_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        content = html_path.read_text(encoding='gbk', errors='ignore')

    # 1. 提取 <title>
    title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else html_path.stem
    # 清理 title 里的管道分隔符（取第一段）
    title = re.split(r'\s*[|·]\s*', title)[0].strip()

    # 2. 提取数据日期 — 优先找 "数据截止" / "数据日期" / 类似关键词
    date_patterns = [
        r'数据截止[：:]\s*(\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日)',
        r'数据日期[：:]\s*(\d{4}-\d{2}-\d{2})',
        r'(\d{4}-\d{2}-\d{2})',
    ]
    data_date = None
    for pattern in date_patterns:
        m = re.search(pattern, content)
        if m:
            data_date = m.group(1)
            break

    # 3. 摘要 — 取第一个 <p> 标签内容（去除 HTML 标签后截断）
    summary = ''
    p_matches = re.findall(r'<p[^>]*>(.*?)</p>', content, re.IGNORECASE | re.DOTALL)
    for p in p_matches:
        clean = re.sub(r'<[^>]+>', '', p).strip()
        clean = re.sub(r'\s+', ' ', clean)
        if len(clean) > 30:  # 跳过太短的（可能是 footer 或装饰）
            summary = clean[:140] + ('...' if len(clean) > 140 else '')
            break

    # 4. 文件修改时间作为兜底排序键
    mtime = datetime.fromtimestamp(html_path.stat().st_mtime)

    return {
        'title': title,
        'data_date': data_date or mtime.strftime('%Y-%m-%d'),
        'summary': summary or '（无摘要）',
        'mtime': mtime.isoformat(),
        'mtime_display': mtime.strftime('%Y-%m-%d'),
    }


def scan_reports() -> dict:
    """扫描所有分类文件夹，返回结构化的报告列表"""
    all_reports = {cat: [] for cat in CATEGORIES}

    for category in CATEGORIES:
        cat_dir = ROOT_DIR / category
        if not cat_dir.exists():
            continue

        for html_file in cat_dir.glob('*.html'):
            meta = extract_metadata(html_file)
            meta['category'] = category
            meta['filename'] = html_file.name
            meta['relative_path'] = f"{category}/{html_file.name}"
            all_reports[category].append(meta)

    # 每个分类按数据日期倒序排列
    for cat in all_reports:
        all_reports[cat].sort(key=lambda x: x['mtime'], reverse=True)

    return all_reports


def render_card(report: dict) -> str:
    """生成单张报告卡片的 HTML"""
    cat_info = CATEGORIES[report['category']]
    return f"""
    <a href="{escape(report['relative_path'])}" class="report-card" data-category="{report['category']}" data-search="{escape((report['title'] + ' ' + report['summary']).lower())}">
      <div class="card-tag" style="background:{cat_info['color']}20;color:{cat_info['color']};border-color:{cat_info['color']}40;">
        {cat_info['icon']} {cat_info['label']}
      </div>
      <h3>{escape(report['title'])}</h3>
      <p class="summary">{escape(report['summary'])}</p>
      <div class="meta">
        <span class="date">📅 {escape(report['data_date'])}</span>
        <span class="filename">📄 {escape(report['filename'])}</span>
      </div>
    </a>
    """


def build_index_html(reports: dict) -> str:
    """生成主页 index.html"""
    total_count = sum(len(r) for r in reports.values())

    # 把所有报告打平成一个列表，按时间倒序
    all_flat = []
    for cat_reports in reports.values():
        all_flat.extend(cat_reports)
    all_flat.sort(key=lambda x: x['mtime'], reverse=True)

    cards_html = '\n'.join(render_card(r) for r in all_flat)

    # 分类统计
    stats_html = ' · '.join(
        f"<span style='color:{CATEGORIES[cat]['color']}'>{CATEGORIES[cat]['icon']} {CATEGORIES[cat]['label']} {len(reports[cat])}</span>"
        for cat in CATEGORIES
    )

    last_update = datetime.now().strftime('%Y-%m-%d %H:%M')

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Becks Research Archive</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #0d1117; color: #e6edf3; line-height: 1.6;
    min-height: 100vh; padding: 32px 16px;
  }}
  .container {{ max-width: 1100px; margin: 0 auto; }}

  /* Header */
  header {{ text-align: center; margin-bottom: 40px; }}
  h1 {{
    font-size: 36px; font-weight: 700;
    background: linear-gradient(135deg, #58a6ff, #79c0ff 50%, #d2a8ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 8px;
  }}
  .subtitle {{ color: #8b949e; font-size: 14px; margin-bottom: 16px; }}
  .stats {{
    display: inline-block; padding: 8px 20px;
    background: rgba(56, 139, 253, 0.08); border: 1px solid rgba(56, 139, 253, 0.2);
    border-radius: 24px; font-size: 13px; color: #c9d1d9;
  }}

  /* Controls */
  .controls {{
    display: flex; gap: 12px; margin-bottom: 32px; flex-wrap: wrap;
    align-items: center;
  }}
  .search-box {{
    flex: 1; min-width: 240px;
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 10px 14px; color: #e6edf3; font-size: 14px;
    font-family: inherit;
  }}
  .search-box:focus {{ outline: none; border-color: #58a6ff; }}
  .filter-btn {{
    padding: 8px 16px; background: #161b22; border: 1px solid #30363d;
    border-radius: 8px; color: #8b949e; cursor: pointer; font-size: 13px;
    font-family: inherit; transition: all 0.2s;
  }}
  .filter-btn:hover {{ color: #e6edf3; border-color: #58a6ff; }}
  .filter-btn.active {{ background: #58a6ff20; color: #58a6ff; border-color: #58a6ff; }}

  /* Cards */
  .reports-grid {{
    display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 16px;
  }}
  .report-card {{
    background: #161b22; border: 1px solid #30363d; border-radius: 12px;
    padding: 20px; text-decoration: none; color: inherit;
    transition: all 0.2s; display: block;
  }}
  .report-card:hover {{
    transform: translateY(-2px); border-color: #58a6ff;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
  }}
  .card-tag {{
    display: inline-block; padding: 3px 10px; border-radius: 12px;
    font-size: 11px; font-weight: 600; border: 1px solid;
    margin-bottom: 12px;
  }}
  .report-card h3 {{
    font-size: 16px; color: #f0f6fc; margin-bottom: 8px;
    line-height: 1.4;
  }}
  .summary {{
    font-size: 13px; color: #8b949e; margin-bottom: 14px;
    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
    overflow: hidden;
  }}
  .meta {{
    display: flex; justify-content: space-between; gap: 8px;
    font-size: 11px; color: #6e7681;
    border-top: 1px solid #21262d; padding-top: 10px;
    flex-wrap: wrap;
  }}
  .meta .filename {{ font-family: monospace; opacity: 0.7; }}

  /* Empty state */
  .empty {{
    text-align: center; padding: 60px 20px; color: #6e7681;
    grid-column: 1 / -1;
  }}

  /* Footer */
  footer {{
    margin-top: 48px; padding-top: 24px;
    border-top: 1px solid #21262d;
    text-align: center; font-size: 12px; color: #6e7681;
  }}
  footer a {{ color: #58a6ff; text-decoration: none; }}
</style>
</head>
<body>
<div class="container">

<header>
  <h1>Becks Research Archive</h1>
  <div class="subtitle">个人投研档案库 · 共 {total_count} 份报告</div>
  <div class="stats">{stats_html}</div>
</header>

<div class="controls">
  <input type="text" class="search-box" id="searchInput" placeholder="🔍 搜索标题或内容关键词...">
  <button class="filter-btn active" data-filter="all">全部</button>
  <button class="filter-btn" data-filter="stocks">📈 个股</button>
  <button class="filter-btn" data-filter="weekly">📊 周报</button>
  <button class="filter-btn" data-filter="daily">📰 日报</button>
</div>

<div class="reports-grid" id="reportsGrid">
{cards_html if total_count > 0 else '<div class="empty">📭 还没有报告。把 HTML 文件放到 stocks/ weekly/ daily/ 文件夹下，再次运行 build_index.py 即可。</div>'}
</div>

<footer>
  <p>最后更新：{last_update} · 由 build_index.py 自动生成</p>
</footer>

</div>

<script>
const searchInput = document.getElementById('searchInput');
const filterBtns = document.querySelectorAll('.filter-btn');
const cards = document.querySelectorAll('.report-card');
let currentFilter = 'all';

function applyFilters() {{
  const query = searchInput.value.toLowerCase().trim();
  let visibleCount = 0;
  cards.forEach(card => {{
    const matchCategory = currentFilter === 'all' || card.dataset.category === currentFilter;
    const matchSearch = !query || card.dataset.search.includes(query);
    const visible = matchCategory && matchSearch;
    card.style.display = visible ? 'block' : 'none';
    if (visible) visibleCount++;
  }});
}}

searchInput.addEventListener('input', applyFilters);
filterBtns.forEach(btn => {{
  btn.addEventListener('click', () => {{
    filterBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter = btn.dataset.filter;
    applyFilters();
  }});
}});
</script>
</body>
</html>
"""


def main():
    print("🔍 扫描研报文件夹...")
    reports = scan_reports()

    total = sum(len(r) for r in reports.values())
    print(f"✓ 发现 {total} 份报告：")
    for cat, items in reports.items():
        print(f"  - {CATEGORIES[cat]['label']}: {len(items)} 份")

    print("\n📝 生成主页 index.html...")
    html = build_index_html(reports)
    output_path = ROOT_DIR / 'index.html'
    output_path.write_text(html, encoding='utf-8')
    print(f"✓ 已写入 {output_path}")

    print("\n🚀 完成！下一步：")
    print("   git add .")
    print('   git commit -m "Update reports"')
    print("   git push")


if __name__ == '__main__':
    main()
