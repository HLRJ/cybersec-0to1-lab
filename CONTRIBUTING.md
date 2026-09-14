# 贡献指南

感谢参与《网络安全攻防 0→1 实战 Lab》。

## 当前优先级

当前只维护中文 Core Curriculum。英文版、额外平台适配和大规模扩展暂不优先；先保证核心课程可运行、可理解、可复现、可验证。

## 贡献必须遵守

- 不提交针对真实公网目标的扫描结果、凭据、Token、密钥或敏感数据；
- 不复制商业课程或外部平台受版权保护的题目、答案和课程正文；
- 每个 Lab 必须有明确学习目标、实验动作、证据和 Gate；
- 涉及安全缺陷时，必须解释根因，并给出修复与重新验证；
- 教学代码优先小而清晰，不为了“工程感”引入无必要的复杂组件；
- 新工具必须说明它解决什么问题，不能用工具替代原理解释。

## 提交风格

优先使用小而可审查的提交。建议 Conventional Commits，例如：

```text
docs: refine S01 TCP lab
feat: add S00 environment checker
test: add target scope validation
fix: prevent public target resolution
```

课程结构调整必须同时检查 `CURRICULUM.md` 与 `docs/CURRICULUM_DESIGN.md` 是否一致。
