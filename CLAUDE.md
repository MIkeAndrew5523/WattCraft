# CLAUDE.md — AI Agent Context File
## Project: Industrial Energy Manager Portfolio & Blog

> This file is the primary context document for any AI agent (Claude Code, Cursor, etc.) working on this project. Read this first before taking any action.

---

## 1. Project Identity

**Site Name:** Abriliam Consulting — abriliamconsulting.com
**Owner:** Mike Leishman — Professional Industrial Energy Manager based in Canada
**Purpose:** A personal brand platform that serves three goals simultaneously:
1. Showcase analytical work (Jupyter notebooks as project case studies)
2. Publish thought leadership (blog: opinion pieces, tutorials, case studies)
3. Document the agentic AI development workflow used to build the site itself

**Meta-purpose:** The act of building this site *is itself* a portfolio project — demonstrating proficiency in spec-driven, LLM-assisted software development.

---

## 2. Target Audience

| Audience Segment | Technical Level | Primary Need |
|---|---|---|
| Prospective consulting clients | Low-Medium | See credibility, contact easily |
| Hiring managers / recruiters | Medium | Assess skills, download resume |
| Fellow energy engineers | High | Learn from notebooks & tutorials |
| Data scientists / developers | High | See agentic dev workflow |

**Tone:** Professional but approachable. Not academic. Not corporate. Think: "senior practitioner sharing hard-won knowledge."

---

## 3. Recommended Tech Stack

The agent should default to this stack unless the owner explicitly changes it:

### Frontend
- **Framework:** [Astro](https://astro.build/) — ideal for content-heavy sites, ships zero JS by default, supports React/MDX islands
- **Styling:** Tailwind CSS
- **Blog engine:** Astro Content Collections (Markdown/MDX files in `/content/`)
- **Notebook rendering:** `nbconvert` → static HTML pages, embedded in Astro pages

### Backend / CMS
- **Content management:** File-based (Markdown in Git) — no CMS needed for solo author
- **Contact form:** Netlify Forms or Formspree (no server needed)
- **No database required** for MVP

### Hosting & Deployment
- **Host:** WebHostingCanada (PHP/Node/Python support confirmed)
- **Domain:** `abriliamconsulting.com` — registered at WordPress.com, **do not transfer**
- **DNS strategy:** Domain stays at WordPress.com as registrar only. At launch, update the A record in WordPress.com DNS settings to point to WHC server IP. No email to preserve.
- **Deployment method:** GitHub Actions CI/CD → FTP/SFTP deploy to WebHostingCanada
- **Build:** Astro static build (`npm run build` → `/dist` folder)

### DNS Launch Checklist (Do this last — after site is built and deployed to WHC)
1. Get WHC server IP from WebHostingCanada control panel
2. Log into WordPress.com → Upgrades → Domains → abriliamconsulting.com
3. Click "DNS records"
4. Find the A record for @ (root domain) and update value to WHC server IP
5. Save and wait 24-48hrs for propagation
6. Verify site is live at abriliamconsulting.com

Notes:
- Transfer lock on WordPress.com should remain ON — do not touch it
- Domain renews September 2026 at US$19/yr — auto-renew is enabled
- Do not use "Transfer" or "Detach" buttons in WordPress.com domain settings
- The mleishman@abriliamconsulting.com mailbox can be abandoned — no email continuity needed

### Development Workflow
- **Version control:** GitHub (mono-repo)
- **AI assistant:** Claude Code (VS Code plugin) — using Agent Teams (not subagents)
- **Spec format:** This repo's `/docs/` folder contains all planning specs
- **Branching:** `main` (production), `dev` (active work), feature branches per task

### Agent Team Structure

This project uses Claude Code's **Agent Teams** to coordinate multiple specialized agents working collectively. The team lead orchestrates work via a shared task list; teammates execute in parallel.

**Team name:** `abriliam-site`

| Role | Agent Name | Type | Responsibilities |
|---|---|---|---|
| Team Lead | `lead` | Coordinator | Reads specs, creates tasks, reviews output, manages task list |
| Frontend Builder | `frontend` | Full-capability | Astro pages, components, layouts, Tailwind styling |
| Content & Config | `content` | Full-capability | Content schemas, markdown templates, utility functions |
| DevOps | `devops` | Full-capability | CI/CD workflow, deployment config, build scripts |
| QA & Testing | `qa` | Full-capability | Runs builds, tests routes, logs bugs, assigns fix tasks |
| Research | `researcher` | Read-only (Explore) | Codebase search, documentation lookup, gap analysis |

**QA agent protocol:**
- Runs `npm run build` after every batch of teammate completions
- Tests all page routes render without errors
- Validates content schemas against actual markdown files
- Logs bugs as new tasks on the shared task list with `[BUG]` prefix and assigns to the appropriate teammate
- Runs a final full-site verification before any milestone is reported as complete
- Checks for: broken links, missing assets, TypeScript errors, Tailwind class issues, build warnings

**Coordination rules:**
- Team lead creates and assigns tasks via the shared task list
- Teammates claim unassigned tasks in ID order (lowest first)
- Each teammate marks tasks complete immediately when done, then checks for next work
- Teammates communicate via `SendMessage` — not terminal tools
- All teammates read `CLAUDE.md`, `AGENT.md`, and `SKILLS.md` before starting work
- QA agent runs verification after each batch of completed tasks — no milestone ships without QA sign-off
- When all tasks are done, team lead shuts down teammates gracefully

**When to spin up the team:**
- Multi-file scaffold operations (like notebook_zero)
- Feature work spanning frontend + content + config
- Any task touching 4+ files across different domains

**When NOT to use the team (single agent is fine):**
- Single file edits or bug fixes
- Content-only changes (adding a blog post)
- Quick config tweaks

---

## 4. Repository Structure

```
/
├── CLAUDE.md              ← YOU ARE HERE — AI context file
├── AGENT.md               ← Agentic workflow rules & task protocol
├── SKILLS.md              ← Reusable patterns & component library
├── docs/
│   ├── architecture.md    ← System design decisions
│   ├── content-plan.md    ← Blog & notebook content strategy
│   └── deployment.md      ← WebHostingCanada deployment guide
├── src/
│   ├── pages/             ← Astro pages
│   ├── content/
│   │   ├── blog/          ← .md/.mdx blog posts
│   │   └── notebooks/     ← Notebook metadata .md files
│   ├── components/        ← Astro/React components
│   └── layouts/           ← Page layouts
├── notebooks/
│   ├── source/            ← Original .ipynb files
│   └── rendered/          ← nbconvert HTML output
├── public/                ← Static assets (images, favicon, etc.)
└── .github/workflows/     ← CI/CD pipeline
```

---

## 5. Site Pages & Features (MVP)

### Pages
| Page | Route | Purpose |
|---|---|---|
| Home | `/` | Hero, intro, featured work, CTA |
| About | `/about` | Bio, credentials, resume download |
| Portfolio | `/portfolio` | Grid of notebook projects |
| Notebook Viewer | `/portfolio/[slug]` | Rendered notebook + metadata |
| Blog | `/blog` | List of posts (case studies, opinions, tutorials) |
| Blog Post | `/blog/[slug]` | Individual post |
| Contact | `/contact` | Simple form |

### Content Types
1. **Notebook Project** — metadata card + rendered HTML from `.ipynb`
2. **Blog Post** — Markdown/MDX with tags: `case-study`, `opinion`, `tutorial`

### Features (MVP)
- Responsive design (mobile-first)
- Dark/light mode toggle
- Tag-based filtering on blog & portfolio
- RSS feed
- SEO meta tags (Open Graph, Twitter Card)
- Reading time estimates
- Static site (no auth, no database)

### Features (Post-MVP)
- Search (Pagefind — static search)
- Newsletter signup (Buttondown or similar)
- Comments (Giscus — GitHub Discussions)

---

## 6. Content Strategy

### Blog Categories
- **Case Studies** — Real projects (anonymized if needed), problem → analysis → outcome
- **Opinion Pieces** — Short takes on energy policy, markets, industry trends
- **Tutorials** — How-to guides for energy analytics tools, Python, data methods

### Notebook Projects
Each notebook project should include:
- Title & summary (non-technical version)
- Tags: technology used, industry sector, analysis type
- The rendered notebook (HTML)
- Key findings callout box (for non-technical visitors)

---

## 7. Design Principles

- **Clean and data-forward** — Let the work speak. No cluttered layouts.
- **Dual-audience design** — Summaries for business readers, full depth for technical ones
- **Fast** — Static site, optimized images, < 2s load time target
- **Professional palette** — Think deep navy, slate, with an energy-sector accent (amber or electric blue)

---

## 8. Constraints & Non-Goals

- **No user auth** (MVP) — No login, no user accounts
- **No live notebook execution** — Notebooks are rendered to static HTML only
- **No WordPress** — File-based content in Git only
- **No paid APIs** — All tooling must be free tier or self-hosted
- **English only** (MVP)

---

## 9. Context Window Efficiency & Document Hygiene

> **Why this matters:** These planning documents are loaded into the AI agent's context window at the start of every session. Bloated docs waste tokens, increase cost, reduce response quality, and can crowd out room for actual code and task context. Treat these files like production code — they need maintenance.

### Document Size Budgets

| File | Soft Limit | Hard Limit | Action if Exceeded |
|---|---|---|---|
| `CLAUDE.md` | 400 lines | 600 lines | Audit & prune or split |
| `AGENT.md` | 300 lines | 450 lines | Move examples to `docs/` |
| `SKILLS.md` | 500 lines | 800 lines | Archive old patterns |

### When to Audit (Trigger Conditions)

The agent should flag a context audit when **any** of the following are true:
- Any planning doc exceeds its soft limit
- A new major feature or content type has been added to the project
- The project reaches a milestone (first deploy, 5th notebook, 10th blog post)
- The agent notices it is re-reading the same context repeatedly without acting on it
- A section hasn't been referenced in 3+ sessions

### Audit Protocol (Agent Instructions)

When triggered, the agent should perform the following and report findings before making changes:

**Step 1 — Measure**
```bash
wc -l CLAUDE.md AGENT.md SKILLS.md
```
Report line counts against the budget table above.

**Step 2 — Identify Waste**
Scan each document for:
- ❌ **Resolved TODOs** — decisions already made, remove the deliberation
- ❌ **Redundancy** — the same rule stated in two places; keep the canonical one
- ❌ **Scaffolding notes** — setup instructions that are now complete history
- ❌ **Over-specified examples** — code samples that are now in actual source files
- ❌ **Stale gotchas** — known issues that have since been fixed

**Step 3 — Propose Changes**
Present a bulleted list of proposed removals/moves to the owner. Do not edit without approval.

**Step 4 — Archive, Don't Delete**
Anything removed from a planning doc should move to `/docs/archive/` — not deleted. Use commit type `chore(docs): archive [section name] from CLAUDE.md`.

**Step 5 — Verify Compression**
After edits, re-run `wc -l` and confirm the doc is back within budget.

### Structural Rules to Prevent Bloat

- **CLAUDE.md** — Project identity, goals, stack, site map, constraints only. No code samples.
- **AGENT.md** — Behavioral rules and protocols only. Examples > 5 lines go in `docs/`.
- **SKILLS.md** — Living pattern library. When a pattern is implemented in real source code, replace the full sample with a one-line pointer: `→ See src/components/NotebookCard.astro`
- **No inline changelogs** — Git history is the changelog. Never add "Updated 2024-XX-XX: changed X to Y" comments inside these files.

### Splitting Strategy (When a Doc Outgrows Its Budget)

If `SKILLS.md` exceeds its hard limit, split by domain:
```
SKILLS.md              ← index file with one-liners + pointers
SKILLS-components.md   ← Astro/React component patterns
SKILLS-content.md      ← Content schemas, frontmatter, notebook pipeline
SKILLS-devops.md       ← CI/CD, deployment, git workflow
```

If `CLAUDE.md` outgrows its budget, extract deep content to `docs/`:
```
CLAUDE.md              ← stays as high-level brief (≤ 300 lines)
docs/architecture.md   ← detailed stack decisions
docs/content-plan.md   ← detailed content strategy
```

---

## 10. Success Metrics

- Site live on custom domain via WebHostingCanada
- At least 3 notebook projects published
- At least 3 blog posts published
- Contact form functional
- Build & deploy pipeline automated via GitHub Actions
- The build process itself documented as a blog post / portfolio item
