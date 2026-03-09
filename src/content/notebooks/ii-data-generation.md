---
title: "01 — Synthetic Data Generation"
date: "2025-11-13"
tags: ["synthetic-data", "wastewater", "i-and-i", "snowmelt", "scada"]
techStack: ["Python", "pandas", "numpy", "scipy", "matplotlib"]
sector: "utility"
summary: "Generates realistic synthetic SCADA data for multiple WWTP service areas with distinct I&I severity profiles — including rainfall-driven RDII, snowmelt-driven infiltration, conductivity dilution, and pump station sub-catchment flow."
keyFindings:
  - "Synthetic plants span low/medium/high I&I severity with inflow-dominated, infiltration-dominated, and mixed response types"
  - "Spring snowmelt events produce the largest sustained I&I volumes for infiltration-dominated plants"
  - "Sub-catchment pump station data demonstrates spatial I&I variability within a single plant service area"
notebookFile: "ii-01-data-generation.ipynb"
renderedFile: "ii-01-data-generation.html"
project: "sewer-ii-detection"
projectTitle: "Sewer I&I Detection & Energy Impact Analysis"
projectSummary: "Multi-method detection of inflow and infiltration in municipal sanitary sewers using lag analysis, hydrograph decomposition, dilution tracing, and machine learning — with energy penalty quantification and remediation prioritization across a multi-plant collection system"
order: 1
---
