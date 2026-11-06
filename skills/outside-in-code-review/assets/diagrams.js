// Renders every <pre class="mermaid"> on the page, one by one, so a single
// broken diagram never hides the others. Failures are shown in place.
// Requires assets/vendor/mermaid.min.js (embedded, works offline and over file://),
// loaded before this file:
//   <script src="assets/vendor/mermaid.min.js" defer></script>
//   <script src="assets/diagrams.js" defer></script>
//
// Results are written into the DOM so they survive `chrome --dump-dom`
// (used by scripts/validate_diagrams.py):
//   <figure data-render="ok|error" data-render-type="..." data-render-error="...">
//   <html data-diagrams="ok|error" data-diagrams-ok="N" data-diagrams-total="M">
// and exposed as window.__diagrams for browser checks.

// Mermaid C4 ignores themeVariables and inlines its blue palette with
// !important, so CSS cannot override it: remap the colours in the SVG text.
const C4_COLORS = {
  '#08427B': '#d9f24f', '#073B6F': '#0a0a0a',            // person
  '#1168BD': '#d9f24f', '#3C7FC0': '#0a0a0a',            // system
  '#438DD5': '#e9f79a', '#3E82C7': '#0a0a0a',            // container
  '#85BBF0': '#f4fbd0', '#78A8D8': '#0a0a0a',            // component
  '#999999': '#f4f4f0', '#8A8A8A': '#0a0a0a',            // external
  '#686868': '#f4f4f0', '#5D5D5D': '#0a0a0a',
  '#B3B3B3': '#f4f4f0', '#A6A6A6': '#0a0a0a',
  '#FFFFFF': '#0a0a0a',                                  // label text
  '#444444': '#0a0a0a',                                  // relations
};
const C4_RE = new RegExp(Object.keys(C4_COLORS).join('|'), 'gi');
const recolorC4 = (svg) => svg.replace(C4_RE, (m) => C4_COLORS[m.toUpperCase()] ?? m);

const diagramType = (source) => {
  const line = source.split('\n').map((l) => l.trim()).find((l) => l && !l.startsWith('%%') && l !== '---');
  return line ? line.split(/\s/)[0] : 'empty';
};

// ---------- Diagram tools: copy the Mermaid source, download .mmd / .svg ----------
// Lets readers reuse a diagram in another tool (mermaid.live, IDE plugin, wiki…).
// Everything is local: no data leaves the page.
const slugify = (s) => s.toLowerCase().normalize('NFKD').replace(/[^\w]+/g, '-').replace(/^-|-$/g, '') || 'diagram';

const announce = (() => {
  let region;
  return (msg) => {
    if (!region) {
      region = document.createElement('p');
      region.className = 'sr-only';
      region.setAttribute('aria-live', 'polite');
      document.body.append(region);
    }
    region.textContent = '';
    setTimeout(() => { region.textContent = msg; }, 50);
  };
})();

async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    // Fallback for contexts where the async clipboard API is unavailable.
    const ta = Object.assign(document.createElement('textarea'), { value: text });
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
    document.body.append(ta);
    ta.select();
    const ok = document.execCommand('copy');
    ta.remove();
    return ok;
  }
}

