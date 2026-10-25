---
name: {{slug}}-design-runtime
display_name: "{{display_name}} Design Runtime"
description: "按已确认的 Design Kernel 为 Web、DOCX、PPTX、XLSX、PDF 与 Charts 提供一致设计身份，并执行媒介适配和 QA。"
version: {{system_version}}
---

# {{display_name}} Design Runtime

唯一长期视觉事实源：`references/design-kernel.json`。

顺序：读取 Kernel → 解析任务/内容/媒介/临时方向 → 选择 Profile → 生成 Resolved Design Context → 读取 Medium Spec → 生产 → Identity/Creative/Medium/Technical QA。临时变化只有用户明确要求长期保留时才写回 Kernel。
