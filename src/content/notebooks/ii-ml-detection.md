---
title: "04 — ML-Based RDII Detection"
date: "2025-11-27"
tags: ["xgboost", "lstm", "anomaly-detection", "shap", "conductivity"]
techStack: ["Python", "pandas", "numpy", "scikit-learn", "xgboost", "tensorflow", "shap", "matplotlib"]
sector: "utility"
summary: "Trains XGBoost and LSTM models for RDII prediction, performs autoencoder-based anomaly detection for I&I period classification, and validates against conductivity-based dilution analysis."
keyFindings:
  - "XGBoost and LSTM both achieve strong RDII prediction, with LSTM capturing longer temporal dependencies"
  - "SHAP analysis confirms rainfall lag and snowmelt as dominant features for inflow plants, antecedent moisture for infiltration plants"
  - "Multi-method consistency check across CCF, RDII decomposition, ML prediction, and conductivity validates detection reliability"
notebookFile: "ii-04-ml-detection.ipynb"
renderedFile: "ii-04-ml-detection.html"
project: "sewer-ii-detection"
projectTitle: "Sewer I&I Detection & Energy Impact Analysis"
projectSummary: "Multi-method detection of inflow and infiltration in municipal sanitary sewers using lag analysis, hydrograph decomposition, dilution tracing, and machine learning — with energy penalty quantification and remediation prioritization across a multi-plant collection system"
order: 4
---
