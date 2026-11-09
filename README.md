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
