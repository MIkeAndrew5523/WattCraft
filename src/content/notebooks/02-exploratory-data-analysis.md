---
title: "02 — Exploratory Data Analysis"
date: "2024-09-18"
tags: ["chiller-plant", "eda", "time-series", "rolling-average"]
techStack: ["Python", "pandas", "matplotlib"]
sector: "industrial"
summary: "Data quality checks, descriptive statistics, time-series visualization, and rolling SMA trend analysis of chiller plant operations."
keyFindings:
  - "Zero missing values across all 23 columns"
  - "24-hour and 240-hour SMAs reveal drift in kW/ton efficiency over the dataset period"
  - "CW flow vs kW/ton spline analysis highlights flow-efficiency coupling"
notebookFile: "02-exploratory-data-analysis.ipynb"
renderedFile: "02-exploratory-data-analysis.html"
project: "chiller-plant-diagnostics"
projectTitle: "Chiller Plant Diagnostics"
projectSummary: "End-to-end diagnostic analysis of a central chiller plant with three embedded operational faults — from data generation through fault detection to energy waste quantification."
order: 2
---

Initial exploration of the chiller plant dataset: data quality validation, summary statistics, dual-axis time-series of plant kW vs cooling tons, and rolling simple moving average analysis to detect efficiency trends.
