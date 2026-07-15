# GPT-5.6 Methodology Basis

## Snapshot

- Engine target: GPT-5.6
- Reviewed: 2026-07-15
- Official guide: https://developers.openai.com/api/docs/guides/latest-model

This file records the basis of PTS rules. It is a maintained interpretation, not a verbatim copy of the official guide. PTS is an independent project, not an official OpenAI product or Skill.

## 1. GPT-5.6-specific direction

The official GPT-5.6 guide says the model is better at inferring the user's underlying goal and intended level of work from context. Prompts often do not need to prescribe every thinking step, but should still provide domain context, hard constraints, approval boundaries, success criteria, and a rule for important ambiguity.

PTS implements this as:

- Extract the real task before rewriting.
- Remove performative thinking steps unless a visible deliverable depends on them.
- Preserve outcome-critical context and constraints.
- Ask one consolidated question when an ambiguity can change the result.
- Preserve the intended level of work through Scope Fidelity.

## 2. Lean-prompt guidance

The official guide recommends:

- Remove repeated instructions and unnecessary examples incrementally.
- State each instruction once.
- Expose only task-relevant tools and keep descriptions concise.
- Keep examples and style guidance when they encode a product requirement or correct a measured failure.
- Re-run representative evaluations after changes.

PTS implements this as functional deletion rather than blind shortening. Long constraints remain when they prevent identity drift, factual invention, format loss, or another measurable failure.

## 3. Autonomy and approval guidance

The official guide recommends compact, proportional boundaries for agentic tasks and confirmation before external, destructive, costly, or scope-expanding actions.

PTS applies this only when compiling an agentic prompt. PTS itself is not a task-execution mode.

## 4. Length and style guidance

The official guide warns that broad brevity instructions may produce answers that are too short. It recommends stating what a short answer must preserve and what lower-value detail may be omitted.

PTS therefore does not optimize for prompt length. It preserves required facts, decisions, caveats, evidence, and next actions while removing repetition, generic reassurance, and optional background first.

## 5. PTS product rules

These are PTS design decisions, not claims of official OpenAI wording:

- `Task immutable; prompt mutable.`
- Brand aliases are for discovery, not execution.
- Default output is the final prompt only; explanation is opt-in.
- Scope Fidelity prevents a simple request from becoming a heavier deliverable.
- The MVP transforms or creates prompts; it does not execute them as a PTS feature.

## 6. Cross-model rules

These are general task-preservation rules:

- Keep the user's explicit target platform and syntax.
- Do not fabricate source content, permissions, or user preferences.
- Use placeholders when questions are forbidden.
- Match visible structure to actual task complexity.

## 7. Update protocol

When the official GPT-5.6 guide changes:

1. Compare the new guidance with this snapshot.
2. Separate model-specific changes from general PTS product rules.
3. Modify one rule group at a time.
4. Re-run the same behavior corpus.
5. Record the new review date and any changed rule in project memory.
