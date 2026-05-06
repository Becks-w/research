---
name: bubble-alert
description: 生成市场泡沫预警报告，覆盖六大类指标：A.泡沫阶段判断（高盛投机指标、高低Beta相对表现、AI标签溢价指数、垃圾股指数）；B.财报反应离散度（板块内财报反应分化）；C.流动性与情绪极端（Put/Call、0DTE、VIX/HV差、Margin Debt）；D.关键人物与资金流（科技高管13F净卖出、聪明钱持仓变化）；E.宏观共振（贵金属-科技股相关性、DXY、美债收益率与盈利收益率差）；F.亚洲杠杆需求（韩国证存局美股单股杠杆ETF净流入、韩国信用交易余额、香港杠杆ETF成交、加密所美股永续持仓）。当用户提到"泡沫预警"、"市场情绪"、"投机情绪"、"bubble watch"、"泡沫指标"、"风险预算"、"是不是顶部"、"市场过热"时，必须使用此技能，联网搜索获取实时数据后生成报告。Topics可在SKILL.md中动态调整。
---

# 市场泡沫预警生成技能

## 目标

基于一组六类指标的综合读数，输出**当前市场所处的"投机阶段"判断**，区分以下三种状态：

- **健康牛市（中期）**：基本面与价格共舞，板块轮换有序
- **牛市中后期 + 局部投机泡沫**：龙头让位、二线接力、垃圾股/AI转型故事局部泡沫化
- **泡沫晚期**：基本面不再定义价格、所有标的同步暴涨、对正面消息反应衰减、对负面反应放大

报告必须给出**具体阶段判断 + 对应仓位调整建议**，不输出模糊措辞。

---

## ⚙️ 可动态配置的 Topics

以下为当前激活的六类指标。未来可在此处增减模块，无需修改执行逻辑。

```yaml
active_topics:
  - bubble_stage          # A 类：泡沫阶段判断指标
  - earnings_dispersion   # B 类：财报反应离散度
  - liquidity_sentiment   # C 类：流动性 / 情绪极端
  - smart_money_flow      # D 类：关键人物与资金流
  - macro_resonance       # E 类：宏观共振
  - asia_leverage         # F 类：亚洲杠杆需求
```

---

## 第一步：确定报告日期、时区与基准

- 默认报告日期为**前一个交易日收盘后**（跳过周末和美国市场假期）
- 报告标题必须包含**完整年份**（例：2026年5月6日泡沫预警）

### ⚠️ 年份锁定规则
所有 web_search 必须带完整日期含年份。
- ✅ `Goldman Sachs Speculative Trading Indicator May 2026`
- ❌ `Goldman Sachs Speculative Trading Indicator`（可能返回历史峰值）
- ❌ `meme stock April`（无年份，可能命中 2021 年文章）

### 🕐 时区规则
- 报告内所有时间一律使用 **新加坡时间（SGT，UTC+8）**
- 美股收盘 16:00 ET = SGT 04:00（次日，夏令时 / SGT 05:00 冬令时）
- Robinhood、Schwab 财报披露通常美东 06:00 = SGT 18:00

### 🎯 报告频率建议
- **每周一**：完整 6 大类指标全量更新
- **每个交易日**：关键预警触发时输出"专题简报"（仅触发的指标 + 阶段判断变化）
- **NVDA / AMD / AVGO / MU 财报次日**：必须更新 B 类（财报反应离散度）

---

## 第二步：数据采集（按激活的 topics 搜索）

### 📌 模块 A：泡沫阶段判断指标 (`bubble_stage`)

#### A1. 高盛投机交易指标（Goldman Sachs Speculative Trading Indicator, GS STI）

搜索关键词：
```
Goldman Sachs Speculative Trading Indicator [Month YYYY] level
GS STI current reading [Month YYYY] history percentile
"Speculative Trading Indicator" [YYYY]
```

目标数据：
- 当前 STI 读数 + 历史百分位
- 与 1998–2001 互联网泡沫峰值对比
- 与 2020–2021 meme stock 峰值对比
- 与 2025–2026 历史最高值对比

