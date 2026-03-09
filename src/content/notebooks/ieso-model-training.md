---
title: "03 — Model Training & Selection"
date: "2025-10-16"
tags: ["xgboost", "regression", "classification", "shap", "model-selection"]
techStack: ["Python", "scikit-learn", "xgboost", "lightgbm", "shap", "matplotlib"]
sector: "utility"
summary: "Trains and compares regression and classification models for daily max demand prediction, with SHAP-based feature importance analysis."
keyFindings:
  - "XGBoost regression outperforms classification approaches by avoiding the extreme class imbalance problem"
  - "Temperature features dominate SHAP importance, followed by demand momentum and calendar features"
  - "Regression approach naturally provides uncertainty quantification via prediction intervals"
notebookFile: "ieso-03-model-training.ipynb"
renderedFile: "ieso-03-model-training.html"
project: "ieso-peak-prediction"
projectTitle: "IESO Coincident Peak Prediction"
projectSummary: "ML-driven prediction of Ontario's top-5 system demand hours for Class A Global Adjustment optimization"
order: 3
---
