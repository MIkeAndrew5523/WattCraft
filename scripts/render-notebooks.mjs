#!/usr/bin/env node
// scripts/render-notebooks.mjs
// Converts .ipynb files from public/notebooks/ to standalone HTML in public/notebooks/rendered/

import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'fs';
import { join, basename } from 'path';
import { Marked } from 'marked';

const SOURCE_DIR = 'public/notebooks';
const OUTPUT_DIR = 'public/notebooks/rendered';
const marked = new Marked();

mkdirSync(OUTPUT_DIR, { recursive: true });

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function renderOutput(output) {
  const parts = [];

  if (output.output_type === 'stream') {
    const text = Array.isArray(output.text) ? output.text.join('') : output.text;
    parts.push(`<pre class="nb-stream nb-stream-${output.name || 'stdout'}">${escapeHtml(text)}</pre>`);
  }

  if (output.output_type === 'execute_result' || output.output_type === 'display_data') {
    const data = output.data || {};
    if (data['text/html']) {
      const html = Array.isArray(data['text/html']) ? data['text/html'].join('') : data['text/html'];
      parts.push(`<div class="nb-html-output">${html}</div>`);
    } else if (data['image/png']) {
      parts.push(`<div class="nb-image-output"><img src="data:image/png;base64,${data['image/png']}" /></div>`);
    } else if (data['image/svg+xml']) {
      const svg = Array.isArray(data['image/svg+xml']) ? data['image/svg+xml'].join('') : data['image/svg+xml'];
      parts.push(`<div class="nb-image-output">${svg}</div>`);
    } else if (data['text/plain']) {
      const text = Array.isArray(data['text/plain']) ? data['text/plain'].join('') : data['text/plain'];
      parts.push(`<pre class="nb-text-output">${escapeHtml(text)}</pre>`);
    }
  }

  if (output.output_type === 'error') {
    const tb = (output.traceback || []).join('\n')
      .replace(/\x1b\[[0-9;]*m/g, ''); // strip ANSI colors
    parts.push(`<pre class="nb-error">${escapeHtml(tb)}</pre>`);
  }

  return parts.join('\n');
}

function renderCell(cell) {
  const source = Array.isArray(cell.source) ? cell.source.join('') : cell.source;
  if (!source.trim()) return '';

  if (cell.cell_type === 'markdown') {
    return `<div class="nb-markdown-cell">${marked.parse(source)}</div>`;
  }

  if (cell.cell_type === 'code') {
    const outputs = (cell.outputs || []).map(renderOutput).filter(Boolean).join('\n');
    // Hide code input — only show outputs
    if (!outputs) return '';
    return `<div class="nb-code-cell"><div class="nb-output">${outputs}</div></div>`;
  }

  return '';
}

function renderNotebook(ipynbPath) {
  const raw = readFileSync(ipynbPath, 'utf-8');
  const nb = JSON.parse(raw);
  const cells = (nb.cells || []).map(renderCell).join('\n');

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  :root {
    --bg: #ffffff; --fg: #1e293b; --code-bg: #f8fafc; --border: #e2e8f0;
    --prompt-color: #64748b; --output-bg: #fafafa; --error-bg: #fef2f2;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #0f172a; --fg: #e2e8f0; --code-bg: #1e293b; --border: #334155;
      --prompt-color: #94a3b8; --output-bg: #1e293b; --error-bg: #450a0a;
    }
  }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg); color: var(--fg);
    max-width: 960px; margin: 0 auto; padding: 1rem;
    line-height: 1.6;
  }
  .nb-markdown-cell { margin: 1.5rem 0; }
  .nb-markdown-cell h1 { font-size: 1.8rem; margin: 1.5rem 0 0.5rem; }
  .nb-markdown-cell h2 { font-size: 1.4rem; margin: 1.2rem 0 0.4rem; }
  .nb-markdown-cell h3 { font-size: 1.1rem; margin: 1rem 0 0.3rem; }
  .nb-markdown-cell p { margin: 0.5rem 0; }
  .nb-markdown-cell ul, .nb-markdown-cell ol { padding-left: 1.5rem; }
  .nb-markdown-cell strong { font-weight: 700; }
  .nb-code-cell {
    margin: 1rem 0; border: 1px solid var(--border); border-radius: 6px;
    overflow: hidden;
  }
  .nb-output { padding: 0.75rem 1rem; background: var(--output-bg); }
  .nb-output pre { margin: 0; font-size: 0.8rem; white-space: pre-wrap; word-break: break-word; overflow-x: auto; }
  .nb-output img { max-width: 100%; height: auto; }
  .nb-html-output { overflow-x: auto; }
  .nb-html-output table { border-collapse: collapse; font-size: 0.8rem; margin: 0.5rem 0; }
  .nb-html-output th, .nb-html-output td { border: 1px solid var(--border); padding: 4px 8px; text-align: left; }
  .nb-html-output th { background: var(--code-bg); font-weight: 600; }
  .nb-error { background: var(--error-bg); color: #dc2626; margin: 0; }
  .nb-image-output { text-align: center; padding: 0.5rem 0; }
</style>
</head>
<body>
${cells}
</body>
</html>`;
}

// Process all .ipynb files
const files = readdirSync(SOURCE_DIR).filter(f => f.endsWith('.ipynb'));
for (const file of files) {
  const inputPath = join(SOURCE_DIR, file);
  const outputName = file.replace('.ipynb', '.html');
  const outputPath = join(OUTPUT_DIR, outputName);
  writeFileSync(outputPath, renderNotebook(inputPath), 'utf-8');
  console.log(`Rendered: ${file} -> ${outputName}`);
}
console.log(`\nDone. ${files.length} notebooks rendered to ${OUTPUT_DIR}/`);