**预警阈值**：
- 🟢 绿色（< 历史中位数）：风险偏好正常
- 🟡 黄色（中位数到 70 百分位）：温和升高
- 🟠 橙色（70 到 90 百分位）：明显过热
- 🔴 红色（> 90 百分位）：进入历史前 10% 的极端区间，3-9 个月内大概率回调

#### A2. 高 Beta vs 低波动相对表现（SPHB / SPLV 比值）

搜索关键词：
```
SPHB SPLV ratio [Month DD YYYY]
high beta low volatility ETF performance [Month YYYY]
SPHB price [Month DD YYYY] close
SPLV price [Month DD YYYY] close
```

目标数据：
- 当日 SPHB / SPLV 比值
- 60 日均值
- 60 日变化率

**预警阈值**：
- 🟢 比值稳定或下降：风险偏好正常
- 🟠 60 日上升 > 15%：风险偏好快速极端化
- 🔴 60 日上升 > 25%：典型泡沫晚期信号

#### A3. AI 标签溢价指数（自建）

搜索关键词：
```
company rebrand "AI" name change [Month YYYY]
"NewBird AI" type rebrand stocks [YYYY]
small cap stock AI pivot announcement [Month YYYY]
penny stock AI transformation [Month YYYY]
```

目标数据：
- 过去 30 天宣布"AI 转型"或公司名添加 AI 后缀的小盘股数量
- 这些公司宣布后 5 日股价中位数涨幅
- 典型案例（如 Allbirds → NewBird AI 模式）

**预警阈值**：
- 🟢 < 5 家/月：正常
- 🟠 5–10 家/月：局部投机
- 🔴 > 10 家/月：明确泡沫晚期信号

#### A4. 垃圾股指数（自建）

搜索关键词：
```
Russell 2000 unprofitable companies performance [Month YYYY]
penny stocks performance [Month YYYY]
loss-making small cap rally [Month YYYY]
```

目标数据：
- 罗素 2000 中亏损公司占比
- 这些公司过去 30 日中位数涨幅
- 复合指标 = 占比 × 中位数涨幅

**预警阈值**：
- 🟢 复合值 < 10：正常
- 🟠 10–25：警戒
- 🔴 > 25：典型泡沫晚期

---

### 📌 模块 B：财报反应离散度 (`earnings_dispersion`)

仅在**半导体板块财报季**（5月、8月、11月、2月）激活。

搜索关键词（**必须包含完整日期年份**）：
```
NVDA earnings reaction [date] after hours
AMD earnings stock reaction [date]
AVGO MU QCOM ARM earnings [Month YYYY]
semiconductor earnings stock movement [Month YYYY]
```

目标数据（每只标的报告窗口期 ±2 日股价反应）：

| 标的 | 财报日 | 营收 beat % | EPS beat % | 指引 beat % | ±2 日股价反应 |
|---|---|---|---|---|---|
| NVDA | | | | | |
| AMD | | | | | |
| AVGO | | | | | |
| MU | | | | | |
| QCOM | | | | | |
| ARM | | | | | |

计算：
- **反应中位数** = 6 只股票 ±2 日反应的中位数
- **反应极差** = 最高反应 − 最低反应
- **轮换方向** = 龙头（NVDA、AVGO）反应是否系统性弱于二线（AMD、MU）

**阶段判断映射**：
- 极差 < 10%（同涨同跌）= **板块同步行情**，可能是阶段顶或底
- 极差 10–25%（温和分化）= **健康轮换**，对应牛市中期
- 极差 > 25%（极端分化）= **激烈轮换**，对应牛市中后期
- 极差 > 25% **且** 资金从二线流向三线（如 SOUN、PLTR 类）= **泡沫晚期**

#### B 附：单股反转检测（财报后 36 小时反转）
对 NVDA、AMD 等龙头：
- 财报盘后涨幅 > 5% 但次日盘中翻绿，且 36 小时累计跌幅 > 3% = **红色预警**
- 历史参照：NVDA Q3 FY26（2025/11/19）盘后 +6% 但 36 小时蒸发 $900B 市值

---

### 📌 模块 C：流动性 / 情绪极端 (`liquidity_sentiment`)

#### C1. CBOE Equity Put/Call Ratio（5 日均值）

搜索关键词：
```
CBOE equity put call ratio [Month DD YYYY]
"put/call ratio" 5 day moving average [Month YYYY]
```

