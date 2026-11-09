# UCRSearcher 部署指引

检索 IRMCT Unified Court Records（UCR）公开 recent-filings 元数据。只访问 `ucr.irmct.org`。

仓库：<https://github.com/HuiwowICCSkills/UCRSearcher>（公开）。

## 1. 环境

Python 3.10+，依赖 `requests`；无需浏览器或登录。

## 2. 安装

```powershell
git clone https://github.com/HuiwowICCSkills/UCRSearcher.git "$env:USERPROFILE\.codex\skills\UCRSearcher"
python -m pip install -r "$env:USERPROFILE\.codex\skills\UCRSearcher\requirements.txt"
```

## 3. 自检

```powershell
& "$env:USERPROFILE\.codex\skills\UCRSearcher\run.ps1" doctor
```

## 4. 使用

```powershell
$ucr = "$env:USERPROFILE\.codex\skills\UCRSearcher\run.ps1"
& $ucr search 'Akayesu' --limit 10 --out './ucr.json'
```

## 5. 排错

| 现象 | 处理 |
| --- | --- |
| 结果很少 | 公开端点只覆盖最近归档；不是全库 |
| 需要完整检索 | 使用 `international-law-manual-research` 的登录交接流程 |
| 空结果 | 只说明最近归档没有匹配；不能推断 UCR 全库无资料 |

## 6. 边界

本 skill 不登录、不下载 UCR 文件；完整 UCR 检索需要注册账号。

## 实测效果（2026-11-09）

以下命令与结果来自本机 `~/.codex/skills/UCRSearcher` 的实网运行；检索日期 2026-11-09（Asia/Shanghai），输出为该次运行实际返回的 JSON 报告。

```powershell
& .\run.ps1 search 'Akayesu' --limit 5
```

- 状态：`ok`；服务端/索引报告 `total = 2`；本次返回 2 条（少于 `--limit 5`，公开端点确实只有 2 条命中）。
- 代表性结果：

| 题名 | 类型 / 日期 | 链接 |
| --- | --- | --- |
| Decision on Jean-Paul Akayesu's Urgent Request to the President (English, 4 Pages) | Decision；06/07/2026 | https://ucr.irmct.org/ |
| Urgent Request to the President (English, 2 Pages) | Request；25/06/2026 | https://ucr.irmct.org/ |

> 说明：本次只调用 UCR 公开的 `GetRecentlyFiled` 端点（`https://ucr.irmct.org/api/Record/GetRecentlyFiled`，HTTP 200，JSON，47,188 字节），返回的是 public recent-filings **元数据**，不是 UCR 全库检索结果，也不含文件正文。两条记录同属案件 MICT-13-30-ES.1（AKAYESU, JEAN-PAUL），能证明的只是“公开最近归档里有该案的两份新文书”，不能据此推断 UCR 全库只有这两份，也不能代替裁判理由；完整 UCR 检索需要注册账号，本 skill 不登录、不下载正文。
