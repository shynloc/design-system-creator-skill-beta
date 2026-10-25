---
name: design-system-creator
display_name: "Design System Creator"
description: "统一个人设计工作台：建立可解释 Design Kernel，生成 Creative Direction，并按同一视觉身份制作或改进 Web、DOCX、PPTX、XLSX、PDF 与 Charts；包含多模态能力门禁、素材收集事务、Runtime Skill 编译和统一 QA。"
version: 1.0.0-beta.1
user-invocable: true
---

# Design System Creator 1.0.0-beta.1

Design System Creator 不是固定审美模板。它统一三层能力：**Identity / Creative Direction / Production**。

核心总线：`Design Kernel + Active Profile + Content Semantics + Task Context + Temporary Art Direction + Medium Constraints = Resolved Design Context`。

## 0. 强制纪律
1. 涉及图片先读 `@references/CAPABILITY-GATE.md`。不能确认模型真的能看图，就禁止描述图片内容。
2. 连续发参考图时读 `@references/REFERENCE-INTAKE.md`：COLLECTING 只收不分析；用户说“上传完成”后先校验；用户再说“开始分析”才进入视觉分析。
3. 设计判断区分 `OBSERVED / INFERRED / CONFIRMED`；高置信度推断不等于用户确认。
4. Design Kernel 是长期身份边界，不是固定模板；本次表达由 Creative Direction 决定。
5. 一次性的情绪、色温、密度和实验构图放在 Temporary Art Direction，默认不写回长期 Kernel。
6. 真实附件/文件优先；不完整就标注，不补造事实、数据或视觉内容。
7. 能真实渲染、打开、截图时必须实际 QA；没有证据不能写 PASS。
8. Portable Export 默认不包含私人原图、私人文档全文、绝对路径、密钥或受限资产。

## 1. 自动路由
用户不需要先选模式。内部路由：
- `DISCOVER`：发现审美与 Anti-style。
- `BUILD`：建立/升级 Kernel、Tokens、Profiles、Runtime Skill。
- `CREATE`：按长期或临时上下文制作作品。
- `REFINE`：精准改稿，限制修改范围，可回滚。
- `AUDIT`：检查 Design System / 作品漂移与质量。
- `EXPORT`：Portable / Runtime Skill / 项目备份。

只有歧义会显著改变结果时才问最小问题。阶段与状态定义见 `@references/WORKFLOW-STATES.md`。

## 2. 没有 Kernel 怎么办
- 用户只是想马上做作品：建立一次性 `TEMPORARY_CONTEXT`，先完成当前任务，不强迫完整审美访谈。
- 用户明确要长期个人设计系统：Capability Gate → Reference Intake → Evidence → Preference Interview → Design Kernel → Preview → Confirm → Compile。
- 已有 Kernel：直接读取，不重复采访已确认偏好。

## 3. 统一工作流
1. ROUTE：识别意图。
2. CAPABILITY：探测 vision、attachments、filesystem、archive、browser/screenshot、artifact generation。
3. SOURCE：读取真实材料并按 `@references/SOURCE-EVIDENCE.md` 建立 source/evidence map。
4. IDENTITY：加载或创建 Design Kernel。
5. CONTENT：读 `@references/CONTENT-SEMANTICS.md`，形成媒介中立的 Content Semantics。
6. DIRECTION：读 `@references/CREATIVE-DIRECTION.md` 和 `@references/DESIGN-RESEARCH.md`；必要时按 `@references/VISUAL-PITCH.md` 做真实可看提案。
7. RESOLVE：生成 `resolved-design-context.json`。
8. REVIEW：默认保留一次主要视觉审阅；正式成品文案按 `@references/AUDIENCE-COPY.md` 独立处理。
9. RENDER：读 `@references/MEDIUM-ROUTING.md` 和对应 Renderer。
10. QA：Identity + Creative + Medium + Technical。
11. DELIVER：交付实际文件、验证状态、版本、剩余 BLOCKED/NOT_TESTED。

## 4. Design Kernel
读 `@references/DESIGN-KERNEL.md`。基本链路：
`References → Evidence → Preference Model → Design DNA → Foundation Tokens → Semantic Tokens → Profiles → Medium Rules → Runtime Skill`。

Reference 支持 `core / positive / partial / negative / neutral` 和维度级正负偏好；核心规则保留 provenance 与 confidence。

## 5. Creative Direction
读 `@references/CREATIVE-DIRECTION.md`。它回答“这次怎么表达”，至少包含 audience、goal、narrative、visual metaphor、visual signatures、layout、typography、asset strategy、density、motion/interaction、temporary direction、avoid、medium notes。

未锁定方向时可给 2–3 个真正不同的可看方案；只换色不算不同方向。

## 6. Renderer
完整测试版包含六类逻辑 Renderer：Web、DOCX、PPTX、XLSX、PDF、Charts。优先调用宿主原生 artifact 能力；没有能力就明确降级，不伪造文件已生成。

Web 可运行 `scripts/build_visual_pitch.py`；有本地 Chromium/Chrome 时 `scripts/visual_qa.py` 会真实截图，没有则准确标记 BLOCKED。

## 7. Runtime Skill
长期 Kernel 确认后：
```bash
python scripts/design_studio.py compile-runtime --project <workspace> --out <runtime-dir>
python scripts/design_studio.py package --path <runtime-dir> --out <runtime.zip>
```
Runtime Skill 日常只负责解析当前任务、选择 Profile、生成 Resolved Design Context、调用 Renderer、执行 QA；不重新发明用户审美。

## 8. Beta 验收
```bash
python scripts/design_studio.py self-test
python tests/run_tests.py
```
然后按 `tests/E2E-TEST-PLAN.md` 做真实全链路测试。Beta 表示尚待真实使用反馈，不表示功能缺项。
