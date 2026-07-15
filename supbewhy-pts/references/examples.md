# PTS Examples

## 1. Natural request: preserve scope

### Input

```text
PTS 一下：我准备把这份商业计划拿去跟潜在合作方聊。请检查市场机会、用户需求、赚钱方式、成本和执行难度，告诉我哪里容易被质疑、缺什么证据、主要风险和下一步先补什么，最后判断继续推进、改完再推进还是暂停。
```

### Correct output shape

```text
请审查下面的商业计划，判断它目前是否适合与潜在合作方讨论。

【商业计划】
{{粘贴或上传商业计划}}

从市场机会、用户需求、商业模式、成本和执行难度五个方面检查计划。区分材料中已有的事实、未经验证的假设和仍然缺失的证据，不要自行补造数据。

请输出：
1. 最终判断：继续推进、改完再推进或暂停，并说明核心原因。
2. 最容易被合作方质疑的地方及其证据缺口。
3. 当前最关键的风险。
4. 下一步最值得优先验证或补充的事项。

不要只做摘要；主动指出逻辑跳跃、隐含假设和关键执行依赖。材料不足时给出暂定判断，并说明哪些信息最可能改变结论。
```

Why it passes: it preserves the original decision and requested dimensions without inventing fixed counts, confidence scores, a full investment audit, or business metrics that may not apply.

## 2. Already simple: keep it simple

### Input

```text
PTS 一下：把以下中文翻译成自然英文，保留轻松口语感。只输出译文，不解释。
```

### Output

```text
把以下中文翻译成自然的英文，保留轻松口语感。只输出译文，不解释。

【原文】
{{粘贴中文原文}}
```

Why it passes: only the missing input slot is added. Headings, personas, scoring, and review steps would be over-compilation.

## 3. Missing source: ask before compiling

### Input

```text
PTS 一下，帮我整理会议纪要。
```

### Response

```text
请把会议录音转写、聊天记录或现有笔记发给我；如果纪要有明确用途（内部同步、客户确认或任务跟进），也请一起说明。
```

Why it passes: the source material changes the result and cannot be invented. One consolidated question overrides the default final-prompt mode.

## 4. Questions forbidden: use placeholders

### Input

```text
PTS 一下，不要问我问题：帮我写一个分析财报的 Prompt。
```

### Output shape

```text
请分析 {{公司名称}} 的 {{财报期间}} 财报，面向 {{受众或使用目的}}。

以 {{财报文件或来源}} 为主要依据，区分已披露事实、管理层指引和你的分析；无法核实的数据不要补造。

重点分析 {{用户关心的维度}}，并输出核心结论、主要依据、关键风险、仍需验证的信息和下一步建议。
```

Why it passes: placeholders preserve uncertainty without forcing a long generic financial-analysis template.

## 5. Preserve another target platform

### Input

```text
PTS 这段给 Claude 用的提示词：审查代码变更，只列出会导致真实回归的问题，并引用文件位置。
```

### Required behavior

Keep Claude as the target. Clarify severity and evidence only if needed; do not silently migrate the prompt to GPT-5.6.

## 6. Explain a prompt created from a brief

When the user asks for a new prompt and an explanation, use:

1. `需求缺口与采用的假设`
2. `PTS 后的完整 Prompt`
3. `关键构建依据`

Do not invent an “原 Prompt 的主要问题” section when the user never supplied an original prompt.

## 7. Brand and acronym boundaries

- `supɃewhY`, `supBewhY`, or `supbewhy` alone: discovery intent; do not transform.
- `PST 一下这段提示词：...`: obvious typo in context; run PTS without lecturing the user.
- `PST 和北京时间相差多少小时？`: time-zone question; do not run PTS.
- `视频时间戳里的 PTS 和 DTS`: media timestamp question; do not run PTS.