**预警阈值**：
- < 0.55：极度乐观，红色预警
- 0.55–0.70：正常偏乐观
- > 0.85：恐慌，可能是反向买入信号

#### C2. 0DTE 期权占比

搜索关键词：
```
0DTE options share total volume [Month YYYY]
zero day expiration options percentage SPX [Month YYYY]
```

**预警阈值**：
- > 50%：极度投机，红色预警
- 40–50%：高位
- < 40%：正常

#### C3. VIX vs 标普 500 历史波动率差

搜索关键词：
```
VIX SPX historical volatility difference [Month YYYY]
VIX 30-day realized volatility spread [Month DD YYYY]
```

**预警阈值**：
- VIX − 30D HV < 0 持续 5+ 个交易日：市场对未来过度乐观，红色预警

#### C4. 散户经纪商日均开户数

搜索关键词：
```
Robinhood daily new accounts [Month YYYY] earnings
Charles Schwab new account openings [Month YYYY]
retail brokerage account growth [Month YYYY]
```

**预警阈值**：
- 单月环比 > 20%：散户狂热进场，红色预警
- > 10%：警戒

#### C5. FINRA Margin Debt（每月发布）

搜索关键词：
```
FINRA margin debt [Month YYYY] release
NYSE margin debt latest [Month YYYY]
margin debt to market cap ratio [YYYY]
```

**预警阈值**：
- Margin Debt / 市值比例突破历史 95 分位：红色预警
- 月度环比增长 > 5%：警戒

---

### 📌 模块 D：关键人物与资金流 (`smart_money_flow`)

仅在每个季度 13F 披露窗口激活（季度结束后 45 天内：2 月中、5 月中、8 月中、11 月中）。

#### D1. 科技公司高管 13F 净卖出比例

搜索关键词：
```
tech executive insider selling [Quarter YYYY] 13F
NVDA AMD insider transactions [Month YYYY]
semiconductor CEO sell shares [Month YYYY]
```

**预警阈值**：
- 净卖出公司数量占比连续两季度上升：警戒
- 龙头股（NVDA、AMD、AVGO）出现高管集中减持：红色预警

#### D2. 宏观聪明钱持仓变化

搜索关键词：
```
Peter Thiel 13F filing [Month YYYY]
David Tepper Appaloosa 13F [Quarter YYYY]
Stan Druckenmiller Duquesne 13F [Quarter YYYY]
Michael Burry Scion Asset 13F [Quarter YYYY]
hedge fund tech exposure reduce [Quarter YYYY]
```

目标数据：
- Thiel Macro、Appaloosa、Duquesne、Scion、Pershing Square 等"宏观聪明钱"对科技板块的持仓变化
- 是否出现完整退出（如 2025 Q3 Thiel 清仓 NVDA 案例）

**预警阈值**：
- 任何一家完整退出 NVDA / AMD / MSFT / META / GOOG 任一只：黄色预警
- 两家以上同时完整退出：红色预警

#### D3. Goldman Sachs Prime Brokerage 周报（如可获取）

搜索关键词：
```
Goldman Prime Brokerage weekly tech sector flow [Month YYYY]
hedge fund tech sector net exposure [Week YYYY]
```

---

### 📌 模块 E：宏观共振 (`macro_resonance`)

#### E1. 贵金属与科技股相关性

搜索关键词：
```
gold silver tech stocks correlation [Month YYYY]
SPY GLD SLV correlation [Month YYYY]
NVDA gold price correlation [Month YYYY]
```

目标数据：
- 黄金 / 白银 / 比特币 与 SPY / QQQ 的 30 日滚动相关性
- 历史均值参照：通常负相关（-0.2 到 -0.4）

**预警阈值**：
- 30 日相关性变正且 > 0.3：流动性驱动而非基本面驱动，泡沫晚期信号
- 30 日相关性变正且 > 0.5：极端流动性泡沫，红色预警

**注意**：白银 1 月突破 $100，4 月已回落到 $73—74（约 -22%）。**贵金属和科技股已不再同步上涨，这条件目前不满足泡沫晚期定义**。需持续追踪是否重新出现共振。

#### E2. 美元指数 (DXY)

