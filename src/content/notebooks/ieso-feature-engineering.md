---
title: "02 — Feature Engineering"
date: "2025-10-09"
tags: ["feature-engineering", "humidex", "cooling-degree-hours", "temporal-features"]
techStack: ["Python", "pandas", "numpy", "matplotlib", "seaborn"]
sector: "utility"
summary: "Transforms raw demand and weather data into ML-ready features including humidex, cooling degree hours, demand momentum, and peak context variables."
keyFindings:
  - "Humidex and daily CDH emerge as stronger predictors than raw temperature alone"
  - "Previous day's max demand captures system-level momentum that weather features miss"
  - "Peak context features (current threshold, peaks so far) provide essential operational framing"
notebookFile: "ieso-02-feature-engineering.ipynb"
renderedFile: "ieso-02-feature-engineering.html"
project: "ieso-peak-prediction"
projectTitle: "IESO Coincident Peak Prediction"
projectSummary: "ML-driven prediction of Ontario's top-5 system demand hours for Class A Global Adjustment optimization"
order: 2
---
