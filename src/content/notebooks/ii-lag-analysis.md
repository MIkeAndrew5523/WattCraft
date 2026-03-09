---
title: "03 — Cross-Correlation Lag Analysis"
date: "2025-11-20"
tags: ["cross-correlation", "lag-analysis", "pre-whitening", "arima", "i-and-i-classification"]
techStack: ["Python", "pandas", "numpy", "statsmodels", "scipy", "matplotlib", "seaborn"]
sector: "utility"
summary: "Computes pre-whitened cross-correlation between rainfall/snowmelt and sewer flow for each plant, identifies dominant lag signatures, and classifies plants as inflow-dominated, infiltration-dominated, or mixed."
keyFindings:
  - "Pre-whitening removes autocorrelation artifacts that inflate raw CCF peaks — essential for accurate lag identification"
  - "Inflow-dominated plants show sharp CCF peaks at 1-3 hour lag; infiltration-dominated show broad peaks at 24-48 hours"
  - "Snowmelt-flow CCF reveals different lag characteristics than rainfall-flow CCF, with broader, more sustained correlation"
notebookFile: "ii-03-lag-analysis.ipynb"
renderedFile: "ii-03-lag-analysis.html"
project: "sewer-ii-detection"
projectTitle: "Sewer I&I Detection & Energy Impact Analysis"
projectSummary: "Multi-method detection of inflow and infiltration in municipal sanitary sewers using lag analysis, hydrograph decomposition, dilution tracing, and machine learning — with energy penalty quantification and remediation prioritization across a multi-plant collection system"
order: 3
---
