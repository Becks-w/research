# Becks Research Archive 📊

> 个人投研档案库 · 自动化研报管理系统

这是一个让你**像写日记一样发布研报**的极简系统。每份研报都是独立的 HTML 文件，通过 GitHub Pages 永久托管，主页自动生成，支持搜索和分类。

---

## 🎯 它能做什么

- ✅ 自动扫描所有 HTML 报告并生成主页索引
- ✅ 按"个股 / 周报 / 日报"三大类自动分类
- ✅ 主页支持关键词搜索 + 分类筛选
- ✅ 通过 GitHub Pages 免费托管，永久公开链接
- ✅ 一份报告 = 一个固定 URL，方便分享和归档

---

## 📁 文件夹结构

```
becks-research/
├── index.html              ← 主页（自动生成，请勿手动编辑）
├── README.md               ← 你正在看的这份文档
├── stocks/                 ← 📈 个股分析报告放这里
│   ├── duol-2026-04.html
│   └── saas-comparison-2026-04.html
├── weekly/                 ← 📊 市场周报放这里
├── daily/                  ← 📰 每日简报放这里
└── scripts/
    └── build_index.py      ← 索引生成脚本
```

---

## 🚀 第一次部署到 GitHub Pages（5 分钟）

### Step 1：注册 GitHub 账号（如已有，跳过）

去 [github.com](https://github.com) 注册一个账号。建议用户名简洁好记，因为这会成为你的网址：`https://你的用户名.github.io/becks-research/`

### Step 2：安装 Git（如已有，跳过）

- **Mac**：打开"终端"，输入 `git --version`。如果没装会提示你安装。
- **Windows**：去 [git-scm.com](https://git-scm.com/download/win) 下载安装包，一路 Next。

### Step 3：在 GitHub 上创建一个新仓库

1. 登录 GitHub，点右上角 `+` → `New repository`
2. 仓库名填 `becks-research`
3. 设为 **Public**（公开，这样 Pages 才能用）
4. **不要**勾选"Add a README"（我们已经有了）
5. 点 `Create repository`

### Step 4：把这套文件上传到 GitHub

打开终端（Mac）或 Git Bash（Windows），切换到本档案库的文件夹（即 `becks-research` 目录），然后逐行执行：

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/becks-research.git
git push -u origin main
```

如果是第一次用 git，可能会要你输入用户名和密码。**密码要用 Personal Access Token**，不是你的 GitHub 登录密码：
- 在 GitHub 网页：Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
- 勾选 `repo` 权限
- 生成后复制下来（只显示一次！），用这个当密码

### Step 5：开启 GitHub Pages

1. 在 GitHub 仓库页面，点 `Settings`（顶部菜单）
2. 左侧菜单点 `Pages`
3. Source 选 `Deploy from a branch`
4. Branch 选 `main`，文件夹保持 `/ (root)`
5. 点 `Save`
6. **等大约 1-2 分钟**，刷新页面，会看到：
   > Your site is live at `https://你的用户名.github.io/becks-research/`

打开这个网址，就能看到你的研报库主页了。🎉

---

## 📝 日常工作流：发布新研报

### 场景：我刚生成了一份新报告 `crwd-deep-dive-2026-05.html`

**步骤 1：把文件放到对应文件夹**

```
新的个股分析 → 放入 stocks/
新的市场周报 → 放入 weekly/
新的每日简报 → 放入 daily/
```

**步骤 2：运行索引生成器**

打开终端，进入档案库根目录，执行：

```bash
python3 scripts/build_index.py
```

输出大概长这样：

```
🔍 扫描研报文件夹...
✓ 发现 3 份报告：
  - 个股分析: 3 份
  - 市场周报: 0 份
  - 每日简报: 0 份

📝 生成主页 index.html...
✓ 已写入 /path/to/becks-research/index.html

🚀 完成！下一步：
   git add .
   git commit -m "Update reports"
   git push
```

**步骤 3：推送到 GitHub**

```bash
git add .
git commit -m "Add CRWD deep dive (2026-05)"
git push
```

**步骤 4：等 30 秒**

GitHub Pages 会自动重新部署。刷新你的主页 URL，新报告卡片就会出现在最顶部。

---

## 💡 文件命名规范（强烈推荐）

好的命名 = 未来 1 年后还能找到自己写的东西。

| 类型 | 命名格式 | 例子 |
|------|---------|------|
| 个股分析 | `{ticker}-YYYY-MM.html` | `duol-2026-04.html` |
| 个股深度（同月多份） | `{ticker}-{topic}-YYYY-MM.html` | `arm-moat-2026-03.html` |
| 横向对比 | `{topic}-YYYY-MM.html` | `saas-comparison-2026-04.html` |
| 周报 | `YYYY-wXX.html` | `2026-w17.html` (ISO 周数) |
| 日报 | `YYYY-MM-DD.html` | `2026-04-29.html` |

**铁律：**
- ✅ 全部小写 + 用连字符分隔（不要用空格、中文、下划线）
- ✅ 日期放结尾，不要放开头（按字母排序时同主题的会聚在一起）
- ❌ 不要用 `final`、`v2`、`new` 这种字眼

---

## 🔧 让自动索引提取得更好（小技巧）

`build_index.py` 会从每份 HTML 提取标题、日期、摘要。要让提取效果好，写报告时记住：

1. **`<title>` 标签**要清晰：`<title>DUOL 估值分析 | 2026-04</title>`，竖线后面的会被忽略
2. **第一段 `<p>` 要写一段总结性介绍**，索引会自动抓取作为卡片摘要
3. **正文里写明数据日期**：用 "数据截止：2026 年 4 月 28 日" 这样的格式，索引会自动识别

我（Claude）每次帮你生成新报告时都会遵循这些规范。

---

## ❓ 常见问题

**Q: 我能修改主页样式/分类吗？**  
A: 可以。改 `scripts/build_index.py` 里的 `CATEGORIES` 字典就能加新分类（比如增加"行业研究" `industry/`）。颜色、布局也都在脚本里。

**Q: 我能删除已发布的报告吗？**  
A: 直接删除文件夹里的 HTML，再跑一次 `build_index.py`，再 `git push` 即可。

**Q: 我的网址能换成自定义域名吗？（比如 becks-research.com）**  
A: 可以。买域名后在 Settings → Pages 里填入"Custom domain"，再去域名服务商那里加 CNAME 记录。具体流程下次需要时再说。

**Q: 报告里的图表会失效吗？**  
A: 不会。HTML 里的 Chart.js 是从 CDN 加载的，不依赖你的服务器。所有交互、雷达图、气泡图都能正常工作。

**Q: 我要保护某些报告不公开怎么办？**  
A: 这套系统是公开档案库。如果有私密研报，建议另开一个 Private 仓库存储，不发布到 Pages。

---

## 🔄 升级路径

- **现在（层次二）**：手动下载 → 放文件 → 跑脚本 → push。适合每周 1-3 份报告。
- **未来可选（层次三）**：用 GitHub Actions 自动跑 build_index.py，你只需要 push 文件就够了。报告积累到 50+ 份再考虑。
- **远景**：Hugo / Astro 静态站点，支持 Markdown 写作 + 标签系统 + RSS 订阅。报告积累到 100+ 份再考虑。

---

## 📜 自动生成

主页 `index.html` 由 `scripts/build_index.py` 自动生成，请勿手动编辑——你的修改会在下次运行脚本时被覆盖。

要修改主页样式或行为，改脚本本身。

---

*Built for Becks · 2026*
