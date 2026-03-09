# Outside-In Discovery Methodology

A structured, time-boxed framework for exploring unknown codebases layer by layer.

## Core Principle

Start with everything visible without diving into code. Gradually work inward as confidence builds — mimicking natural exploration. The goal is not complete comprehension but answering essential questions in ~1 hour.

**Key questions to answer:**
- How accessible is onboarding?
- Where are the friction points?
- Where does intuition break down?

---

## The Two Layers

### Outside Layer — Non-code artifacts
Explore before touching a single line of code:
- README and documentation
- Git history and contributor patterns
- CI/CD pipelines
- Project management boards

### Inside Layer — Code-focused
Enter only after forming an outside mental model:
- Folder structure and naming
- Entry points
- Business logic location
- Test suites
- Core algorithms and hotspots

---

## 10-Step Framework

### Step 1 — Documentation Review
Read README files and any available documentation.

Look for:
- Project purpose and features
- Setup and execution instructions
- Links to additional resources

**Red flag:** Missing or outdated README signals onboarding friction and reliance on tacit knowledge.

---

### Step 2 — Git History Analysis
Inspect commit patterns and contributor activity.

Look for:
- Active maintenance status
- Number and diversity of contributors
- Code ownership concentration
- Change frequency and consistency

**Red flag:** Single contributor, stale history, or erratic commit patterns signals bus factor risk.

---

### Step 3 — Build and Compile
Attempt to build and run the project from scratch following only documented instructions.

Look for:
- Whether the build succeeds
- Undocumented steps or missing prerequisites
- Quality of the developer experience

**Red flag:** A broken or undocumented build is a systemic signal, not just an inconvenience.

---

### Step 4 — Warning Analysis
Examine compiler/build output carefully.

Look for:
- Deprecated or unsupported frameworks
- Security vulnerability warnings
- Tech stack complexity signals
- Dependency management issues

**Red flag:** Warnings that have been silently accepted over time reveal accumulated technical debt.

---

### Step 5 — UI Exploration
For applications with a user interface, explore it before reading code.

Look for:
- Core features and user workflows
- Mapping between frontend actions and backend operations
- Discrepancies between what the UI suggests and what the code does

---

### Step 6 — Code Structure Assessment
Analyze the project's folder hierarchy before reading any implementation.

Look for:
- Clarity of folder names and boundaries
- Architectural patterns (layered, hexagonal, feature-based, etc.)
- Business logic location (domain vs. infrastructure)
- Naming consistency

**Red flag:** Deep nesting, mixed concerns, or unclear boundaries signal lack of architectural discipline.

---

### Step 7 — Dependency Inventory
List all major dependencies: backend libraries, frontend packages, external APIs, databases, message brokers.

Look for:
- Technology surface area (how many moving parts)
- Known problematic or abandoned libraries
- Licensing issues

---

### Step 8 — Dependency Freshness
Measure how far behind current versions the dependencies are.

Tool: **LibYear** (1 libyear = 1 year of version lag across all dependencies)

Look for:
- Total accumulated libyears
- Security-relevant outdated packages
- Patterns of neglect vs. selective updates

**Red flag:** High LibYear drift signals both technical debt and potential security exposure.

---

### Step 9 — Code Quality Metrics

Gather objective signals about code health:

| Metric                | Tool                  | What it reveals                        |
|-----------------------|-----------------------|----------------------------------------|
| Code coverage         | Language test tools   | Percentage of code exercised by tests  |
| Mutation score        | Pitest, Stryker, etc. | Whether tests actually catch real bugs |
| Static analysis       | SonarCloud, etc.      | Code smells, duplication, complexity   |
| Cyclomatic complexity | SonarCloud, etc.      | Cognitive load of individual functions |

**Red flag:** Low coverage + low mutation score = tests exist but do not protect against regressions.

---

### Step 10 — Behavioral Code Analysis (Hotspots)

**Hotspot = High Complexity × High Change Frequency**

Tool: **CodeScene** or equivalent

Look for:
- Files that are both complex and frequently modified (highest risk)
- Knowledge islands (single-author files)
- Code health trends over time

**Red flag:** A complex file changed by one person 50 times in 6 months is a critical risk concentration.

---

## Key Signals Summary

| Signal                | Implication                                       |
|-----------------------|---------------------------------------------------|
| Missing README        | Onboarding friction; tacit knowledge dependency   |
| Single contributor    | Bus factor risk; knowledge loss vulnerability     |
| Build warnings        | Tech debt; unsupported frameworks; security risks |
| High LibYear drift    | Outdated dependencies; vulnerability exposure     |
| Low mutation score    | Tests do not catch real bugs                      |
| Complex hotspot files | Risk concentration; refactoring targets           |
| Knowledge islands     | Single point of failure for expertise             |
| High code duplication | Poor modularity; maintenance burden               |

---

## Customization

This framework is a starting template. Adapt it to your context:
- Remove steps that do not apply (e.g., no UI → skip Step 5)
- Add steps relevant to your stack (e.g., database schema review, API contract inspection)
- Create a team-specific discovery checklist from the core structure
