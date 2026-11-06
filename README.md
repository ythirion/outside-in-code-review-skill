# Outside-In Code Review
[![Release skill](https://github.com/ythirion/outside-in-code-review-skill/actions/workflows/release.yml/badge.svg)](https://github.com/ythirion/outside-in-code-review-skill/actions/workflows/release.yml)
[![GitHub Release](https://img.shields.io/github/v/release/ythirion/outside-in-code-review-skill)](https://github.com/ythirion/outside-in-code-review-skill/releases)
[![Listed on ClaudePluginHub](https://www.claudepluginhub.com/badge/ythirion-outside-in-code-review)](https://www.claudepluginhub.com/plugins/ythirion-outside-in-code-review?ref=badge)

A structured skill for AI agents to explore and review unknown codebases — layer by layer, from surface artifacts down to implementation detail.

> "We spend up to 60% of our time reading code... yet treat this as a side effect rather than a skill to cultivate."

![Outside in code review logo](img/outside-in-code-review.webp)

## What is Outside-In Code Review?

Outside-In Code Review is a systematic methodology for understanding unfamiliar codebases without getting lost. It starts with what is visible without reading code (docs, git history, CI/CD), then progressively dives into code structure, quality, and behavior.

Applied with AI, it becomes a rapid discovery process: an agent can reverse-engineer a product backlog, generate architecture diagrams, and rate code quality — all from a cold start, in ~1 hour.

## Articles

This skill is based on my two articles:
- [Outside-In Discovery: A Structured Approach to Unknown Codebases](https://goatreview.com/outside-approach-discover-unknown-codebases/)
- [Augmented Outside-In Discovery with Claude Code](https://goatreview.com/augmented-outside-discovery-claude-code/)

## Repository Structure

```
outside-in-code-review/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest (claudepluginhub.com)
├── commands/                    # Slash commands installed by the plugin
│   ├── gather_product_insights.md
│   ├── explain_the_architecture.md
│   ├── detail_flow.md
│   └── rate_code_quality.md
├── skills/
│   └── outside-in-code-review/
│       ├── SKILL.md             # Skill definition: frontmatter metadata + execution protocol
│       ├── references/
│       │   └── catalog.md       # All 28 code smells — definitions and refactoring guidance
│       ├── assets/              # Copied into every report: report.css, diagrams.js, template.html,
│       │                        # fonts/, vendor/mermaid.min.js (embedded Mermaid, works offline)
│       └── scripts/
│           ├── validate_diagrams.py  # Renders every diagram in headless Chrome, checks C4 coverage
│           └── export_pdf.py         # Assembles all pages and prints outside-in-review.pdf
├── examples/
│   └── outside-in-review/       # Sample static HTML report (jurassic-code): index, architecture,
│                                # flow, backlog, code quality + self-contained assets
├── scripts/
│   └── package.sh               # Builds outside-in-code-review-<version>.zip
├── README.md                    # This file
├── METHODOLOGY.md               # The 10-step outside-in framework
├── checklist.md                 # Quick reference checklist
├── LICENSE
└── .github/
    └── workflows/
        └── release.yml          # Packages the zip and creates a draft release on version tag
```

## Installation

### Option 1 — Claude Plugin Hub (recommended)

Install directly via the [Claude Plugin Hub](https://www.claudepluginhub.com/plugins/ythirion-outside-in-code-review):

```
outside-in-code-review
```

The plugin installs the skill and all slash commands automatically. From any Claude Code session, just describe what you want:

> *"Review this codebase"* / *"Technical audit"* / *"Help me understand this repo"*

### Option 2 — AI agent skill (manual)

Download the latest zip from the [Releases](../../releases) page, unzip, and install:

```bash
mkdir -p ~/.claude/skills/outside-in-code-review
cp -r skill/* ~/.claude/skills/outside-in-code-review/
```

### Option 3 — Individual slash commands

```bash
cp commands/* ~/.claude/commands/
```

### Option 4 — From source

```bash
bash scripts/package.sh
# produces outside-in-code-review-<version>.zip

unzip outside-in-code-review-*.zip

# Install as a skill
mkdir -p ~/.claude/skills/outside-in-code-review
cp -r skill/* ~/.claude/skills/outside-in-code-review/
```

> Claude Code loads skills from `~/.claude/skills/` and commands from `~/.claude/commands/` (global) or `.claude/commands/` (project-level).

## Release a new version

1. Bump the `version` field in `skills/outside-in-code-review/SKILL.md` (and in `.claude-plugin/plugin.json`)
2. Commit and push
3. Tag the commit with the matching version:

```bash
git tag v2.0.0
git push origin v2.0.0
```

The GitHub Action (`.github/workflows/release.yml`) will:
- Package `outside-in-code-review-<version>.zip` from source (skill with its assets and scripts, commands, README)
- Validate that the tag matches the version in `SKILL.md`
- Create a **draft release** on GitHub with the zip attached

The Claude Plugin Hub auto-discovers the update within 2 hours once the tag is pushed.

Open the draft on GitHub, review the release notes, and publish when ready.

## Usage

### Running a full discovery session

Once the skill is installed, just describe what you want in any Claude Code session:

> *"Review this codebase"* / *"Technical audit"* / *"I don't know this codebase"*

The skill runs all its phases automatically and produces a static HTML site in `outside-in-review/`:

| Page | Content |
|------|---------|
| `index.html` | Dashboard with gauges, then the 13 sections (documentation → eco-design) and the summary |
| `architecture.html` | C4 diagrams: Context, Container, Component, Code |
| `flow-<slug>.html` | One business flow detailed end-to-end with a sequence diagram |
| `backlog.html` | Features reverse-engineered as user stories with Gherkin acceptance criteria |
| `code-quality.html` | Code smells with a letter grade and refactoring guidance |
| `outside-in-review.pdf` | The whole report as one PDF |

Every diagram is validated before the report is handed over, and can be copied as Mermaid or downloaded as `.mmd` / `.svg`.

By default the skill picks the most central business flow; name another one to detail it instead:

> *"Review this codebase and detail the checkout flow"*

**Requirements:** Python 3 and a Chromium-based browser (Chrome, Chromium, Edge or Brave; set `CHROME_PATH` to choose one) for diagram validation and PDF export. Nothing is downloaded at run time.

### Running individual steps

```bash
# Generate C4 architecture diagrams only
/explain_the_architecture

# Rate code quality with smell detection
/rate_code_quality

# Trace a specific feature flow
/detail_flow User Login
```

## Sample Output

The skill was run on [jurassic-code](https://github.com/ythirion/jurassic-code), a legacy-code workshop repository. The result is a static site you can browse:

[![Outside-In Review of jurassic-code: dashboard with an overall health of 36/100 and one gauge per section](img/report-preview.webp)](https://htmlpreview.github.io/?https://github.com/ythirion/outside-in-code-review-skill/blob/main/examples/outside-in-review/index.html)

**[Open the live report](https://htmlpreview.github.io/?https://github.com/ythirion/outside-in-code-review-skill/blob/main/examples/outside-in-review/index.html)** · [Download the PDF](examples/outside-in-review/outside-in-review.pdf) · [Browse the source](examples/outside-in-review/)

What you will find in it:
- **Report**: dashboard with gauges, then the 13 sections (documentation, CI/CD, git history, dependencies, hotspots, accessibility, eco-design…)
- **Architecture**: the 4 C4 levels as Mermaid diagrams, each one validated, copyable and downloadable (`.mmd`, `.svg`)
- **Flow**: "move a dinosaur" traced end-to-end, from the button click to the in-memory store
- **Backlog**: 9 features reverse-engineered as user stories with Gherkin acceptance criteria
- **Code quality**: 14 code smells and 3 real defects the tests did not catch

To view it offline, clone the repo and open `examples/outside-in-review/index.html`: no server or network needed.

## Core Principles

- **Outside before inside** — surface artifacts reveal as much as code
- **AI as cognitive reducer** — let the agent build the first mental model
- **Human validation is mandatory** — all AI outputs must be verified with stakeholders

## More explanations
I have explained the concepts behind this approach during a talk at [Mendercon 2026](https://mendercon.com/):
[![Outside-In Discovery - A structured way to understand Legacy Code](img/outside-in-discovery@mendercon.webp)](https://canva.link/4b9mxwe0oxw67js)
