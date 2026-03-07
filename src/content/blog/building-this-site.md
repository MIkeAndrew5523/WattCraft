---
title: "Building This Site with Spec-Driven AI Development"
date: "2026-03-07"
tags: ["tutorial"]
summary: "How I used Claude Code and a spec-driven workflow to build this portfolio site from scratch."
draft: true
---

This site was built using a spec-driven development workflow powered by Claude Code and Astro. Rather than starting with a blank editor and writing code line by line, I began by writing detailed specification documents — CLAUDE.md, AGENT.md, and SKILLS.md — that describe the project's goals, architecture, design system, and reusable patterns. The AI agent reads these specs at the start of every session and uses them as the source of truth for all decisions.

The workflow uses an agent team structure where specialized agents handle different parts of the build in parallel: frontend layout and components, content schemas and utilities, DevOps and deployment configuration, and quality assurance. Each agent reads the same specs, follows the same conventions, and communicates through a structured task system. The result is a coherent codebase that looks like it was built by a single developer with a clear plan.

What makes this approach compelling as a portfolio piece is that the process itself is the product. The commit history tells a coherent story, the specs are version-controlled alongside the code, and every architectural decision is documented. If you are interested in how AI-assisted development works in practice — not as a demo or toy project, but as a real production workflow — this site and its source code are the case study.