function download(filename, content, type) {
  const url = URL.createObjectURL(new Blob([content], { type }));
  const a = Object.assign(document.createElement('a'), { href: url, download: filename });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function toolButton(label, title, onClick) {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'diagram__tool';
  b.textContent = label;
  b.title = title;
  b.setAttribute('aria-label', title);
  b.addEventListener('click', onClick);
  return b;
}

function addTools(figure, el, source, name) {
  const caption = figure.querySelector?.('figcaption');
  if (!caption) return;
  const base = slugify(name);
  const tools = document.createElement('div');
  tools.className = 'diagram__tools';
  tools.setAttribute('role', 'group');
  tools.setAttribute('aria-label', `Export ${name}`);

  const copy = toolButton('Copy Mermaid', `Copy the Mermaid source of ${name}`, async () => {
    const ok = await copyText(source + '\n');
    copy.textContent = ok ? 'Copied' : 'Copy failed';
    announce(ok ? `Mermaid source of ${name} copied to the clipboard` : 'Copy failed');
    setTimeout(() => { copy.textContent = 'Copy Mermaid'; }, 2000);
  });
  tools.append(copy);
  tools.append(toolButton('.mmd', `Download the Mermaid source of ${name}`,
    () => download(`${base}.mmd`, source + '\n', 'text/plain')));

  const svg = el.querySelector('svg');
  if (svg) {
    tools.append(toolButton('.svg', `Download ${name} as SVG`, () => {
      const clone = svg.cloneNode(true);
      clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      download(`${base}.svg`, '<?xml version="1.0" encoding="UTF-8"?>\n' + clone.outerHTML, 'image/svg+xml');
    }));
  }
  caption.append(tools);
}

(async () => {
  const blocks = [...document.querySelectorAll('pre.mermaid')];
  const report = { total: blocks.length, ok: 0, errors: [] };
  const root = document.documentElement;

  const finish = () => {
    window.__diagrams = report;
    root.dataset.diagramsOk = String(report.ok);
    root.dataset.diagramsTotal = String(report.total);
    root.dataset.diagrams = report.errors.length ? 'error' : 'ok';
    console.info(`[diagrams] ${report.ok}/${report.total} rendered`);
  };

  if (typeof window.mermaid === 'undefined') {
    report.errors.push({ name: 'mermaid', message: 'assets/vendor/mermaid.min.js not loaded' });
    blocks.forEach((el) => el.closest('figure')?.setAttribute('data-render', 'error'));
    finish();
    return;
  }
  const { mermaid } = window;

  mermaid.initialize({
    startOnLoad: false,
    securityLevel: 'strict',
    theme: 'base',
    fontFamily: 'Lexend Variable, system-ui, sans-serif',
    themeVariables: {
      primaryColor: '#d9f24f',
      primaryTextColor: '#0a0a0a',
      primaryBorderColor: '#0a0a0a',
      lineColor: '#0a0a0a',
      secondaryColor: '#f4f4f0',
      tertiaryColor: '#ffffff',
      noteBkgColor: '#f4f4f0',
      noteBorderColor: '#0a0a0a',
      actorBkg: '#d9f24f',
      actorBorder: '#0a0a0a',
    },
    sequence: { showSequenceNumbers: true, wrap: true, useMaxWidth: false },
    flowchart: { htmlLabels: true, curve: 'basis' },
  });

  for (const [i, el] of blocks.entries()) {
    const source = el.textContent.trim();
    const type = diagramType(source);
    const figure = el.closest('figure') ?? el;
    const name = figure.querySelector?.('figcaption')?.firstChild?.textContent?.trim() || `diagram-${i + 1}`;
    const status = figure.querySelector?.('[data-render-status]');
    figure.setAttribute('data-render-type', type);
    try {
      await mermaid.parse(source);
      const { svg } = await mermaid.render(`mmd-${i}`, source);
      el.innerHTML = /^C4/.test(type) ? recolorC4(svg) : svg;
      el.setAttribute('data-processed', 'true');
      const node = el.querySelector('svg');
      if (!node || node.getBBox().width === 0 || node.querySelectorAll('rect,path,polygon,circle,ellipse,line,text').length < 3) {
        throw new Error('Rendered SVG is empty');
      }
      report.ok++;
      figure.setAttribute('data-render', 'ok');
      if (status) { status.textContent = 'rendered'; status.className = 'pill pill--ok'; }
    } catch (err) {
      const message = String(err?.message || err);
      report.errors.push({ name, type, message });
      figure.setAttribute('data-render', 'error');
      figure.setAttribute('data-render-error', message.slice(0, 500));
      figure.classList.add('diagram--error');
      el.setAttribute('data-processed', 'error');
      el.textContent = '';
      document.getElementById(`dmmd-${i}`)?.remove(); // mermaid's leftover error node
      const box = document.createElement('p');
      box.className = 'diagram__error';
      box.textContent = `Render failed: ${message}`;
      el.after(box);
      const src = document.createElement('details');
      src.innerHTML = '<summary>Mermaid source</summary>';
      const pre = document.createElement('pre');
      pre.textContent = source;
      src.append(pre);
      box.after(src);
      if (status) { status.textContent = 'render error'; status.className = 'pill pill--critical'; }
      console.error(`[diagrams] ${name}:`, err);
    }
    addTools(figure, el, source, name);
  }
  finish();
})();
