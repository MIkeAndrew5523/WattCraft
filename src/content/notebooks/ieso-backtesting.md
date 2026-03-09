---
title: "04 — Backtesting & Financial Valuation"
date: "2025-10-23"
tags: ["backtesting", "walk-forward", "financial-analysis", "global-adjustment"]
techStack: ["Python", "pandas", "matplotlib", "seaborn", "numpy"]
sector: "utility"
summary: "Walk-forward backtesting across multiple base periods with confusion matrices, alert calendars, and financial valuation for a hypothetical 10 MW Class A customer."
keyFindings:
  - "Walk-forward validation across 5 base periods demonstrates consistent peak detection performance"
  - "RED alert precision and recall trade-off calibrated to minimize missed peaks (the costlier error)"
  - "Model-guided curtailment outperforms naive temperature heuristic by reducing false alarm days"
notebookFile: "ieso-04-backtesting.ipynb"
renderedFile: "ieso-04-backtesting.html"
project: "ieso-peak-prediction"
projectTitle: "IESO Coincident Peak Prediction"
projectSummary: "ML-driven prediction of Ontario's top-5 system demand hours for Class A Global Adjustment optimization"
order: 4
---
