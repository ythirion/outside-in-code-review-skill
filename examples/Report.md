# 🔍 Outside-In Review — jurassic-code

> 📅 Analyzed: 2026-03-09 | ⏱️ Duration: ~1h | 🛠️ Skill by [Yoan Thirion](https://github.com/ythirion/)

---

## 📋 1. Documentation

The README identifies the project as a workshop designed for DevOps Days Geneva 2025, focused on "taming the dinosaurs of legacy code." It references a Miro board and cards PDF, but provides no instructions for building, running, or testing the application. A new developer arriving at this repository would have no idea how to start the API or the frontend without exploring the source tree.

- 🔴 **No setup instructions** — README contains only workshop marketing material (Miro link, cards PDF). No build, run, or test steps.
- 🟠 **No architecture or ADR documents** — the `docs/` folder contains workshop cards and Claude-generated artifacts, not living technical documentation.
- 🟠 **Undocumented prerequisites** — .NET SDK version, Node/npm versions, and required tooling (`dotnet-stryker`) are not mentioned anywhere.
- 🟠 **Scripts exist but are undocumented** — `src/run.sh` and `src/stop.sh` are present with no explanation of what they start or require.
- ✅ **Swagger UI** is enabled at the app's root, providing self-documenting API endpoints once the server is running.

---

## 🔄 2. CI/CD Pipelines

No CI/CD pipeline exists in the current working tree. A file `src/.github/workflows/ci.yml` appears in the git history (5 commits) but is no longer present — it was likely removed or lives in a different branch path. Pull requests are currently not gated by any automated quality check.

- 🔴 **No active CI/CD pipeline** — the `.github/workflows/` directory does not exist on the current branch.
- 🔴 **No quality gates** — no coverage threshold, no static analysis, no mutation testing enforced automatically.
- 🟠 **Historical evidence of CI** — the file appeared in git history, suggesting intent that was not followed through.
- 🟠 **No PR protection** — merges to `main` are unguarded.

---

## 📜 3. Git History

The repository spans approximately 4 months (2025-02-24 to 2025-06-30) with 67 commits across 2 contributors: Yoan Thirion (62 commits, ~92%) and Alexandre Trigueros (22 commits). The most-changed files are workshop materials (`IDEAS.md`, `claude/steps.md`) rather than production code. Commit message quality is good — conventional commits format (`feat:`, `fix:`, `refactor:`, `docs:`) is used consistently.

- 🟠 **Near-single contributor** — Yoan Thirion owns 92% of commits; Alexandre contributes occasionally. Knowledge concentration is high.
- ✅ **Conventional commits** — `feat:`, `fix:`, `refactor:`, `docs:` prefixes used consistently throughout history.
- ✅ **Active repository** — last commit June 2025, well within the 6-month window.
- 🟠 **Most-changed files are docs/workshop artifacts**, not production source — signals the codebase itself is treated as a static teaching fixture, not an evolving product.

---

## 🔨 4. Build & Compilation

Build succeeds from `dotnet build JurassicCode.sln` without extra steps. The 3 tests pass. However, the solution targets `netcoreapp3.1` which reached end-of-life in December 2022 — 3+ years ago. The frontend (`jurassic-ui`) uses Vite/React 19 and has no documented start command. Scripts `run.sh`/`stop.sh` exist but their content and prerequisites are undocumented.

- 🟠 **netcoreapp3.1 target** — EOL framework, not receiving security patches.
- 🟠 **No Docker Compose or dev container** — multi-process startup (API + frontend) requires manual orchestration.
- 🟠 **Frontend setup undocumented** — no `npm install` / `npm run dev` instructions anywhere visible.
- ✅ **Clean build from a single command** — `dotnet build JurassicCode.sln` succeeds in ~4 seconds.
- ✅ **3 tests pass** — no test failures on current state.

---

## ⚠️ 5. Compilation Warnings

The build emits 14 warnings. Two categories are critical: a known CVE in `Swashbuckle.AspNetCore.SwaggerUI 5.6.3` (GHSA-qrmm-w75w-3wpx, moderate severity) and `Polly 2.2.0` being incompatible with .NET Core 3.1 (restored against .NET Framework 4.x targets). The EOL framework warning is flagged on 3 projects.

- 🔴 **CVE in Swashbuckle.AspNetCore.SwaggerUI 5.6.3** — `GHSA-qrmm-w75w-3wpx` moderate vulnerability (affected endpoint exposes server details / path traversal risk in Swagger UI).
- 🔴 **netcoreapp3.1 EOL on all 3 C# projects** — no security patches since December 2022.
- 🟠 **Polly 2.2.0 incompatibility** — NuGet resolved it against .NET Framework 4.x, which means Polly's resilience policies may silently fail or behave incorrectly at runtime.
- 🟠 **14 warnings total** — none suppressed, but the signal-to-noise ratio is high enough that engineers risk ignoring real problems.

---

## 🗂️ 6. Code Structure

The solution contains 4 projects: `JurassicCode` (domain/service), `JurassicCode.API` (ASP.NET Core), `JurassicCode.Tests` (xUnit), and `JurrassicCode.Console` (VB.NET — note the typo). The domain library has no sub-folders; all files sit flat at the root. The architectural separation is muddled: the service (`ParkService`) is a `partial class` split across `Class1.cs` and `Init.cs`, directly couples to a static `DataAccessLayer`, and `Database.cs` uses reflection to access its own private fields.

- 🔴 **No discernible architecture** — no layering, no hexagonal ports/adapters, no feature modules. Everything is flat.
- 🔴 **Business logic tightly coupled to static data access** — `ParkService` calls `DataAccessLayer._db` directly throughout.
- 🟠 **`Class1.cs`** — the central service file has the default VS placeholder name, a significant naming signal.
- 🟠 **`partial class ParkService`** — service split across two files with no obvious reason, increasing cognitive load.
- 🟠 **VB.NET console app** — a second runtime client (with a typo in the project name: `JurrassicCode`) duplicates all initialization data from `Init.cs` verbatim.
- 🟠 **Inconsistent naming conventions between domain and persistence layer** — `IsCarnivorous` ↔ `IsVegan`, `Name` ↔ `CodeName`, `IsOpen` ↔ `AccessStatus`.

---

## 📦 7. Dependencies

**Backend (C#):**
| Package | Version | Status |
|---------|---------|--------|
| Swashbuckle.AspNetCore | 5.6.3 | 🔴 CVE GHSA-qrmm-w75w-3wpx |
| Swashbuckle.AspNetCore.SwaggerUI | 5.6.3 | 🔴 Same CVE |
| Confluent.Kafka | 0.11.1 | 🔴 Released ~2018, abandoned major version |
| Polly | 2.2.0 | 🔴 Incompatible with .NET Core 3.1; Polly is now v8+ |

**Frontend (TypeScript/React):**
| Package | Version | Status |
|---------|---------|--------|
| React | ^19.0.0 | ✅ Latest |
| Vite | ^6.2.0 | ✅ Latest |
| axios | ^1.8.2 | ✅ Up-to-date |
| styled-components | ^6.1.15 | ✅ Maintained |
| react-router-dom | ^7.3.0 | ✅ Latest |

- 🔴 **`Confluent.Kafka 0.11.1`** — released circa 2018 (major version 0.x), no Kafka usage found in the code. Dead import.
- 🔴 **`Polly 2.2.0`** — current stable is 8.x; version 2.x dates from 2016. Incompatible with the target runtime.
- 🟠 **Both Kafka and Polly are unused** — present as dependencies but nowhere imported or called in source files.
- ✅ **Frontend dependencies are modern and well-maintained**.

---

## 🕐 8. Dependency Freshness

Backend packages are severely outdated. `Confluent.Kafka 0.11.1` is ~8 years behind current (2.x). `Polly 2.2.0` is ~6 years behind (8.x). `Swashbuckle 5.6.3` is ~3 years behind (6.x). `netcoreapp3.1` itself is EOL since late 2022. Estimated libyear drift for the backend alone is **>15 libyears**.

- 🔴 **>15 libyears drift** — heavily concentrated in unused backend dependencies and EOL framework.
- 🔴 **Security-critical components outdated** — HTTP serving middleware (Swashbuckle) carries a known CVE.
- 🟠 **Selective maintenance** — frontend is kept modern while backend rots.
- ✅ **Frontend is < 0.5 libyears drift** — React 19, Vite 6, all recent releases.

---

## 📊 9. Quality Metrics

3 tests exist, all passing. Coverage tooling is not configured. Stryker (mutation testing) is configured via `stryker-config.json` but no mutation score baseline is recorded. The single test class (`ParkServiceTests`) exercises the happy path and a few error cases, but entire methods (`GetAllZones`, `CanSpeciesCoexist` edge cases) are untested. Cyclomatic complexity is moderate — `ParkService.CanSpeciesCoexist` uses a branching score system with hardcoded species names and no extensibility.

- 🔴 **Coverage estimated < 40%** — only one test class with 3 test methods covering 7 public methods. `GetAllZones` has zero test coverage.
- 🔴 **No mutation score baseline** — Stryker is configured but never run in CI, so quality regression is undetected.
- 🟠 **`CanSpeciesCoexist` hardcodes 3 species** — logic will silently return wrong results for any other pair.
- 🟠 **Tests share global static state** — `DataAccessLayer._db` is a static singleton; tests call `DataAccessLayer.Init(new Database())` to reset, which is fragile.
- ✅ **Stryker is configured** — tooling intent is present, just not enforced.

---

## 🔥 10. Hotspots

Hotspot analysis correlates file change frequency with structural complexity:

| File | Complexity | Commits (all time) | Primary author | Risk |
|------|-----------|-------------------|----------------|------|
| `src/JurassicCode/Class1.cs` (ParkService) | High — 7 methods, loops, global state | 4 | Yoan Thirion | 🔴 |
| `src/JurassicCode.API/Controllers/ParkController.cs` | Medium — 7 endpoints, copy-paste catch blocks | 5 | Yoan Thirion | 🟠 |
| `src/JurassicCode.Tests/Tests.cs` | Medium — 3 tests, shared static state | 5 | Yoan Thirion | 🟠 |
| `src/JurassicCode/Db2/DataAccessLayer.cs` | Medium — static class, 5 methods | 2 | Yoan Thirion | 🟠 |
| `src/JurassicCode/Init.cs` | Low — data setup only, but 277 lines | 2 | Yoan Thirion | 🟡 |

**Knowledge island:** Yoan Thirion owns 100% of commits on all production source files. No knowledge sharing exists on the codebase itself.

- 🔴 **`Class1.cs` (ParkService)** — highest complexity, direct `DataAccessLayer._db` access throughout, manual for-loops, single author.
- 🔴 **Single author on all production code** — 100% of production file commits belong to one person.
- 🟠 **Controller has 7 copy-paste catch blocks** — divergent change risk; any error handling change requires touching all 7 endpoints.
- 🟠 **No tests cover `DataAccessLayer` directly** — it is the most dangerous class (global mutable state) and has zero direct test coverage.

---

## 🎯 11. Summary

### 🔴 Top 3 risks
1. **EOL framework + known CVE in Swashbuckle** — `netcoreapp3.1` no longer receives security patches, and the Swagger UI middleware carries a known moderate CVE (`GHSA-qrmm-w75w-3wpx`). This is production-risk if the API is exposed.
2. **Global mutable static state** — `DataAccessLayer._db` is a public static field, making the application fundamentally non-thread-safe, untestable in isolation, and fragile. Any concurrent request can corrupt park state.
3. **Near-zero test coverage with no CI enforcement** — 3 tests cover 7 public methods with no coverage measurement, no mutation testing in CI, and no pull request gates. Regressions will go undetected.

### ❓ Top 3 questions to validate with the team
1. **Is `Confluent.Kafka` actually used?** It is listed as a dependency but no import or usage appears anywhere in the source. Is this a leftover from a planned feature, or was it added intentionally as a "code smell" for the workshop?
2. **What is the intended test isolation strategy?** Tests currently reset the singleton with `DataAccessLayer.Init(new Database())`. Is this deliberate "legacy code smell" for the workshop, or does the team intend to introduce proper DI?
3. **Is the CI/CD pipeline intentionally absent?** The `.github/workflows/ci.yml` file appeared in git history but is gone. Is pipeline removal itself part of the workshop exercise?

### 🗺️ Recommended next actions
- **Immediate:** Upgrade `Swashbuckle.AspNetCore` to 6.x+ to resolve the active CVE. Upgrade `netcoreapp3.1` to at least `.net8` (LTS).
- **Short term:** Replace `static DataAccessLayer` with an injected interface. Register `IParkService` and `IRepository` via ASP.NET Core DI. This unblocks proper unit testing.
- **Medium term:** Add CI pipeline (GitHub Actions) with build + test + coverage gate (≥80%) + Stryker mutation score gate (≥60%). Rename `Class1.cs` to `ParkService.cs` and merge the `partial class` split. Remove unused `Confluent.Kafka` and `Polly` dependencies.

---

## 📂 Detailed Analysis

| Document | Description |
|----------|-------------|
| [📦 Product Backlog](details/Backlog.md) | Features reverse-engineered as User Stories with Gherkin acceptance criteria |
| [🏗️ Architecture (C4)](details/C4.md) | C4 model diagrams — Context, Container, Component, Code |
| [🧹 Code Quality](details/CodeQuality.md) | Code smell report with letter grade and refactoring guidance |
