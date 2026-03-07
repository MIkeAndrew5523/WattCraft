# SKILLS.md — Reusable Patterns & Component Library
## Project: Industrial Energy Manager Portfolio & Blog

> This is a living document. When the agent builds something reusable, it should be documented here so future agent sessions can reference it without reinventing the wheel.

---

## 1. Design System

### Color Palette
```css
/* Tailwind custom config additions */
colors: {
  brand: {
    navy:    '#0f172a',   /* Primary background / headers */
    slate:   '#334155',   /* Secondary text, borders */
    amber:   '#f59e0b',   /* Accent — energy, highlights, CTAs */
    electric:'#3b82f6',   /* Links, interactive elements */
    offwhite:'#f8fafc',   /* Light mode background */
  }
}
```

### Typography
```css
/* Base font stack */
font-family: 'Inter', system-ui, sans-serif;     /* Body */
font-family: 'JetBrains Mono', monospace;        /* Code blocks */

/* Type scale (Tailwind classes) */
h1: text-4xl font-bold tracking-tight
h2: text-2xl font-semibold
h3: text-xl font-semibold
body: text-base leading-relaxed
code: text-sm font-mono
```

### Spacing System
- Use Tailwind's default spacing scale
- Section padding: `py-16 md:py-24`
- Container max-width: `max-w-5xl mx-auto px-4 sm:px-6`
- Card gap: `gap-6 md:gap-8`

---

## 2. Layout Patterns

### Base Page Layout
```astro
---
// src/layouts/BaseLayout.astro
import Nav from '../components/Nav.astro';
import Footer from '../components/Footer.astro';

interface Props {
  title: string;
  description?: string;
  ogImage?: string;
}

const { title, description, ogImage } = Astro.props;
---
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width" />
    <title>{title} | Mike Leishman — Energy Analytics</title>
    <meta name="description" content={description} />
    <!-- OG tags here -->
  </head>
  <body class="bg-brand-offwhite dark:bg-brand-navy text-brand-slate dark:text-slate-200">
    <Nav />
    <main>
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

### Content Page Layout (Blog posts, Notebooks)
```astro
---
// src/layouts/ContentLayout.astro
// Adds: breadcrumb, reading time, tags, back button
---
```

---

## 3. Component Patterns

### Notebook Card (Portfolio Grid Item)
**Purpose:** Displays a notebook project in the portfolio grid
**Props:** `title`, `summary`, `tags`, `techStack`, `date`, `slug`

```astro
---
// src/components/NotebookCard.astro
interface Props {
  title: string;
  summary: string;
  tags: string[];
  techStack: string[];
  date: string;
  slug: string;
}
---
<article class="rounded-xl border border-slate-200 dark:border-slate-700 p-6 hover:shadow-lg transition-shadow">
  <div class="flex gap-2 flex-wrap mb-3">
    {tags.map(tag => <TagBadge tag={tag} />)}
  </div>
  <h3 class="text-xl font-semibold mb-2">
    <a href={`/portfolio/${slug}`} class="hover:text-brand-electric">{title}</a>
  </h3>
  <p class="text-sm text-slate-500 mb-4">{summary}</p>
  <div class="flex gap-2 flex-wrap">
    {techStack.map(tech => <span class="text-xs font-mono bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded">{tech}</span>)}
  </div>
</article>
```

### Blog Post Card
**Purpose:** Displays a blog post in the blog index list
**Props:** `title`, `summary`, `date`, `tags`, `readingTime`, `slug`

```astro
---
// src/components/BlogCard.astro
---
<article class="border-b border-slate-200 dark:border-slate-700 py-8">
  <time class="text-xs text-slate-400 uppercase tracking-wide">{date}</time>
  <h2 class="text-2xl font-semibold mt-1 mb-2">
    <a href={`/blog/${slug}`} class="hover:text-brand-electric">{title}</a>
  </h2>
  <p class="text-slate-500 mb-3">{summary}</p>
  <div class="flex gap-3 items-center">
    {tags.map(tag => <TagBadge tag={tag} />)}
    <span class="text-xs text-slate-400">{readingTime} min read</span>
  </div>
</article>
```

### Tag Badge
**Purpose:** Colored badge for content categorization
**Tag types:** `case-study` (blue), `opinion` (amber), `tutorial` (green), `energy-audit` etc.

```astro
---
// src/components/TagBadge.astro
const colorMap = {
  'case-study':  'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  'opinion':     'bg-amber-100 text-amber-800 dark:bg-amber-900 dark:text-amber-200',
  'tutorial':    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  'default':     'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300',
}
const { tag } = Astro.props;
const color = colorMap[tag] ?? colorMap['default'];
---
<span class={`text-xs font-medium px-2.5 py-0.5 rounded-full ${color}`}>
  {tag}
</span>
```

### Key Findings Box
**Purpose:** Non-technical summary callout inside notebook pages
**Usage:** Place above the rendered notebook HTML

```astro
---
// src/components/KeyFindings.astro
interface Props {
  findings: string[];
}
---
<div class="bg-amber-50 dark:bg-amber-950 border-l-4 border-brand-amber p-6 my-8 rounded-r-lg">
  <h3 class="font-semibold text-brand-amber mb-3">⚡ Key Findings</h3>
  <ul class="space-y-2">
    {findings.map(f => (
      <li class="flex gap-2 text-sm">
        <span class="text-brand-amber mt-0.5">→</span>
        <span>{f}</span>
      </li>
    ))}
  </ul>
