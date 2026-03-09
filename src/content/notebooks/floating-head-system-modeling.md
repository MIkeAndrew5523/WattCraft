---
title: "01 — System Modeling & Temperature Bin Analysis"
date: "2025-01-09"
tags: ["refrigeration", "floating-head-pressure", "bin-analysis", "energy-savings"]
techStack: ["Python", "numpy", "pandas", "matplotlib", "scipy"]
sector: "commercial"
summary: "Builds a compressor performance model for a grocery cold storage reciprocating rack system on R-448A and runs a temperature bin analysis using TMY weather data to estimate annual compressor energy savings from floating head pressure control under two retrofit tiers."
keyFindings:
  - "Tier 1 (TEV-constrained float, floor 27°C) reduces annual compressor energy by approximately 15-20%"
  - "Tier 2 (EEV retrofit, floor 18°C) reduces annual compressor energy by approximately 25-35%"
  - "Majority of savings accrue in the 3,000+ hours per year when outdoor temperature is below 27°C"
  - "Condenser fan energy penalty is 5-10% of gross compressor savings — net benefit is strongly positive"
notebookFile: "floating-head-01-system-modeling.ipynb"
renderedFile: "floating-head-01-system-modeling.html"
project: "floating-head-pressure"
projectTitle: "Floating Head Pressure — Grocery Cold Storage"
projectSummary: "Savings estimation and M&V framework for floating condenser head pressure control on a grocery chain cold storage warehouse with reciprocating compressor racks and air-cooled condensers — covering TEV-constrained and EEV-enabled retrofit tiers."
order: 1
---

Compressor performance modeling and temperature bin analysis for estimating annual energy savings from floating head pressure control. Uses COP-based compressor power calculations and TMY weather data for southern Ontario to quantify the savings potential under two implementation scenarios: a controls-only retrofit (Tier 1, TEV floor) and a full EEV retrofit (Tier 2, lower floor).