搜索关键词：
```
DXY US Dollar Index [Month DD YYYY] close
US dollar index level [Month YYYY]
```

**预警阈值**：
- DXY < 100 + 科技股大涨：流动性放水信号过度
- DXY < 95 + 黄金、科技、垃圾债同涨：红色预警

#### E3. 10 年期美债收益率与盈利收益率差

搜索关键词：
```
S&P 500 earnings yield 10 year treasury [Month YYYY]
equity risk premium [Month YYYY] level
ERP S&P 500 [Quarter YYYY]
```

计算：
- 盈利收益率 = 1 / forward PE
- ERP = 盈利收益率 − 10 年美债收益率
- 长期均值约 3.0–3.5%

**预警阈值**：
- ERP 0–1%：风险溢价被压缩，警戒
- ERP < 0%：股票收益率低于无风险收益率，红色预警（极端泡沫）

---

### 📌 模块 F：亚洲杠杆需求 (`asia_leverage`)

这是这个 skill 区别于美国本土泡沫指标的**特色模块**。亚洲杠杆资金往往是全球风险偏好的边际驱动力。

#### F1. 韩国证券存管局：美股单股 2x 杠杆 ETF 净流入

搜索关键词：
```
Korea Securities Depository US single stock leveraged ETF flow [Month YYYY]
한국예탁결제원 미국 레버리지 ETF [Month YYYY]
KSD weekly net buy single stock 2x leveraged [Month YYYY]
Korean retail US leveraged ETF holdings [Month YYYY]
```

目标产品（关注名单）：
- Direxion Daily Tesla Bull 2X (TSLL)
- Defiance Daily Target 2X Long AMD (AMDL)
- Defiance Daily Target 2X Long NVDA (NVDX)
- T-rex 2X Long BMNR
- Defiance Daily Target 2X Short IONQ

**预警阈值**：
- 单周净买入 > $5 亿：警戒
- 单周净买入 > $10 亿：红色预警（参照 2025/10/3-9 数据）
- 韩国投资者持有的"Tesla Daily 2x"持仓总额突破 $20 亿：红色

#### F2. 韩国信用交易融资余额

搜索关键词：
```
Korea margin debt 신용거래융자 [Month YYYY]
Korea Financial Investment Association credit balance [Month YYYY]
한국 신용거래융자 잔고 [Month YYYY]
```

历史参照：
- 2021 年历史高点：25.65 万亿韩元
- 2025/10/15 水平：23.83 万亿韩元（接近历史高点）

**预警阈值**：
- > 24 万亿韩元：警戒
- > 25.65 万亿韩元（突破历史高点）：红色预警

#### F3. 香港杠杆 ETF 成交（半导体方向）

搜索关键词：
```
CSOP SK Hynix 2x leveraged ETF turnover [Month YYYY]
Hong Kong semiconductor leveraged ETF volume [Month DD YYYY]
南方东英 海力士 杠杆 ETF [Month YYYY]
```

历史参照：
- CSOP SK Hynix 2x 单日成交峰值：2026/2/27 单日 24 亿港元（约 $3.07 亿）

**预警阈值**：
- 单日成交 > 20 亿港元：警戒
- 单日成交 > 30 亿港元：红色预警

#### F4. 加密交易所代币化美股永续合约持仓量

搜索关键词：
```
Bybit US stock perpetual futures open interest [Month YYYY]
Binance tokenized stocks Ondo Finance OI [Month YYYY]
crypto exchange US equity perp OI [Month YYYY]
```

目标数据（如可获取）：
- Bybit 美股永续合约总持仓量（自 2026/4/27 上线）
- Binance EWY、其他美股永续 OI
- 月度环比增长率

**预警阈值**：
- 月度 OI 增长 > 50%：警戒
- 月度 OI 增长 > 100%：红色预警

#### F5. 韩国 ETF 杠杆教育人数（监管前置指标）

搜索关键词：
```
Korea leveraged ETF education registrations [Month YYYY]
Korea Financial Investment Education Institute [Month YYYY]
한국 레버리지 ETF 교육 [Month YYYY]
```

历史参照：
- 2025/1：8,600 人
- 2026/1：167,000 人（19 倍增长）

