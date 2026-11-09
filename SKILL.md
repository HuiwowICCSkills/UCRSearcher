---
name: UCRSearcher
description: 检索 IRMCT Unified Court Records（UCR）的公开 recent-filings 端点，按案号、案件名、文书标题和类型过滤；明确区分公开新近文件与需要登录的完整 UCR 检索。
---

# UCRSearcher

> **`<skill-dir>`** = 本 SKILL.md 所在目录。核心脚本为 `<skill-dir>/scripts/ucr_search.py`；Windows 用 `<skill-dir>/run.ps1`，macOS/Linux 用 `<skill-dir>/run.sh`。部署与排错见 [README.md](README.md)。

这个 skill 只做 `ucr.irmct.org` 一个站点，且只使用无需登录的公开 `GetRecentlyFiled` 端点：

- `search`：按文书标题、案号、案件名、文书类型和日期过滤最近归档记录；
- 不提供 `fetch`：公开端点只有元数据，完整 UCR 检索和文件下载需要注册账号，本 skill 不尝试登录；
- `doctor`：探测公开 recent-filings 端点。

## 命令

```powershell
& '<skill-dir>/run.ps1' search 'Akayesu' --limit 10 --out './ucr-search.json'
& '<skill-dir>/run.ps1' search 'ICC-01/04' --limit 5
& '<skill-dir>/run.ps1' doctor
```

通用参数：`--out`、`--cache`、`--cache-ttl`、`--offline`、`--timeout`；`search` 另有 `--limit`（1..50）、`--offset`。

## 结果边界

- `GetRecentlyFiled` 只返回**最近归档**的公开记录，不是整个 UCR 名册；`total` 是本次过滤后的条数，不能写成 UCR 全库命中数。
- 结果是元数据，不含文书正文。需要完整 UCR 登录检索时，使用 `international-law-manual-research` 的人工交接流程，或由用户在自己的账号下操作。
- `status=ok` 且 `total=0` 只表示最近归档中没有匹配项，不表示 UCR 全库没有相关资料。
- 不要把 UCR 记录当作 Legal Tools 或 ICTY/ICTR 官方页面的替代；三者的覆盖范围和文号体系不同。

## 参考

- 2026-11-09 实测：`GetRecentlyFiled` 字段、公开范围与登录限制：[references/ucr-search.md](references/ucr-search.md)
- 部署、环境与排错：[README.md](README.md)
