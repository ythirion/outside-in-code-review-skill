## Outside-In Discovery

Use this checklist as a structured, time-boxed way (≈1 hour) to explore any new codebase.

### Read the `README` / Related Documentation
- [ ] Does a `README.md` exist?
- [ ] Is there documentation on how to run / understand the system?
- [ ] Are architectural decisions or domain concepts explained?
- [ ] If missing: what questions remain unanswered?

### Inspect CI/CD Pipelines
- [ ] Is there a `.github/workflows/`, `.gitlab-ci.yml`, or similar CI config?
- [ ] Are builds/tests automatically triggered on push or PR?
- [ ] Are releases/deployments automated?
- [ ] Are quality gates configured (tests, linting, security checks)?
- [ ] What is the feedback loop duration?

> CI/CD tells you how code gets validated, tested, and delivered — and how confident the team is in their process.

### Inspect the Git History
- [ ] Run `git log --oneline` and scroll through:
    - [ ] Are commit messages meaningful?
    - [ ] Is the activity recent? Regular?
- [ ] Look for signs of churn or abandoned features

### Compile the Code
- [ ] Can the system be built and executed?
- [ ] Are there build scripts or automated setup steps?
- [ ] Any blockers or friction during installation?
- [ ] First impression: does the system "welcome" a new dev?

#### Analyze Compilation Warnings
- [ ] Any deprecated technologies or unsupported frameworks?
- [ ] Security vulnerabilities flagged during install or build?
- [ ] Language diversity or stack complexity (e.g. C#, VB.NET, JS)?
- [ ] Are these signals of tech debt or lack of maintenance?

### Explore the UI
- [ ] Run the app and identify its core features

### Analyze the Code Structure
- [ ] Map features to corresponding components or APIs
- [ ] Analyze folder structure: clear modularity or spaghetti?
- [ ] Look for vague naming (`Manager`, `Helper`, etc.)
- [ ] Can you identify where business logic resides?

### List and Review Dependencies
- [ ] List back-end dependencies (`dotnet list ...`)
- [ ] List front-end dependencies (`npm list --depth=0`)
- [ ] Spot integration points: APIs, DBs, brokers (Kafka, Redis…)
- [ ] Are libraries up-to-date? Secure? Maintained?

### Dependencies freshness
- [ ] Install and run `libyear`
- [ ] Check drift in dependencies:
- [ ] Prioritize critical updates if needed

### Gather Metrics (if applicable)
> ⚠️ Every project is different — some may already have tools like SonarCloud or Stryker configured.
Others may require you to install tools locally. Adapt accordingly.

- [ ] Look for existing dashboards or CI outputs (code quality gates, badges, etc.)
- [ ] Review test coverage (if reported)
    - [ ] How much is covered?
    - [ ] Are the tests meaningful?
- [ ] Check mutation testing results (if available)
- [ ] Run or review static analysis reports (SonarCloud, ESLint, etc.)
    - [ ] Code smells, bugs, complexity, duplication?

### Identify Hotspots (Behavioral Code Analysis)
Use CodeScene (or alternative) to:
- [ ] Identify complex + frequently changed files
- [ ] Spot refactoring candidates
- [ ] Visualize knowledge islands (single-author files)

### Reflect
- [ ] What would onboarding feel like on this project?
- [ ] What’s your confidence in making a change today?
- [ ] What would you improve first: documentation, tests, structure?