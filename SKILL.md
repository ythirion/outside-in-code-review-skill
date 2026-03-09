---
name: outside-in-code-review
description: >
  Systematic codebase exploration from surface artifacts to implementation detail,
  producing an actionable discovery report within ~1 hour.
  Triggers: "review this codebase", "explore unknown codebase", "technical audit",
  "onboarding to new project", "legacy code review", "due diligence",
  "I don't know this codebase", "help me understand this repo",
  "can you analyze this project", "what does this codebase do".
author: Yoan Thirion <https://github.com/ythirion/>
version: 1.0.0
outputs:
  - outside-in-review/Report.md
  - outside-in-review/details/Backlog.md
  - outside-in-review/details/C4.md
  - outside-in-review/details/CodeQuality.md
time_budget: 60min
references:
  - https://goatreview.com/outside-approach-discover-unknown-codebases/
  - https://goatreview.com/augmented-outside-discovery-claude-code/
  - https://www.sammancoaching.org/reference/code_smells/index.html
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash(git log *)
  - Bash(git shortlog *)
  - Bash(git remote *)
  - Bash(git diff *)
  - Bash(basename *)
  - Bash(mkdir -p *)
---

# Outside-In Code Review

Execute a full Outside-In Code Review on the current working directory.
All output files must be written inside an `outside-in-review/` folder created at the root of the current directory.

Before starting, determine the repository name:
- Try `git remote get-url origin` and extract the repo name from the URL
- Fall back to `basename $(pwd)` if no remote is configured
- Use this name as `<REPO_NAME>` throughout all generated files

---

## Output structure

```
outside-in-review/
├── Report.md             ← full 11-section analysis + links to details
└── details/
    ├── Backlog.md        ← product backlog reverse-engineered from code
    ├── C4.md             ← C4 architecture diagrams in Mermaid syntax
    └── CodeQuality.md    ← code smell report with letter grade
```

Create both `outside-in-review/` and `outside-in-review/details/` before writing any file. Never write output files at the root of the project.

---

## Execution order

Run the four phases sequentially. Do not skip a phase because the previous one was incomplete — produce best-effort output for each.

---

## Phase 1 — Discovery Report → `outside-in-review/Report.md`

### Report title and header

Start the file with:

```
# 🔍 Outside-In Review — <REPO_NAME>

> 📅 Analyzed: <date> | ⏱️ Duration: ~1h | 🛠️ Skill by [Yoan Thirion](https://github.com/ythirion/)

---
```

### Visual conventions

Use these markers consistently throughout the report:
- 🔴 **Red flag** — critical risk requiring immediate attention
- 🟠 **Warning** — notable concern to address in the short term
- ✅ **OK** — positive signal worth acknowledging

Each section must open with a one-paragraph summary of findings, then list signals using the markers above.

### Section emoji headers

Use these exact headers for the 11 sections:

```
## 📋 1. Documentation
## 🔄 2. CI/CD Pipelines
## 📜 3. Git History
## 🔨 4. Build & Compilation
## ⚠️ 5. Compilation Warnings
## 🗂️ 6. Code Structure
## 📦 7. Dependencies
## 🕐 8. Dependency Freshness
## 📊 9. Quality Metrics
## 🔥 10. Hotspots
## 🎯 11. Summary
```

---

### 📋 1. Documentation
Read README, contributing guides, ADRs, wikis, and any available documentation.
- Is the project purpose clear?
- Can a new developer build and run the project from the README alone?
- Are setup steps, environment variables, and required services documented?

Signals to report:
- 🔴 No README or empty README
- 🔴 Setup steps fail or are incomplete
- 🟠 No architecture or decision records
- 🟠 Undocumented prerequisites
- ✅ README is complete, setup works end-to-end

---

### 🔄 2. CI/CD Pipelines
Inspect `.github/workflows/`, `Jenkinsfile`, `.gitlab-ci.yml`, or equivalent.
- What stages are defined (build, test, lint, deploy)?
- Are there quality gates (coverage thresholds, static analysis)?
- Do pipelines run on pull requests?

Signals to report:
- 🔴 No CI/CD pipeline
- 🔴 Pipeline never fails despite poor quality
- 🟠 No coverage gate or quality threshold
- 🟠 PRs not gated by CI
- ✅ Pipeline gates PRs with quality checks

---

### 📜 3. Git History
Run `git log --oneline`, `git shortlog -sn`, `git log --stat` to analyze:
- Total commits and timespan
- Number of active contributors (last 6 months)
- Most changed files and their commit counts
- Commit message quality

