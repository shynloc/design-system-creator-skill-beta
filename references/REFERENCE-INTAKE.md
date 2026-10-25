# Reference Intake Transaction

状态：`IDLE → COLLECTING → SEALED → VALIDATING → READY → ANALYZING`。

COLLECTING → SEALED 必须由用户明确触发，不根据沉默、时间或“已经发了很多张”推断。

- `上传完成`：停止收集、进入校验，不分析。
- `开始分析`：用户确认接收情况后才进入视觉分析。

COLLECTING 期间只能确认接收、可靠时计数、注册 Reference ID、记录权重/备注、等待更多素材。禁止风格总结、配色建议、Design DNA 推断和自动跳阶段。

权重：core / positive / partial / negative / neutral。partial 支持 `positive_dimensions` 与 `negative_dimensions`。

输入顺序：Multi-Attachment → Sequential Attachment → Folder（仅 filesystem）→ Archive（仅 extract）→ Contact Sheet（只做宏观判断）→ URL/Remote（权限与隐私允许）。Seal 后先报告可读/不可读、重复、低分辨率/Contact Sheet、授权疑点。
