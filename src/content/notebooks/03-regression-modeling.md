---
title: "03 — Regression Modeling"
date: "2024-09-25"
tags: ["chiller-plant", "regression", "scikit-learn", "prediction"]
techStack: ["Python", "scikit-learn", "scipy", "matplotlib"]
sector: "industrial"
summary: "Simple and multivariable linear regression with residual diagnostics and short-window prediction generalization."
keyFindings:
  - "Single-variable regression (kW vs OAT): R²=0.86, MSE=5,055"
  - "Multivariable regression (OAT, tons, occupancy): R²=0.98, MSE=1,099"
  - "24-hour training window generalizes well to full dataset (R²=0.94)"
notebookFile: "03-regression-modeling.ipynb"
renderedFile: "03-regression-modeling.html"
project: "chiller-plant-diagnostics"
projectTitle: "Chiller Plant Diagnostics"
projectSummary: "End-to-end diagnostic analysis of a central chiller plant with three embedded operational faults — from data generation through fault detection to energy waste quantification."
order: 3
---

Progressive regression modeling of chiller power consumption: from single-variable OAT regression to multivariable models with residual analysis. Tests whether a short 24-hour training window can generalize across the full operating period.
