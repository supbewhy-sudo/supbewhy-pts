# PTS Rulebook

## Contents

1. Task contract
2. Remove, preserve, or translate
3. Missing information
4. Scope Fidelity
5. Structure and output
6. Agentic prompt boundaries
7. Target platform
8. Final self-check

## 1. Task contract

Treat these as immutable unless the user asks to change them:

- Task and desired outcome
- Audience and use context
- Target model, tool, platform, or syntax
- Source materials and their priority
- Must-have and prohibited content
- Language, tone, format, length, and delivery constraints
- Identity, composition, position, scale, color, and accessory constraints in image tasks
- Authorization and approval boundaries in agentic tasks
- Implied task depth and delivery complexity

A complete rewrite is allowed. A task or scope change is not.

## 2. Remove, preserve, or translate

### Remove when non-functional

- Generic personas such as “world-class expert” or “20 years of experience”.
- Empty intensity such as “deeply”, “professionally”, or “comprehensively” without an observable requirement.
- Performative rituals such as “simulate five experts” or “reflect three times” when no visible output depends on them.
- Duplicated instructions, repeated prohibitions, and examples that only restate a rule.
- Tool lists unrelated to the task.
- Broad brevity commands when concrete length and required content already control the output.

Do not remove content merely because it is long. Remove it only when it is non-functional.

### Preserve when outcome-critical

- Specific professional frameworks, standards, or evaluation perspectives.
- Facts, source priority, evidence requirements, uncertainty rules, and non-invention boundaries.
- Tone and style choices that define the product rather than merely praising quality.
- Target-platform syntax and parameters.
- Separate image constraints that prevent identity, layout, or accessory drift.
- Explicit counts, schemas, or length limits requested by the user.

### Translate private process requests into visible results

- “深入思考” → require a conclusion, key evidence, risks, and material uncertainty when those outputs fit the task.
- “多位专家讨论” → require distinct supporting and opposing views only when the user needs a balanced comparison.
- “反复检查” → require a concise acceptance check tied to explicit success criteria.

Never add these visible outputs mechanically. They still have to pass Scope Fidelity.

## 3. Missing information

Add only information required to execute or verify the actual task:

- A concrete deliverable when the requested result is otherwise unknowable.
- Inputs and source priority when multiple materials exist.
- Evidence, citations, assumptions, or uncertainty handling when claims need support.
- Output language, format, hierarchy, length, or schema when the use case requires control.
- Completion criteria that distinguish success from a plausible-looking answer.
- Tool permissions and approval boundaries only for an agentic prompt that can take actions.

Decision policy:

- **Low-risk and unique interpretation:** infer conservatively; encode the assumption only when the user needs to see it.
- **Outcome-changing ambiguity:** ask one consolidated question.
- **Questions forbidden:** use explicit `{{placeholder}}` fields.
- **Authorization or high-risk fact:** never infer.

Do not ask for information the user already provided. Do not ask merely to make the prompt more detailed.

## 4. Scope Fidelity

Before adding anything, record the scope envelope implied by the source:

- Decision to be made or job to be done
- Expected depth
- Expected answer length
- Number of deliverables or sections
- Professional or technical level
- Intended use and audience

Every added requirement must pass all four gates:

1. **Real gap:** Does it resolve an actual ambiguity or missing requirement?
2. **Material value:** Does it clearly improve usability, correctness, or verification?
3. **Task fit:** Does it apply to this task rather than a generic template?
4. **Necessary:** Would removing it materially reduce result quality?

If any answer is no, omit the addition.

Common over-compilation failures:

- Turning a quick review into a complete audit, consulting project, or due-diligence framework.
- Inventing fixed counts, word limits, confidence scores, matrices, or risk fields.
- Adding domain metrics that do not apply to the user's business or task.
- Requiring citations, tables, JSON, or step-by-step plans without a use-case reason.
- Expanding one deliverable into several independent deliverables.

When the user's source is already clear, improvement may consist only of removing noise and lightly reorganizing it.

## 5. Structure and output

Use these functional slots internally, but render only what matters:

- Goal / deliverable
- Context / inputs
- Requirements / constraints
- Permissions / boundaries
- Output format
- Success criteria

A simple translation prompt may remain one sentence. A complex agent task may use headings. Empty headings are forbidden.

Match the user's language unless the target platform, audience, or requested output language requires another language.

## 6. Agentic prompt boundaries

PTS does not execute the compiled task. When compiling a prompt that will control an agent, make its permissions proportional to that task:

- Read, review, explain, diagnose, or plan: inspect and report; do not mutate unless requested.
- Change, build, or fix: allow requested in-scope local work and relevant non-destructive validation.
- Require confirmation before external writes, destructive actions, purchases, or material scope expansion.

Keep this boundary in one place. Do not repeat it throughout the prompt.

## 7. Target platform

Preserve the user's explicit target:

- A Midjourney prompt keeps required Midjourney syntax and parameters.
- A Claude prompt remains for Claude unless migration is requested.
- A GPT-5.6 prompt may use GPT-5.6-specific output, ambiguity, and approval controls.

When migration is requested, preserve the underlying task while replacing only platform-specific syntax and controls.

## 8. Final self-check

- Does the final prompt ask for the same result?
- Is the scope envelope unchanged?
- Is every outcome-critical detail present?
- Did any new objective, audience, tool, metric, section, or deliverable appear without passing all four gates?
- Is any line repeated, vague, contradictory, or performative?
- Are platform syntax and permissions correct?
- Is the output mode correct?
- Can the user copy and use the result immediately?
