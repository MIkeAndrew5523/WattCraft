---
title: "01 — Data Acquisition & Exploratory Analysis"
date: "2025-10-02"
tags: ["ieso", "demand-data", "weather-api", "exploratory-analysis"]
techStack: ["Python", "pandas", "matplotlib", "seaborn", "requests", "openpyxl"]
sector: "utility"
summary: "Fetches 15 years of IESO hourly demand data and Open-Meteo weather for Toronto, merges datasets, and performs comprehensive EDA on peak demand patterns."
keyFindings:
  - "15 base periods of hourly Ontario demand (2010–2025) combined from local ICI files and IESO public CSVs"
  - "~90% of top-5 peaks occur June–August, on weekdays, between 3–7 PM EST"
  - "Strong nonlinear relationship between daily max temperature and daily max demand above ~22°C"
notebookFile: "ieso-01-data-acquisition.ipynb"
renderedFile: "ieso-01-data-acquisition.html"
project: "ieso-peak-prediction"
projectTitle: "IESO Coincident Peak Prediction"
projectSummary: "ML-driven prediction of Ontario's top-5 system demand hours for Class A Global Adjustment optimization"
order: 1
---
