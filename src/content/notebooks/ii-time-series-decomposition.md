---
title: "02 — DWF Baseline & Time Series Decomposition"
date: "2025-11-20"
tags: ["stl-decomposition", "dry-weather-flow", "rdii", "time-series"]
techStack: ["Python", "pandas", "numpy", "statsmodels", "matplotlib", "seaborn"]
sector: "utility"
summary: "Establishes dry weather flow baselines using STL decomposition, computes RDII for each wet-weather and snowmelt event, and validates results against MECP per-capita flow guidelines."
keyFindings:
  - "STL decomposition cleanly separates diurnal wastewater patterns from wet-weather RDII events"
  - "Per-capita DWF validation against MECP guidelines flags plants with chronic baseflow infiltration"
  - "RDII mass balance checks confirm physically plausible runoff coefficients (1-10% of rainfall entering the sewer)"
notebookFile: "ii-02-time-series-decomposition.ipynb"
renderedFile: "ii-02-time-series-decomposition.html"
project: "sewer-ii-detection"
projectTitle: "Sewer I&I Detection & Energy Impact Analysis"
projectSummary: "Multi-method detection of inflow and infiltration in municipal sanitary sewers using lag analysis, hydrograph decomposition, dilution tracing, and machine learning — with energy penalty quantification and remediation prioritization across a multi-plant collection system"
order: 2
---
