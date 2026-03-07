---
title: "07 — Efficiency Summary & Energy Waste"
date: "2026-03-07"
tags: ["chiller-plant", "energy-waste", "subsystem-analysis", "summary"]
techStack: ["Python", "pandas", "numpy", "matplotlib"]
sector: "industrial"
summary: "Subsystem dominance analysis, energy waste quantification, and rolling SMA dashboards for final diagnostic conclusions."
keyFindings:
  - "99.1 MWh wasted during inefficient operation (10.2% of 971.5 MWh total)"
  - "Chiller-dominated inefficiency for 100% of flagged hours"
  - "Rolling SMA dashboards reveal correlated drift in delta-P, CW temps, and fan power"
notebookFile: "07-plant-efficiency-summary.ipynb"
renderedFile: "07-plant-efficiency-summary.html"
project: "chiller-plant-diagnostics"
projectTitle: "Chiller Plant Diagnostics"
projectSummary: "End-to-end diagnostic analysis of a central chiller plant with three embedded operational faults — from data generation through fault detection to energy waste quantification."
order: 7
---

Final diagnostic summary: quantifies energy waste tied to inefficient operation, determines which subsystem dominates during bad hours, and presents rolling SMA dashboards consolidating delta-P, CW temperatures, fan power, and overall plant efficiency trends.