Signals to report:
- 🔴 Single contributor on a large codebase
- 🔴 No commits in 6+ months
- 🟠 One file changed in >20% of all commits
- 🟠 Commit messages with no context ("fix", "wip", "update")
- ✅ Healthy contributor spread and consistent commit hygiene

---

### 🔨 4. Build & Compilation
Attempt a clean build following only documented instructions.
- Does the build succeed?
- Are there undocumented steps or dependencies?
- How long does the build take?

Signals to report:
- 🔴 Build fails on clean checkout
- 🔴 Undocumented environment variables or services required
- 🟠 Build succeeds only with undocumented workarounds
- 🟠 No Docker Compose or dev container provided
- ✅ Clean build from documented steps in under 2 minutes

---

### ⚠️ 5. Compilation Warnings
Read all warnings emitted during the build — do not ignore any.
- Deprecated APIs
- Security-related warnings
- Suppressed or ignored warning counts

Signals to report:
- 🔴 Deprecated APIs from 2+ major versions ago
- 🔴 Security-related warnings (CVE, vulnerable deps)
- 🟠 Hundreds of suppressed or ignored warnings
- 🟠 Deprecated framework features in heavy use
- ✅ Clean build with zero warnings

---

### 🗂️ 6. Code Structure
Analyze folder hierarchy and naming before reading implementation files.
- Is there a discernible architectural pattern (layered, hexagonal, feature-based)?
- Are concerns separated (domain vs. infrastructure)?
- Is naming consistent across modules?

Signals to report:
- 🔴 No discernible architectural pattern
- 🔴 Business logic mixed with infrastructure concerns
- 🟠 Inconsistent naming conventions across modules
- 🟠 Flat structure with hundreds of files in one folder
- ✅ Clear architecture with well-named, well-bounded modules

---

### 📦 7. Dependencies
List all major dependencies: backend, frontend, external APIs, databases, message brokers.
- Are any dependencies abandoned (no releases in 3+ years)?
- Are there multiple libraries doing the same thing?

Signals to report:
- 🔴 Dependency on an abandoned library
- 🔴 Security-critical library with known CVE
- 🟠 Multiple libraries serving the same purpose
- 🟠 Transitive dependencies not pinned
- ✅ Dependencies are maintained and well-scoped

---

### 🕐 8. Dependency Freshness
Estimate lag using LibYear (1 libyear = 1 year of version lag across all dependencies).
- Total estimated drift
- Security-relevant packages (auth, crypto, HTTP) specifically

Signals to report:
- 🔴 > 10 libyears total drift
- 🔴 Security-critical packages outdated
- 🟠 Some deps updated, most ignored (selective maintenance)
- ✅ < 2 libyears total drift, security packages up to date

---

### 📊 9. Quality Metrics
Use available tooling (test runners, static analyzers). Report what is available; note what is missing.
- Code coverage %
- Mutation score (if configured)
- Static analysis findings (code smells count, duplication %, complexity)
- Maximum cyclomatic complexity

Signals to report:
- 🔴 Code coverage < 40%
- 🔴 Mutation score < 50%
- 🔴 Max cyclomatic complexity > 10 on core files
- 🟠 Coverage high but mutation score low
- 🟠 Code duplication > 5%
- ✅ Coverage > 80%, mutation score > 75%, low complexity

---

### 🔥 10. Hotspots
Correlate git change frequency with complexity metrics.
Hotspot = high complexity × high change rate.

List the top 5 hotspot files as a table:

| File | Complexity | Commits (12mo) | Primary author | Risk |
|------|-----------|----------------|----------------|------|
| ... | ... | ... | ... | 🔴 / 🟠 / ✅ |

Identify knowledge islands (files with a single author who owns >80% of commits).

Signals to report:
- 🔴 A single file changed in >30% of all commits
- 🔴 Hotspot file has a single author
- 🟠 Hotspot files have no tests
- 🟠 Multiple hotspots clustered in one module
- ✅ Complexity spread across many files with diverse authorship

---

### 🎯 11. Summary

Structure the summary as follows:

```
## 🎯 11. Summary

### 🔴 Top 3 risks
1. ...
2. ...
3. ...

### ❓ Top 3 questions to validate with the team
1. ...
2. ...
3. ...

### 🗺️ Recommended next actions
- **Immediate:** ...
- **Short term:** ...
- **Medium term:** ...
```

After the summary, append at the end of `Report.md`:

```
---

## 📂 Detailed Analysis

| Document | Description |
|----------|-------------|
| [📦 Product Backlog](details/Backlog.md) | Features reverse-engineered as User Stories with Gherkin acceptance criteria |
| [🏗️ Architecture (C4)](details/C4.md) | C4 model diagrams — Context, Container, Component, Code |
| [🧹 Code Quality](details/CodeQuality.md) | Code smell report with letter grade and refactoring guidance |
```

