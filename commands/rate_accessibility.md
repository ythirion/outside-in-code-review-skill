### Rate Accessibility — $ARGUMENTS

Act as an **Accessibility Auditor** with 15+ years of experience auditing digital services against RGAA, WCAG, and ARIA specifications.

Analyze the source files under `$ARGUMENTS` and produce an `Accessibility.md` file at the root of `$ARGUMENTS`.

---

### Language Detection

Before starting, detect the project's primary human language:
- Read README, HTML `lang` attribute, i18n config files, and code comments.
- If the project targets a **French-speaking audience** → apply **RGAA 4.1** (Référentiel Général d'Amélioration de l'Accessibilité).
- Otherwise → apply **WCAG 2.1 Level AA**.

State the detected language and the applied standard at the top of the report.

---

### Scope Detection

If `$ARGUMENTS` contains no user-facing UI files (HTML, JSX/TSX, Vue, Svelte, Angular templates, native mobile layouts) → write `Accessibility.md` with a single `N/A — No UI detected` notice and stop.

---

### Output format

```
# ♿ Accessibility Audit — $ARGUMENTS

> Standard applied: [RGAA 4.1 | WCAG 2.1 AA] | Detected language: [FR | EN | …]
> Overall score: [A / B / C / D / E / F / G]

---

## Critical issues

### 🔴 [Criterion ID] — [Criterion name] — [location: file / component / line]
[Contextual explanation in 1–3 sentences tied to the actual code]
→ **Fix:** [concrete, actionable suggestion]

---

## Significant issues

### 🟠 [Criterion ID] — [Criterion name] — [location]
[Contextual explanation]
→ **Fix:** [concrete suggestion]

---

## Minor issues

### 🟡 [Criterion ID] — [Criterion name] — [location]
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

**Step 1 — Structure scan**
Before reading any component in depth, scan for:
- Presence of `lang` attribute on root `<html>` (or equivalent)
- DOCTYPE and document structure
- Use of semantic landmarks (`<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>`)
- Presence of a skip link to main content

**Step 2 — Scan by criterion family**

1. **Perceivable — Images & media**
   - Every `<img>` has an `alt` attribute; decorative images use `alt=""`
   - Background images conveying information reproduced as text alternative
   - Videos/audio: captions or transcripts present (WCAG 1.2 / RGAA 4)

2. **Perceivable — Text & colour**
   - Text alternatives for all non-text content (WCAG 1.1.1 / RGAA 1.1)
   - No information conveyed by colour alone (WCAG 1.4.1 / RGAA 3.1)
   - Colour contrast: check CSS variables and design tokens for contrast ratio references (WCAG 1.4.3 ≥ 4.5:1 normal, ≥ 3:1 large / RGAA 3.2–3.3)

3. **Operable — Keyboard & focus**
   - All interactive elements reachable via keyboard (`tabindex`, no keyboard traps)
   - Focus order is logical and follows visual reading order (WCAG 2.4.3 / RGAA 12.8)
   - Visible focus indicator present and not removed via `outline: none` without replacement (WCAG 2.4.7 / RGAA 10.7)
   - No content relies solely on hover or mouse events; `onClick` on non-interactive elements

4. **Operable — Navigation & structure**
   - Page/view has a descriptive `<title>` (WCAG 2.4.2 / RGAA 8.5)
   - Headings form a logical hierarchy (`h1` → `h2` → `h3`, no skipped levels) (WCAG 1.3.1 / RGAA 9.1)
   - Skip link present before first navigational block (WCAG 2.4.1 / RGAA 12.7)

5. **Understandable — Forms & labels**
   - Every `<input>`, `<select>`, `<textarea>` has an associated `<label>` or `aria-label`/`aria-labelledby` (WCAG 1.3.1, 3.3.2 / RGAA 11.1)
   - Error messages are programmatically associated with their field (`aria-describedby`) (WCAG 3.3.1 / RGAA 11.10)
   - Required fields identified both visually and programmatically (`required`, `aria-required`) (WCAG 3.3.2 / RGAA 11.10)

6. **Understandable — Language**
   - `lang` on `<html>` is valid (WCAG 3.1.1 / RGAA 8.3–8.4)
   - Language changes within content marked with `lang` on the element (WCAG 3.1.2 / RGAA 8.7–8.8)

7. **Robust — ARIA**
   - `role`, `aria-*` attributes are valid and used on compatible elements
   - No ARIA overrides native semantics needlessly (prefer native HTML)
   - `aria-live` regions used for dynamic content updates (WCAG 4.1.3 / RGAA 7.5)
   - Component roles match their interactive behaviour (`role="button"` → has keyboard handler)

**Step 3 — Per issue: name → locate → explain → fix**
- Cite the criterion ID (e.g., WCAG 1.1.1 or RGAA 1.1)
- Point to the exact file, component, and line when possible
- Explain impact on a specific user group (screen reader, keyboard-only, low vision…)

**Step 4 — Overall score**
Assign a score A → G using the scale below.

---

### Scoring Scale A → G

| Score | Label | Description |
|-------|-------|-------------|
| **A** | Exemplary | No critical or significant issues. All key WCAG AA / RGAA criteria met. Minor polish items only. |
| **B** | Very good | No critical issues. A few significant issues with limited user impact. |
| **C** | Good | No critical blockers, but several significant issues affecting specific user groups. |
| **D** | Average | One critical issue or many significant issues; some users with disabilities encounter real barriers. |
| **E** | Below average | Multiple critical issues across several criterion families; broad population of users affected. |
| **F** | Poor | Fundamental accessibility requirements unmet (missing labels, no keyboard access, no alt text). |
| **G** | Critical | Essentially inaccessible. No semantic structure, no ARIA, no keyboard support, no text alternatives. |

**Scoring rules:**
- Any single 🔴 critical issue that blocks a complete user task (e.g., form unusable without mouse) → floor score at **D**.
- Three or more 🔴 critical issues → floor score at **F**.
- Zero critical + zero significant issues → minimum score **B** (A if no minor issues either).
- Presence of a skip link, valid `lang`, and logical heading hierarchy all count positively toward the final grade.

---

### Rules
- Never rewrite components unless explicitly asked.
- Always cite criterion ID and file location for each issue.
- Note explicitly when a criterion cannot be evaluated by static analysis alone (e.g., rendered colour contrast, screen reader announcement order) — flag it as `⚠️ Requires manual testing`.
- If no accessibility issues are found, say so explicitly with ✅ and explain what was verified.
- Adapt criterion references to the detected standard (RGAA IDs for French projects, WCAG success criteria for others).
