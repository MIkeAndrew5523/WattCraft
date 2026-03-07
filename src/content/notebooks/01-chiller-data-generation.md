---
title: "01 — Data Generation & Setup"
date: "2026-03-07"
tags: ["chiller-plant", "synthetic-data", "fault-injection"]
techStack: ["Python", "numpy", "pandas", "matplotlib"]
sector: "industrial"
summary: "Generates a synthetic 8-week chiller plant dataset with three embedded operational faults for diagnostic training."
keyFindings:
  - "1,344 hourly data points simulating a central chiller plant (June–July 2025)"
  - "Three hidden faults injected: low-delta-T syndrome, cooling tower degradation, night-time fan bias"
  - "23 columns covering temperatures, flows, power, and derived KPIs"
notebookFile: "01-chiller-plant-data-generation.ipynb"
renderedFile: "01-chiller-plant-data-generation.html"
project: "chiller-plant-diagnostics"
projectTitle: "Chiller Plant Diagnostics"
projectSummary: "End-to-end diagnostic analysis of a central chiller plant with three embedded operational faults — from data generation through fault detection to energy waste quantification."
order: 1
---

Synthetic chiller plant dataset creation with embedded operational faults for energy management diagnostic training. The dataset simulates real-world HVAC conditions including weather drivers, occupancy patterns, and cooling load dynamics.