---

## Phase 2 — Product Backlog → `outside-in-review/details/Backlog.md`

Start the file with:
```
# 📦 Product Backlog — <REPO_NAME>
> ⚠️ AI-inferred from code — validate with product owners before use

← [Back to Report](../Report.md)
```

Reverse-engineer the product backlog from the codebase without relying on external documentation.
Infer features from routes, controllers, services, use cases, and test files.
Group features by business domain.

For each feature:
- **Title**
- **User Story** — "As a [role], I want [goal] so that [benefit]"
- **Acceptance Criteria** — at least one, written in Gherkin syntax (Given / When / Then)
  - **Examples / Test Cases** — at least one concrete example with test data per criterion

Mark features that appear incomplete or untested with ⚠️.

---

## Phase 3 — Architecture Diagrams → `outside-in-review/details/C4.md`

Start the file with:
```
# 🏗️ Architecture — <REPO_NAME>
> ⚠️ AI-inferred from code — validate with the team before sharing externally

← [Back to Report](../Report.md)
```

Generate C4 model diagrams using Mermaid syntax. Produce one diagram per level.

**Context** — Where does the system fit in the world?
- System as a black box; users and external systems; answers: Who uses this and why?

**Container** — What are the main building blocks?
- Major runtime units (web app, API, DB, queue); how they communicate.

**Component** — What lives inside each container?
- Modules, services, controllers and their interactions.

**Code** — What's under the hood?
- Classes, methods, or files inside one key component; structural issues (coupling, static state).

Flag all inferred user roles and external systems with a `%% ASSUMPTION` comment in the Mermaid diagram.

---

## Phase 4 — Code Quality Report → `outside-in-review/details/CodeQuality.md`

Start the file with:
```
# 🧹 Code Quality — <REPO_NAME>
> Overall grade: [A / B+ / C- / F]

← [Back to Report](../Report.md)
```

Act as a Software Crafter Coach with 20+ years of experience in Clean Code, SOLID, DRY, Object-Oriented Design, Functional Programming, and Design Patterns.

### Output format for each smell

```
### 🔴 [Smell Name] — [file / class / method]
[Contextual explanation in 1–3 sentences tied to the actual code]
→ **Refactoring:** [concrete suggestion]

### 🟠 [Smell Name] — [file / class / method]
...

### 🟡 [Smell Name] — [file / class / method]
...
```

Priority markers:
- 🔴 **Critical** — strong coupling, mutable/global data, deep nesting ≥ 4 levels
- 🟠 **Significant** — long function, large class, duplicated code, feature envy
- 🟡 **Minor** — mysterious name, comments, lazy element, paragraph of code

End the file with:
```
---
## Summary
X smell(s) detected: N 🔴 critical, N 🟠 significant, N 🟡 minor.
Recommended starting point: [most impactful smell and why]
```

### Review protocol

**Step 1 — Global read:** understand the structure and intent before commenting.

**Step 2 — Scan by family** (full definitions in `references/catalog.md`):

1. **Readability / Naming:** Mysterious Name, Comments, Paragraph of Code
2. **Size / Complexity:** Long Function, Large Class, Long Parameter List, Deep Nesting, Bumpy Road, Loops, Variable with Long Scope
3. **Coupling / Cohesion:** Feature Envy, Insider Trading, Message Chains, Middle Man, Divergent Change, Shotgun Surgery, Alternative Classes with Different Interfaces
4. **Data Structures / Modeling:** Data Class, Data Clumps, Primitive Obsession, Global Data, Mutable Data, Temporary Field, Refused Bequest, Speculative Generality, Duplicated Code, Repeated Switches, Lazy Element

**Step 3 — Per smell:** name it → locate it → explain in context → suggest refactoring.

**Step 4 — Overall grade:** assign a letter grade (A / B+ / C- / F).

### Rules
- Never rewrite the entire code unless explicitly asked.
- Always cite the location (file / class / method / line) for each smell.
- Name the smell before explaining it.
- If the codebase is clean, say so explicitly with ✅.
- Adapt refactoring suggestions to the language and ecosystem in use.
- For smell definitions and refactoring guidance, refer to `references/catalog.md`.

---

## Constraints and Guardrails

- **Time-box to ~1 hour** — stop when the time is up, not when everything is understood
- **AI outputs are hypotheses** — all architecture diagrams, user roles, and inferred product features must be validated with actual stakeholders and domain experts
- **Do not optimize prematurely** — this phase is diagnostic, not prescriptive; avoid making changes during discovery
- **Adapt the framework** — remove irrelevant steps (e.g., no UI), add project-specific steps (e.g., database schema, API contracts)