**预警阈值**：
- 单月新增 > 10 万人：警戒
- 单月新增 > 20 万人：红色预警（散户大规模进场前的合规动作）

#### F6. 韩国监管机构联合警告（事件型指标）

搜索关键词：
```
Korea Exchange Financial Investment Association warning [Month YYYY]
KOSPI margin warning statement [Month YYYY]
한국거래소 금융투자협회 경고 [YYYY]
```

**预警阈值**：
- 韩国证券交易所 + 金融投资协会发布联合警告 = **直接红色预警**（情绪过热的可靠确认信号）
- 历史参照：2025/10/17 罕见联合警告

---

## 第三步：综合阶段判断

把六类指标读数汇总到一张评分表，每类指标按颜色给分：

| 颜色 | 分值 |
|---|---|
| 🟢 绿色 | 0 分 |
| 🟡 黄色 | 1 分 |
| 🟠 橙色 | 2 分 |
| 🔴 红色 | 3 分 |

每个模块取该模块内**最高单项分**作为模块得分（不是平均，因为单一红色信号已经足够说明问题）。六个模块满分 18 分。

### 阶段映射

| 总分 | 阶段判断 | 仓位建议 |
|---|---|---|
| 0–4 | **健康牛市** | 维持配置，可适度加仓高 Beta |
| 5–8 | **牛市中期** | 维持配置，停止加仓二线/三线投机标的 |
| 9–12 | **牛市中后期 + 局部泡沫** | 减仓 20-30% 高 Beta 标的，保留龙头底仓，加仓防御性资产至 5-10% |
| 13–15 | **泡沫晚期** | 减仓 50% 高 Beta，对冲性资产至 10-15%，启动尾部风险保护（put spread） |
| 16–18 | **极端泡沫** | 减仓 70%+ 高 Beta，仅留长线龙头底仓，对冲至 15-20% |

### 必须显示的核心判断

报告头部必须用一行话给出：

```
当前阶段：[健康牛市 / 牛市中期 / 牛市中后期+局部泡沫 / 泡沫晚期 / 极端泡沫]
总分：X / 18
触发的红色指标：[列举]
建议仓位调整：[具体方向]
```

---

## 第四步：生成报告

**输出格式：HTML 文件（可下载）**

报告必须生成为 `.html` 文件，保存至 `/mnt/user-data/outputs/` 并调用 `present_files` 工具提供下载链接。不在对话中输出报告正文（图表除外）。

