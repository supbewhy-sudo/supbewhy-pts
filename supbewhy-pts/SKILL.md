---
name: supbewhy-pts
description: Use when the user uses PTS as a prompt-transformation command, uses PST as an obvious typo in that same context, asks to optimize or rewrite an existing prompt for GPT-5.6, or asks to create a GPT-5.6 prompt from a brief. Do not use for unrelated meanings of PTS/PST, ordinary task execution, bare author aliases supɃewhY/supBewhY/supbewhy, or other-model prompts unless the user explicitly invokes PTS or requests migration.
---

# supɃewhY - PTS

PTS means **Prompt To Spec**: turn an existing prompt or brief into the smallest sufficient task specification for reliable execution.

**Golden rule:** Task immutable; prompt mutable.

## Scope

PTS has two functions:

1. Transform an existing prompt.
2. Create a prompt from a user brief.

Do not treat PTS as a prompt polisher, prompt compressor, or task-execution mode.

## Non-negotiable rules

1. Preserve the task, audience, use context, target model/tool, desired outcome, and every outcome-critical constraint.
2. Optimize execution quality, not similarity to the original wording and not prompt length.
3. State each instruction once. Remove only content that does not change the expected result.
4. Use functional slots internally, but render only the structure the task needs. Never add empty or ceremonial headings.
5. Preserve the task's scope envelope: expected depth, length, number of deliverables, professional level, and use scenario.
6. Do not invent facts, source content, user preferences, permissions, or target-platform syntax.
7. `supɃewhY`, `supBewhY`, and `supbewhy` identify the author and works. They do not execute PTS by themselves.
8. Treat `PST` as a typo only when it is clearly used as a prompt-transformation command. Always call the method `PTS` in output.
9. **Do not execute the compiled task as a PTS feature.** Prompt transformation ends when the prompt is delivered; any separately requested execution follows the host agent's normal rules.

## Workflow

1. **Resolve the source.** Use the prompt or brief in the current message, or the nearest unambiguous one in context. If none exists, ask once for the missing source.
2. **Extract the task contract.** Identify the goal, deliverable, audience, inputs, target platform, critical constraints, permissions, output requirements, success conditions, and implied scope envelope.
3. **Remove noise.** Delete generic authority claims, empty intensity words, performative thinking rituals, duplicated rules, irrelevant examples, and unrelated tool instructions.
4. **Handle necessary gaps.** Infer only when one low-risk interpretation is obvious. Ask one consolidated question for outcome-changing ambiguity. If the user forbids questions, use explicit `{{placeholders}}`.
5. **Apply Scope Fidelity.** Add a requirement only when it resolves a real gap, materially improves usability or verification, fits this task, and would reduce quality if removed. If any condition fails, omit it.
6. **Rebuild from first principles.** Produce a lean, self-contained prompt. Keep simple tasks simple; use sections only when they reduce ambiguity.
7. **Validate.** Confirm the task, target platform, scope envelope, and critical constraints are unchanged; every added line has a purpose; the result is copy-ready.

Read `references/rulebook.md` only when a keep/delete/complete/scope decision needs detail. Read `references/examples.md` only for edge cases or pattern comparison. Read `references/gpt-5-6-basis.md` only when the user asks about the methodology, official basis, or engine version.

## Output contract

### Default

Return only the final prompt in one copyable code block. Do not add a preamble, score, changelog, or method explanation.

### Missing outcome-changing information

Ask one consolidated question instead of emitting a speculative final prompt. This state overrides Default mode.

### Explain an existing prompt

Only when the user asks to explain, analyze, compare, or say why, output:

1. 原 Prompt 的主要问题
2. PTS 后的完整 Prompt
3. 关键修改依据

### Explain a prompt created from a brief

When no original prompt exists, output:

1. 需求缺口与采用的假设
2. PTS 后的完整 Prompt
3. 关键构建依据

## Final check

- Same task, audience, target platform, and desired result?
- Same scope and delivery complexity unless the user requested expansion?
- Every critical constraint preserved?
- Every addition passes Scope Fidelity?
- No repeated, vague, contradictory, or performative line?
- Correct output mode and immediately usable result?
