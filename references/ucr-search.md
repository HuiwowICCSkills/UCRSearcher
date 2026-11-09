# UCR 检索实测记录（2026-11-09）

## 端点

`https://ucr.irmct.org/api/Record/GetRecentlyFiled`

- 公开、无需登录
- 返回 JSON 数组，约 47 KB（实测）
- 字段：`documentTitle`、`caseNumber`、`caseDescription`、`docTypeDesc`、`docFilingDate`、`filingDate`、`signatureDate`、`recordID`、`documentID`

实测 `genocide` 在最近归档中 0 条；这**不**表示 UCR 全库没有相关资料。

## 边界

- 该端点只覆盖最近归档，不是完整 UCR 名册。
- 完整 UCR 搜索需要注册/登录账号；本 skill 不尝试登录、不保存凭据。
- 需要完整检索时，交给 `international-law-manual-research` 的人工交接流程。
