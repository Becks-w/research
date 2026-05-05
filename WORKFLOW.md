# 🚀 工作流速查卡

> 每次发布新报告，照着这张卡走就行。

---

## 发布新报告（4 步走）

### 1️⃣ 把新报告放进对应文件夹

```
个股分析  →  stocks/
市场周报  →  weekly/
每日简报  →  daily/
```

文件名命名格式：`ticker-YYYY-MM.html` 或 `YYYY-wXX.html`

### 2️⃣ 跑索引脚本

```bash
python3 scripts/build_index.py
```

### 3️⃣ Git 三连

```bash
git add .
git commit -m "Add [报告名称]"
git push
```

### 4️⃣ 等 30 秒，刷新网址

✅ 完成！新报告自动出现在主页最顶部。

---

## 📦 常用 Git 命令速查

| 操作 | 命令 |
|------|------|
| 查看状态（哪些文件变了） | `git status` |
| 查看修改了什么 | `git diff` |
| 撤销未提交的修改 | `git checkout -- 文件名` |
| 查看历史提交 | `git log --oneline` |
| 拉取远端最新（防冲突） | `git pull` |

---

## ⚠️ 万一出了问题

**问题 1：`git push` 失败，提示 "rejected"**

可能是云端有更新。先拉再推：
```bash
git pull --rebase
git push
```

**问题 2：跑脚本报错 "python3: command not found"**

Mac/Linux 用：`python3 scripts/build_index.py`  
Windows 用：`python scripts/build_index.py`

**问题 3：主页没更新**

- 等 1-2 分钟（GitHub Pages 部署需要时间）
- 浏览器强制刷新：`Cmd+Shift+R`（Mac）/ `Ctrl+F5`（Windows）
- 检查 GitHub 仓库的 Actions 页面，看部署是否成功

---

## 💡 命名速查

| 类型 | 模板 | 例子 |
|------|------|------|
| 个股分析 | `{ticker}-YYYY-MM.html` | `duol-2026-04.html` |
| 个股深度（细分） | `{ticker}-{topic}-YYYY-MM.html` | `arm-moat-2026-03.html` |
| 横向对比 | `{theme}-YYYY-MM.html` | `saas-comparison-2026-04.html` |
| 市场周报 | `YYYY-wXX.html` | `2026-w17.html` |
| 每日简报 | `YYYY-MM-DD.html` | `2026-04-29.html` |

✅ 全部小写 + 连字符  
❌ 不用空格 / 中文 / 下划线 / `final` / `v2`
