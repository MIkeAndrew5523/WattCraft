---
title: "Chiller Plant Diagnostics"
date: "2025-08-26"
tags: ["chiller-plant", "fault-detection", "energy-diagnostics", "regression", "HVAC"]
techStack: ["Python", "numpy", "pandas", "matplotlib", "scipy", "scikit-learn"]
sector: "industrial"
summary: "End-to-end diagnostic analysis of a central chiller plant with three embedded operational faults — from data generation through fault detection to energy waste quantification."
scope: "A 7-notebook diagnostic case study analyzing a central chiller plant serving a commercial building. The project starts from raw operational data (temperatures, flows, power consumption) and works through exploratory analysis, regression modeling, hydraulic regime detection, fault isolation, cooling tower performance assessment, and a final plant efficiency summary. The goal is to demonstrate a repeatable diagnostic workflow that identifies hidden operational faults, quantifies their energy impact, and prioritizes corrective actions."
data: "A synthetic 8-week hourly dataset (1,344 data points) simulating a central chiller plant during a June-July cooling season. The dataset includes 23 columns covering chilled water supply/return temperatures, condenser water temperatures, flow rates, compressor and auxiliary power consumption, outdoor air temperature, building occupancy, and derived KPIs (COP, kW/ton, delta-T). Three operational faults were deliberately injected into the data to simulate real-world degradation: low-delta-T syndrome on the chilled water loop, cooling tower performance degradation, and a night-time condenser fan control bias."
approach: "The analysis follows a structured diagnostic sequence across seven notebooks. Data generation establishes the synthetic plant with realistic weather drivers and embedded faults. Exploratory data analysis uses scatter plots, time series, and correlation matrices to identify anomalies. Regression modeling builds weather-normalized baseline models to separate weather-driven variation from operational faults. Hydraulic regime detection identifies flow imbalances and valve behavior patterns. Low-delta-T syndrome analysis isolates the chilled water loop fault and quantifies its impact on plant capacity and efficiency. Cooling tower performance assessment evaluates heat rejection effectiveness and identifies degradation. The final notebook synthesizes all findings into a plant efficiency summary with prioritized recommendations."
outcome: "The diagnostic workflow successfully identified all three embedded faults and quantified their combined energy waste. Low-delta-T syndrome was found to reduce effective plant capacity by approximately 15-20%, forcing longer compressor runtimes and higher energy consumption. Cooling tower degradation elevated condenser water temperatures by 2-3 degrees C, reducing chiller COP by approximately 5-8%. The night-time fan bias caused unnecessary energy consumption during unoccupied hours. Combined, the faults represent an estimated 10-15% increase in total plant energy consumption — recoverable through targeted operational corrections with minimal capital investment."
keyFindings:
  - "Three hidden operational faults identified and isolated through systematic diagnostic analysis"
  - "Low-delta-T syndrome reduces effective plant capacity by 15-20%"
  - "Cooling tower degradation elevates condenser water temperatures by 2-3 deg C"
  - "Combined faults represent 10-15% excess energy consumption — recoverable through operational fixes"
  - "Weather-normalized regression models achieve R-squared > 0.85 for baseline characterization"
notebookProject: "chiller-plant-diagnostics"
---

This project demonstrates a complete chiller plant diagnostic workflow — the kind of analysis an energy manager performs when investigating why a building's cooling costs are higher than expected. Starting from raw operational data, the analysis systematically identifies, isolates, and quantifies hidden operational faults that silently waste energy.

The seven-notebook sequence mirrors the real-world diagnostic process: gather data, explore patterns, build baseline models, detect anomalies, isolate root causes, and quantify impact. Each notebook builds on the previous one, with the final summary providing actionable recommendations prioritized by energy savings potential and implementation complexity.
