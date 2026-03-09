---
title: "04 — Hydraulic Regime Detection"
date: "2024-10-03"
tags: ["chiller-plant", "clustering", "gmm", "hydraulics", "regime-detection"]
techStack: ["Python", "scikit-learn", "matplotlib"]
sector: "industrial"
summary: "Differential pressure analysis and Gaussian Mixture Model clustering to identify two distinct operational regimes."
keyFindings:
  - "Bimodal delta-P distribution reveals two hydraulic configurations"
  - "GMM clustering identifies 422 hours in regime 0 vs 922 hours in regime 1"
  - "Q² vs delta-P scatter confirms two distinct flow-pressure relationships"
notebookFile: "04-hydraulic-regime-detection.ipynb"
renderedFile: "04-hydraulic-regime-detection.html"
project: "chiller-plant-diagnostics"
projectTitle: "Chiller Plant Diagnostics"
projectSummary: "End-to-end diagnostic analysis of a central chiller plant with three embedded operational faults — from data generation through fault detection to energy waste quantification."
order: 4
---

Investigates hydraulic operating regimes using differential pressure histograms, hydraulic coefficient analysis (k_hyd = ΔP/Q²), and unsupervised Gaussian Mixture Model clustering on pressure and fan power features.
