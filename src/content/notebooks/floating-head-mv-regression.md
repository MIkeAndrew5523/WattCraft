---
title: "02 — M&V Regression Framework & Sensitivity Analysis"
date: "2025-09-11"
tags: ["refrigeration", "floating-head-pressure", "m-and-v", "regression", "ipmvp"]
techStack: ["Python", "numpy", "pandas", "matplotlib", "scipy"]
sector: "commercial"
summary: "Demonstrates regression-based measurement and verification (M&V) for floating head pressure savings using simulated pre/post compressor power data, and performs sensitivity analysis on key assumptions including electricity rate, minimum condensing floor, and condenser approach temperature."
keyFindings:
  - "Pre/post kW vs. T_ambient regression isolates floating head pressure savings from other variables"
  - "R-squared > 0.80 achievable for constant-load cold storage facilities using hourly submetered data"
  - "Savings are most sensitive to the minimum condensing temperature floor — each 3°C reduction in floor adds approximately 5-8% savings"
  - "Simple payback under 1 year for Tier 1, 2-3 years for Tier 2 at Ontario industrial electricity rates"
notebookFile: "floating-head-02-mv-regression.ipynb"
renderedFile: "floating-head-02-mv-regression.html"
project: "floating-head-pressure"
projectTitle: "Floating Head Pressure — Grocery Cold Storage"
projectSummary: "Savings estimation and M&V framework for floating condenser head pressure control on a grocery chain cold storage warehouse with reciprocating compressor racks and air-cooled condensers — covering TEV-constrained and EEV-enabled retrofit tiers."
order: 2
---

Regression-based measurement and verification framework for validating floating head pressure energy savings. Simulates pre-retrofit and post-retrofit compressor power data, fits OLS regressions against outdoor temperature, and quantifies verified savings as the area between regression lines. Includes sensitivity analysis on electricity rate, minimum condensing floor, and condenser approach temperature.
