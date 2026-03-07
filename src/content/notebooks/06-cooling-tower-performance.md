---
title: "06 — Cooling Tower Performance"
date: "2026-03-07"
tags: ["chiller-plant", "cooling-tower", "heat-rejection", "free-cooling"]
techStack: ["Python", "pandas", "numpy", "matplotlib"]
sector: "industrial"
summary: "Heat rejection calculations, tower approach trending, fan power analysis, and free-cooling feasibility assessment."
keyFindings:
  - "Cooling tower approach rises by +1.5°C over the period indicating degradation"
  - "Free-cooling feasibility: 0% of hours qualify with 3°C approach"
  - "Night-time fan control bias detected via 24-hour SMA smoothing"
notebookFile: "06-cooling-tower-performance.ipynb"
renderedFile: "06-cooling-tower-performance.html"
project: "chiller-plant-diagnostics"
projectTitle: "Chiller Plant Diagnostics"
projectSummary: "End-to-end diagnostic analysis of a central chiller plant with three embedded operational faults — from data generation through fault detection to energy waste quantification."
order: 6
---

Comprehensive cooling tower performance analysis: physics-based heat rejection calculations, approach temperature trending over time, fan power vs approach relationships, CW supply vs wet-bulb analysis, free-cooling feasibility check, and night-time fan control bias detection.
