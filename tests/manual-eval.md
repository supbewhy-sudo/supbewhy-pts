# supbewhy-pts 人工行为评测

这份协议验证 Skill 在真实模型中的触发和输出行为。结构验证通过不等于行为验证通过；每个案例必须在互不共享上下文的新任务中运行，避免前一案例影响后一案例。

## 测试前提

1. 把本仓库的 `supbewhy-pts/` 安装到项目级或个人级 Skill 目录。
2. 重启 Codex，确认 Skill 可被发现。
3. 每个案例打开一个新的 Codex 任务。
4. 原样发送 `tests/cases.json` 中对应案例的 `input`，不要追加提示或暗示期望答案。
5. 保存模型完整输出，并按下面的标准判定。

## 单项判定

每个案例检查六个维度：

| 维度 | 通过条件 |
| --- | --- |
| 触发 | 与 `should_trigger` 一致；品牌名或无关缩写不会误触发 |
| 模式 | 与 `expected_mode` 一致，例如默认只交付 Prompt、缺料时提问、解释模式才解释 |
| 意图 | 保留用户真正要完成的任务，没有把“改 Prompt”误当成“执行 Prompt” |
| 范围 | 任务规模、交付数量和复杂度没有被擅自扩大或缩小 |
| 约束 | 满足 `required`，且没有出现 `forbidden` 中的行为 |
| 事实 | 不补造用户未提供的事实；缺失信息被提问、标记为假设或保留占位符 |

只有六个维度全部通过，案例才记为通过。措辞不同不是失败；改变任务、漏掉硬约束、误触发或宣称完成未执行的工作均为失败。

## 15 个必测案例

| ID | 主要风险 |
| --- | --- |
| `scope-natural-business-review` | 把自然商业审查过度编译成完整尽调 |
| `remove-performative-noise` | 删除思考表演时连可见交付物一起删掉 |
| `missing-source-question` | 缺少源材料仍直接补造内容，或连续追问 |
| `from-scratch-competitor-prompt` | 无法从明确需求生成可执行 Prompt |
| `brand-alias-only` | 作者标识导致误触发 |
| `unrelated-pts-acronym` | 无关 PTS 缩写导致误触发 |
| `pst-contextual-typo` | 在明确转换语境中无法兼容 PST 误输入 |
| `unrelated-pst-acronym` | 无关 PST 缩写导致误触发 |
| `preserve-claude-target` | 擅自把明确的 Claude 目标改为 GPT-5.6 |
| `preserve-midjourney-syntax` | 破坏 Midjourney 参数和必要语法 |
| `preserve-image-identity-constraints` | 过度压缩图像身份、构图等硬约束 |
| `explain-existing-prompt` | 用户要解释时只给结果，或解释替代最终 Prompt |
| `explain-from-brief` | 从零生成时假装存在“原 Prompt”并虚构修改项 |
| `no-questions-use-placeholders` | 用户禁止提问后擅自猜测关键信息 |
| `pts-and-execute-separated` | 把“转换并执行”固化成 PTS 的默认产品能力 |

## 结果记录

复制下表，每个案例填写 `通过` 或 `失败`，失败时附上触发条件和输出片段：

| ID | 结果 | 失败维度 | 证据或备注 |
| --- | --- | --- | --- |
| scope-natural-business-review |  |  |  |
| remove-performative-noise |  |  |  |
| missing-source-question |  |  |  |
| from-scratch-competitor-prompt |  |  |  |
| brand-alias-only |  |  |  |
| unrelated-pts-acronym |  |  |  |
| pst-contextual-typo |  |  |  |
| unrelated-pst-acronym |  |  |  |
| preserve-claude-target |  |  |  |
| preserve-midjourney-syntax |  |  |  |
| preserve-image-identity-constraints |  |  |  |
| explain-existing-prompt |  |  |  |
| explain-from-brief |  |  |  |
| no-questions-use-placeholders |  |  |  |
| pts-and-execute-separated |  |  |  |

## 发布门槛

- 15 个案例全部通过，才可声明“行为评测通过”。
- 任一误触发、任务范围漂移、目标平台被改写或事实补造，均阻止发布。
- 修改规则后必须重跑全部 15 个案例，不能只复测失败项。
- 没有完成这轮独立前向测试时，只能声明“行为评测语料已建立”，不能声明“行为评测已通过”。
