---
title: "01 — Data Acquisition & Exploratory Analysis"
date: "2026-03-09"
tags: ["natural-gas", "postal-code", "mpac", "exploratory-analysis"]
techStack: ["Python", "pandas", "numpy", "matplotlib", "seaborn"]
sector: "other"
summary: "Ingests aggregated residential gas consumption by postal code, regional HDD data, and MPAC property tax roll summaries. Performs EDA on gas-temperature relationships across 150 synthetic postal codes."
keyFindings:
  - "150 postal codes with 24 months of residential gas data assembled from utility and MPAC sources"
  - "Clear linear relationship between monthly gas consumption and HDD visible at the postal code level"
  - "Customer counts range from 10–40 per postal code, typical of Ontario suburban FSAs"
notebookFile: "ces-01-data-acquisition.ipynb"
renderedFile: "ces-01-data-acquisition.html"
project: "community-envelope-screening"
projectTitle: "Gas Bills by Postal Code"
projectSummary: "Postal code gas consumption screening to identify neighbourhoods with poor building envelopes for municipal retrofit incentive targeting"
order: 1
---
