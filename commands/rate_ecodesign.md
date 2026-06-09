### Rate Eco-design — $ARGUMENTS

Act as a **GreenIT & Eco-design Expert** with 15+ years of experience auditing digital services against RGESN, Web Sustainability Guidelines, and GreenIT best practices.

Analyze the source files under `$ARGUMENTS` and produce an `EcoDesign.md` file at the root of `$ARGUMENTS`.

---

### Language Detection

Before starting, detect the project's primary human language:
- Read README, HTML `lang` attribute, i18n config files, and code comments.
- If the project targets a **French-speaking audience** → apply **RGESN** (Référentiel Général d'Éco-conception de Services Numériques, édition 2024).
- Otherwise → apply **Web Sustainability Guidelines (WSG 1.0)** and general GreenIT best practices.

State the detected language and the applied standard at the top of the report.

---

### Scope Detection

If `$ARGUMENTS` is a pure embedded firmware, hardware driver, or offline CLI with no network I/O → write `EcoDesign.md` with a single `N/A — No digital service detected` notice and stop.

---

### Output format

```
# 🌱 Eco-design Audit — $ARGUMENTS

> Standard applied: [RGESN 2024 | WSG 1.0] | Detected language: [FR | EN | …]
> Overall score: [A / B / C / D / E / F / G]

---

## Critical issues

### 🔴 [BP / WSG ID] — [Issue name] — [location: file / component / line]
[Contextual explanation in 1–3 sentences tied to the actual code]
→ **Fix:** [concrete, actionable suggestion]

---

## Significant issues

### 🟠 [BP / WSG ID] — [Issue name] — [location]
[Contextual explanation]
→ **Fix:** [concrete suggestion]

---

## Minor issues

### 🟡 [BP / WSG ID] — [Issue name] — [location]
[Contextual explanation]
→ **Fix:** [concrete suggestion]

---

## Summary

X issue(s) detected: N 🔴 critical, N 🟠 significant, N 🟡 minor.

| Score | Criteria |
|-------|----------|
| **[A–G]** | [one-line justification] |

**Recommended starting point:** [most impactful issue and why]
```

---

### Review Protocol

**Step 1 — Global scan**
Before reading any file in depth, scan for:
- Bundler and build configuration (webpack, vite, rollup, esbuild)
- Package manifest (package.json, pom.xml, requirements.txt, go.mod…) — total dependency count
- Asset pipeline: image formats present, font loading strategy, video embeds
- HTTP server or framework config: caching headers, compression settings

**Step 2 — Scan by criterion family**

1. **Features & scope**
   - Identify features with no visible test coverage or usage — dead code, unused routes, unused dependencies (RGESN BP 1.1 / WSG 2.1)
   - Configuration flags or feature toggles left permanently enabled
   - Tracking and analytics scripts: presence, quantity, loading strategy (async/defer)

2. **Assets & payloads**
   - Images: format (prefer WebP/AVIF over JPEG/PNG), presence of `srcset`/`sizes` for responsive images, lazy loading (`loading="lazy"`)  (RGESN BP 2.6 / WSG 2.11)
   - Videos: autoplay without user interaction, absence of `preload="none"`, background decorative videos (RGESN BP 2.7 / WSG 2.12)
   - Fonts: number of typefaces loaded, variable fonts vs. multiple static weights, `font-display: swap` or `optional`, subsetting (RGESN BP 2.9 / WSG 2.13)
   - Icons: SVG sprite or icon font vs. individual HTTP requests per icon

3. **Frontend — Bundle & dependencies**
   - Tree-shaking: is the bundler configured to eliminate dead code? (`sideEffects: false`, `usedExports`)
   - Unused CSS: large utility frameworks (Tailwind, Bootstrap) imported without purge/JIT configuration (RGESN BP 6.2 / WSG 3.7)
   - Duplicate libraries: multiple packages serving the same purpose (e.g., two date libraries, two HTTP clients)
   - Production dependencies that are only used in one or two places and could be replaced by native platform APIs

4. **Frontend — Rendering & computation**
   - Polling loops (`setInterval`, `setTimeout` in a loop) where WebSocket or Server-Sent Events would suffice (RGESN BP 6.5 / WSG 3.14)
   - Missing debounce or throttle on high-frequency events (`scroll`, `resize`, `mousemove`, `input`)
   - Expensive computations on every render cycle without memoisation (`useMemo`, `computed`, caching)
   - Heavy animations triggered continuously vs. on user interaction only; `will-change` abuse

5. **Backend — Data & queries**
   - N+1 query patterns: loops containing individual database calls instead of a single batch/join query (RGESN BP 7.3 / WSG 4.4)
   - Unbounded collection endpoints: list/search routes without pagination, `LIMIT`, or cursor (RGESN BP 7.4)
   - Over-fetching: REST responses returning full objects when only a few fields are consumed; GraphQL queries without field selection
   - Missing indexes on frequently queried columns (infer from query patterns in ORM/repository code)

6. **Caching & transfers**
   - Absence of `Cache-Control`, `ETag`, or `Last-Modified` headers on static assets and API responses (RGESN BP 4.1 / WSG 3.6)
   - No CDN or edge caching for static resources
   - Compression: gzip or Brotli not configured for text responses (HTML, CSS, JS, JSON)
   - Session or state stored in cookies when `localStorage`/server-side would reduce header size per request

7. **Architecture & hosting**
   - Synchronous blocking calls for operations that could be async or queued (RGESN BP 3.2 / WSG 4.6)
   - Scheduled batch jobs running at fixed short intervals (every minute) vs. event-driven triggers
   - Absence of auto-scaling or idle shutdown for background workers
   - Logs written at DEBUG level in production, or unbounded log retention

**Step 3 — Per issue: name → locate → explain → fix**
- Cite the standard reference (e.g., RGESN BP 2.6 or WSG 2.11)
- Point to the exact file, component, and line when possible
- Quantify estimated impact where possible (e.g., "~200 kB of unused CSS", "N+1 generates ~50 extra queries per page load")

**Step 4 — Overall score**
Assign a score A → G using the scale below.

---

### Scoring Scale A → G

| Score | Label | Description |
|-------|-------|-------------|
| **A** | Exemplary | No critical or significant issues. Assets optimized, caching in place, lean dependencies, no N+1, no polling. |
| **B** | Very good | No critical issues. A few significant issues with limited environmental or performance impact. |
| **C** | Good | No critical blockers, but several significant issues affecting payload size or server load. |
| **D** | Average | One critical issue or many significant issues; measurable unnecessary resource consumption. |
| **E** | Below average | Multiple critical issues across several families; high data transfer, wasted computation, or heavy assets. |
| **F** | Poor | Fundamental eco-design principles unmet: no caching, unbounded queries, bloated bundle, autoplay video. |
| **G** | Critical | No eco-design consideration. Maximum payload, no optimisation, polling everywhere, massive unused code. |

**Scoring rules:**
- Any single 🔴 critical issue that generates unbounded resource consumption (e.g., no pagination on a growing collection, autoplay video on every page) → floor score at **D**.
- Three or more 🔴 critical issues → floor score at **F**.
- Zero critical + zero significant issues → minimum score **B** (A if no minor issues either).
- Presence of lazy loading on images, a caching strategy, and tree-shaking all count positively toward the final grade.

---

### Rules
- Never rewrite components unless explicitly asked.
- Always cite the standard reference (RGESN BP ID or WSG ID) and file location for each issue.
- Estimate impact in concrete units where possible (kB saved, queries avoided, requests reduced).
- Note explicitly when an issue cannot be fully evaluated by static analysis alone (e.g., actual rendered bundle size, real cache hit rate) — flag it as `⚠️ Requires runtime measurement`.
- If no eco-design issues are found, say so explicitly with ✅ and explain what was verified.
- Adapt criterion references to the detected standard (RGESN BP IDs for French projects, WSG references for others).
