---
title: "05 — Low Delta-T Syndrome"
date: "2025-08-12"
tags: ["chiller-plant", "low-delta-t", "fault-detection", "efficiency"]
techStack: ["Python", "pandas", "numpy", "matplotlib"]
sector: "industrial"
summary: "Deep dive into low-delta-T syndrome using quantile-based thresholds and efficiency classification."
keyFindings:
  - "17.3% of operating hours classified as inefficient (plant kW/ton > 4.0)"
  - "Inefficient hours cluster at low wet-bulb (median 11.9°C) and low load (median 96 tons)"
  - "Power floor estimated at ~142 kW with incremental cost of 2.87 kW/ton"
notebookFile: "05-low-delta-t-syndrome.ipynb"
renderedFile: "05-low-delta-t-syndrome.html"
project: "chiller-plant-diagnostics"
projectTitle: "Chiller Plant Diagnostics"
projectSummary: "End-to-end diagnostic analysis of a central chiller plant with three embedded operational faults — from data generation through fault detection to energy waste quantification."
order: 5
---

Systematic investigation of low-delta-T syndrome: configurable threshold analysis, quantile-based fault flagging, efficiency classification, power floor detection, and identification of the worst-performing operating hours.
