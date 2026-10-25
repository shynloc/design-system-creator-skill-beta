# Architecture

四层：Orchestrator、Design Kernel、Creative Director、Renderers + QA。

数据流：`Source → Content Semantics → Design Kernel → Creative Direction → Resolved Design Context → Renderer → Artifact → QA`。

规则优先级：安全/真实性/宿主限制 → 用户本次明确要求 → CONFIRMED Kernel → Profile → Temporary Direction → Creative proposal → Renderer defaults。

长期规则与临时方向严格分离；没有用户明确确认，临时改稿不写回 Kernel。