### HTML 文件规格（与 daily-news-briefing 风格保持一致）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>泡沫预警 [YYYY-MM-DD]</title>
<style>
  :root {
    --bg: #ffffff; --bg2: #f5f5f3; --bg3: #eeecea;
    --text: #1a1a1a; --text2: #555552; --text3: #888784;
    --border: #dddbd8; --accent: #3266ad;
    --green: #1D9E75; --yellow: #C7A11A;
    --orange: #BA7517; --red: #E24B4A;
    --font: -apple-system, "Helvetica Neue", Arial, sans-serif;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: var(--font); background: var(--bg); color: var(--text);
         font-size: 14px; line-height: 1.7; max-width: 860px;
         margin: 0 auto; padding: 32px 24px 64px; }
  h1 { font-size: 22px; font-weight: 600; margin-bottom: 4px; }
  h2 { font-size: 17px; font-weight: 600; margin: 28px 0 12px; padding-bottom: 6px;
       border-bottom: 1px solid var(--border); }
  h3 { font-size: 14px; font-weight: 600; margin: 16px 0 8px; }
  .stage-banner { padding: 16px 20px; border-radius: 8px; margin: 16px 0 24px;
                  background: var(--bg2); border-left: 4px solid var(--accent); }
  .stage-banner.red { border-color: var(--red); background: rgba(226,75,74,0.06); }
  .stage-banner.orange { border-color: var(--orange); background: rgba(186,117,23,0.06); }
  .stage-banner.yellow { border-color: var(--yellow); background: rgba(199,161,26,0.06); }
  .stage-banner.green { border-color: var(--green); background: rgba(29,158,117,0.06); }
  .score-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 10px; margin: 12px 0 20px; }
  .score-card { background: var(--bg2); border-radius: 6px; padding: 10px 12px;
                border-left: 3px solid var(--border); }
  .score-card.red { border-color: var(--red); }
  .score-card.orange { border-color: var(--orange); }
  .score-card.yellow { border-color: var(--yellow); }
  .score-card.green { border-color: var(--green); }
  .score-label { font-size: 11px; color: var(--text2); margin-bottom: 4px; }
  .score-value { font-size: 18px; font-weight: 500; }
  .score-detail { font-size: 11px; color: var(--text3); margin-top: 2px; }
  table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }
  th { background: var(--bg2); padding: 8px; text-align: left; font-weight: 500;
       border-bottom: 1px solid var(--border); }
  td { padding: 8px; border-bottom: 1px solid var(--border); }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 10px;
           font-size: 11px; font-weight: 500; }
  .badge.red { background: rgba(226,75,74,0.15); color: var(--red); }
  .badge.orange { background: rgba(186,117,23,0.15); color: var(--orange); }
  .badge.yellow { background: rgba(199,161,26,0.18); color: #846908; }
  .badge.green { background: rgba(29,158,117,0.15); color: var(--green); }
  .meta { color: var(--text3); font-size: 12px; margin-bottom: 24px; }
  .footer { margin-top: 40px; padding-top: 16px; border-top: 1px solid var(--border);
            font-size: 12px; color: var(--text3); }
</style>
</head>
<body>

<h1>泡沫预警报告 [YYYY-MM-DD]</h1>
<div class="meta">报告期: [date] | 时区: SGT (UTC+8) | 数据截至: [time SGT]</div>

<!-- 阶段判断 banner（颜色根据总分自动选择 red/orange/yellow/green）-->
<div class="stage-banner [color]">
  <h2 style="margin: 0 0 8px; border: none; padding: 0;">当前阶段判断：[阶段名称]</h2>
  <div>总分：<strong>[X / 18]</strong></div>
  <div>触发红色指标：[列举]</div>
  <div style="margin-top: 8px;">建议仓位调整：[具体方向]</div>
</div>

<!-- 6 大模块得分总览 -->
<h2>六大模块得分总览</h2>
<div class="score-grid">
  <div class="score-card [color]">
    <div class="score-label">A. 泡沫阶段</div>
    <div class="score-value">[X] 分</div>
    <div class="score-detail">[最高项关键词]</div>
  </div>
  <!-- 其他 5 个 -->
</div>

<!-- 各模块详细数据表 -->
<h2>A. 泡沫阶段判断指标</h2>
<table>
  <thead><tr>
    <th>指标</th><th>当前读数</th><th>阈值</th><th>颜色</th>
  </tr></thead>
  <tbody>
    <tr><td>GS STI 历史百分位</td><td>...</td><td>...</td><td><span class="badge [color]">[label]</span></td></tr>
    <!-- A1-A4 -->
  </tbody>
</table>

<!-- B-F 模块同上 -->

<!-- 历史阶段对照 -->
<h2>历史阶段对照</h2>
<p>1999年12月-2000年3月（互联网泡沫顶部）持续约3个月；2020年11月-2021年2月（meme stock 顶部）持续约4个月。
当前若处于"牛市中后期+局部泡沫"，历史经验显示该阶段通常持续 6–12 个月后过渡到下一阶段。</p>

<div class="footer">
  数据来源：Goldman Sachs、CBOE、FINRA、Korea Securities Depository、KOFIA、Bloomberg、Capital.com、SEC 13F filings、KRX、CSOP、Bybit、Binance。
  本报告仅作信息参考，不构成投资建议。
</div>

</body>
</html>
```

---

## 第五步：图表（必须）

每份报告至少输出 3 张图表，调用 `visualize:show_widget` 工具 inline 展示在对话中（同时 HTML 文件中也嵌入相同图表）。

### 图表 1：六大模块得分雷达图

雷达图（radar chart），6 顶点对应 A-F 模块，0-3 分刻度。

### 图表 2：核心指标历史走势（过去 12 个月）

折线图，3-4 条曲线：
- GS STI 历史百分位
- SPHB / SPLV 比值
- 0DTE 期权占比
- 韩国杠杆 ETF 净流入（次坐标轴）

### 图表 3：财报反应离散度（仅财报季激活）

柱状图，6 只半导体股的财报后 ±2 日股价反应。
红色横线标注 ±2 SD 区间。

---

## 第六步：触发器与简报模式

除了完整报告之外，以下任一条件触发"专题简报"（仅输出触发的指标 + 阶段判断变化，不需要完整 6 大模块）：

### 即时触发器（任一即生成简报）

1. NVDA / AMD / AVGO 单日跌幅 > 5%
2. NVDA / AMD 单日成交量 > 历史均值的 2 倍
3. 任何一只龙头股**财报后 36 小时反转**（盘后 +5% → 收盘 -3%）
4. ARM 单日跌幅 > 5%（联动 SoftBank 杠杆风险）
5. ARM 单日成交量 > 2,000 万股
6. 软银发布任何与 ARM 持股相关的公告
7. ARM 期权 IV 单日跳升 > 20%
8. SFTBY 单日跌幅 > 8%
9. CSOP SK Hynix 2x ETF 单日成交 > 30 亿港元
10. 韩国证券交易所 + KOFIA 联合警告
11. GS STI 单周变化进入历史 95 分位
12. 任一"宏观聪明钱"完整退出 NVDA / AMD / META / GOOG / MSFT

### 简报输出格式（不输出 HTML，仅在对话中给一段简短文字）

```
🚨 泡沫预警简报 [YYYY-MM-DD HH:mm SGT]

触发指标：[X 项]
- [指标 1]：[当前读数] vs [阈值]
- [指标 2]：...

阶段判断变化：[原阶段] → [新阶段]
即时建议：[1-2 句话的具体行动]
```

---

## 关键限制与诚实性原则

1. **承认数据缺口**：以下指标公开度不高，搜索失败时必须明确标注"数据未获取"，不可编造：
   - GS STI 实时数值（仅 GS 客户可见，依赖二手报道）
   - 0DTE 期权占比（部分需付费数据源）
   - 加密交易所代币化美股永续 OI（披露有限）
   - GS Prime Brokerage 周报（机构客户专用）

2. **避免单点回归**：当某个指标只有一个历史数据点时（如 TSMC 清仓 ARM 引发 -7.98%），不要把这个数字当成"弹性系数"反复套用，必须标注"基于单一案例的估算"。

3. **历史定位优先于绝对值**：每个指标都要给出"当前读数 vs 历史 50/75/95 百分位"，不要只报当前数值。

4. **跨市场冲突时坦白说明**：如果 A 类指标显示绿色但 F 类指标显示红色（美国本土平静但亚洲杠杆狂热），不要"取中位数"模糊处理，而是明确标注**分层判断**："美国本土投资者尚理性，但亚洲散户已显著过热，注意全球风险偏好的边际驱动力"。

5. **避免泡沫晚期的语言通胀**：不要每周都说"接近泡沫顶部"。一旦进入"泡沫晚期"判断，应锁定该判断 4-6 周，除非有明确指标退出红色区间。

6. **诚实标注修正**：如果上一份报告的判断被后续数据证伪，新报告必须显式承认（例：「上周判断为'牛市中后期'，本周因 X 指标回落，下调为'牛市中期'」）。

---

## 附录：术语对照与数据源清单

### 术语
- **GS STI** = Goldman Sachs Speculative Trading Indicator
- **SPHB** = Invesco S&P 500 High Beta ETF
- **SPLV** = Invesco S&P 500 Low Volatility ETF
- **0DTE** = Zero Days to Expiration（当日到期期权）
- **ERP** = Equity Risk Premium（股权风险溢价）
- **FINRA** = Financial Industry Regulatory Authority
- **KSD** = Korea Securities Depository（韩国证券存管局）
- **KOFIA** = Korea Financial Investment Association（韩国金融投资协会）
- **DTE** = Days to Expiration

### 数据源
- 美国本土：CBOE、FINRA、SEC EDGAR、Bloomberg、Goldman Sachs research、Yahoo Finance、Macrotrends
- 韩国本土：KSD、KOFIA、KRX、Seoul Economic Daily、Korea Herald、KED Global
- 香港：HKEX、CSOP Asset Management
- 加密：Bybit、Binance、CoinMarketCap、Bloomingbit

