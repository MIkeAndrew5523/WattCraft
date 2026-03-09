---
title: "02 — HDD Regression & Normalization"
date: "2026-01-22"
tags: ["regression", "normalization", "hdd", "building-stock"]
techStack: ["Python", "pandas", "numpy", "scipy", "matplotlib", "seaborn"]
sector: "other"
summary: "Runs OLS regression per postal code, applies quality filters, normalizes slopes by MPAC building stock characteristics, and produces a thermal intensity metric for neighbourhood ranking."
keyFindings:
  - "OLS regression per postal code achieves R² > 0.80 for the majority of residential postal codes"
  - "Normalization by heated volume materially reshuffles the raw slope ranking"
  - "Normalized thermal intensity correlates strongly with ground truth in the synthetic validation"
notebookFile: "ces-02-regression-normalization.ipynb"
renderedFile: "ces-02-regression-normalization.html"
project: "community-envelope-screening"
projectTitle: "Gas Bills by Postal Code"
projectSummary: "Postal code gas consumption screening to identify neighbourhoods with poor building envelopes for municipal retrofit incentive targeting"
order: 2
---