</div>
```

### Hero Section (Home Page)
```astro
---
// src/components/Hero.astro
// Full-width intro section with name, title, CTA buttons
---
<section class="py-24 md:py-32">
  <div class="max-w-5xl mx-auto px-6">
    <p class="text-brand-amber font-mono text-sm mb-4 tracking-widest uppercase">Industrial Energy Manager</p>
    <h1 class="text-5xl md:text-7xl font-bold text-brand-navy dark:text-white mb-6 leading-tight">
      Mike Leishman
    </h1>
    <p class="text-xl text-slate-500 max-w-2xl mb-10">
      I help industrial facilities reduce energy costs through data-driven analysis. 
      Here's my work.
    </p>
    <div class="flex gap-4 flex-wrap">
      <a href="/portfolio" class="btn-primary">View Portfolio</a>
      <a href="/blog" class="btn-secondary">Read Blog</a>
    </div>
  </div>
</section>
```

---

## 4. Utility Functions

### Reading Time Calculator
```javascript
// src/utils/readingTime.js
export function getReadingTime(content) {
  const wordsPerMinute = 200;
  const wordCount = content.split(/\s+/).length;
  return Math.ceil(wordCount / wordsPerMinute);
}
```

### Date Formatter
```javascript
// src/utils/dateFormat.js
export function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-CA', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}
```

### Tag Filter (Client-side)
```javascript
// src/utils/tagFilter.js
// Used on blog and portfolio pages for client-side filtering
export function filterByTag(items, selectedTag) {
  if (!selectedTag || selectedTag === 'all') return items;
  return items.filter(item => item.tags.includes(selectedTag));
}
```

---

## 5. Content Collection Schemas

### Blog Posts Schema
```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    tags: z.array(z.enum(['case-study', 'opinion', 'tutorial'])),
    summary: z.string(),
    draft: z.boolean().default(true),
  }),
});
```

### Notebooks Schema
```typescript
const notebooks = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.string(),
    tags: z.array(z.string()),
    techStack: z.array(z.string()),
    sector: z.enum(['industrial', 'commercial', 'utility', 'other']),
    summary: z.string(),
    keyFindings: z.array(z.string()),
    notebookFile: z.string(),
    renderedFile: z.string(),
  }),
});
```

---

## 6. GitHub Actions Workflow Template

```yaml
# .github/workflows/deploy.yml
name: Build & Deploy to WebHostingCanada

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build site
        run: npm run build

      - name: Deploy via FTP
        uses: SamKirkland/FTP-Deploy-Action@v4.3.4
        with:
          server: ${{ secrets.FTP_SERVER }}
          username: ${{ secrets.FTP_USERNAME }}
          password: ${{ secrets.FTP_PASSWORD }}
          local-dir: ./dist/
          server-dir: /public_html/
```

**Required GitHub Secrets:**
- `FTP_SERVER` — WebHostingCanada FTP hostname
- `FTP_USERNAME` — FTP username
- `FTP_PASSWORD` — FTP password

---

## 7. Notebook Rendering Script

```bash
#!/bin/bash
# scripts/render-notebooks.sh
# Usage: ./scripts/render-notebooks.sh [notebook-name.ipynb]
# Renders one or all notebooks in /notebooks/source/ to /notebooks/rendered/

NOTEBOOK=$1
SOURCE_DIR="notebooks/source"
OUTPUT_DIR="notebooks/rendered"

if [ -z "$NOTEBOOK" ]; then
  # Render all notebooks
  for nb in $SOURCE_DIR/*.ipynb; do
    jupyter nbconvert --to html \
      --template classic \
      --output-dir $OUTPUT_DIR \
      "$nb"
    echo "Rendered: $nb"
  done
else
  jupyter nbconvert --to html \
    --template classic \
    --output-dir $OUTPUT_DIR \
    "$SOURCE_DIR/$NOTEBOOK"
fi

echo "Done. Check $OUTPUT_DIR/ for rendered HTML files."
```

---

## 8. SEO Patterns

### Standard OG Tags (add to BaseLayout.astro)
```html
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:type" content="website" />
<meta property="og:image" content={ogImage ?? '/og-default.png'} />
<meta name="twitter:card" content="summary_large_image" />
```

### Sitemap config
```javascript
// astro.config.mjs
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://abriliamconsulting.com',
  integrations: [sitemap()],
})
```

---

## 9. Skill Log

> When a new reusable pattern is built, add a one-line entry here.

| Date | Pattern | File Location | Notes |
|---|---|---|---|
| [date] | Base layout | `src/layouts/BaseLayout.astro` | Initial scaffold |
| — | — | — | Add entries as you build — |

---

## 10. Known Gotchas

- **WebHostingCanada + Astro:** Must use static output mode (`output: 'static'` in `astro.config.mjs`). SSR requires Node adapter which may not be supported on all WHC plans — verify before enabling.
- **nbconvert HTML embeds:** Rendered notebooks include their own CSS. Wrap in an iframe or a scoped container to prevent style bleed into the main site layout.
- **Dark mode + notebook HTML:** nbconvert output won't automatically dark-mode. Add a CSS filter (`filter: invert(1) hue-rotate(180deg)`) on the notebook container for a quick dark-mode fix, or use a custom nbconvert template.
- **Draft posts in build:** Astro includes draft posts in dev but excludes them in production builds — verify your content collection filter is correct.
