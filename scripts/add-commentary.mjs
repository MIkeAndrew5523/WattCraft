#!/usr/bin/env node
// scripts/add-commentary.mjs
// Injects markdown commentary cells into .ipynb files for the website rendering.
// Run once — idempotent (replaces all cells, re-inserts commentary).

import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const NB_DIR = 'public/notebooks';

function md(source) {
  return {
    cell_type: 'markdown',
    metadata: {},
    source: Array.isArray(source) ? source : source.split('\n').map((l, i, a) => i < a.length - 1 ? l + '\n' : l),
  };
}

function readNb(filename) {
  const raw = readFileSync(join(NB_DIR, filename), 'utf-8');
  return JSON.parse(raw);
}

function writeNb(filename, nb) {
  writeFileSync(join(NB_DIR, filename), JSON.stringify(nb, null, 1), 'utf-8');
  console.log(`Updated: ${filename}`);
}

function insertAfter(cells, index, newCells) {
  cells.splice(index + 1, 0, ...newCells);
}

function findCodeCellIndex(cells, startFrom, searchString) {
  for (let i = startFrom; i < cells.length; i++) {
    if (cells[i].cell_type === 'code') {
      const src = Array.isArray(cells[i].source) ? cells[i].source.join('') : cells[i].source;
      if (src.includes(searchString)) return i;
    }
  }
  return -1;
}

// Helper: remove existing injected commentary (cells with metadata.injected === true)
function stripInjected(cells) {
  return cells.filter(c => !c.metadata?.injected);
}

function markInjected(cell) {
  cell.metadata = { ...cell.metadata, injected: true };
  return cell;
}

// ============================================================
// NB01 — Data Generation
// ============================================================
function patchNb01() {
  const nb = readNb('01-chiller-plant-data-generation.ipynb');
  nb.cells = stripInjected(nb.cells);

  // Replace the title cell
  nb.cells[0] = md([
    '# Chiller Plant Data Generation\n',
    '\n',
    '**Abriliam Consulting** — Industrial Energy Management\n',
    '\n',
    'This notebook generates a synthetic 8-week chiller plant dataset simulating realistic central plant operations for a commercial building during summer cooling season (June–July 2025). The dataset serves as a controlled environment for diagnostic training — with **three hidden operational faults** embedded in the data.\n',
    '\n',
    '### What\'s in the dataset\n',
    '- **1,344 hourly observations** across 23 columns\n',
    '- Weather drivers (outdoor air temperature, wet-bulb proxy)\n',
    '- Occupancy-driven cooling loads (weekday/weekend patterns)\n',
    '- Chilled water loop: supply/return temperatures, delta-T, flow rates\n',
    '- Condenser water loop: supply/return temperatures, cooling tower approach\n',
    '- Equipment power: chiller, tower fans, CHW pumps, CW pumps\n',
    '- Derived KPIs: kW/ton (chiller and plant-level), pumping intensity\n',
    '\n',
    '### Hidden faults (revealed later in the series)\n',
    '1. **Low delta-T syndrome** — CHW temperature differential collapses mid-series, driving excessive pump energy\n',
    '2. **Cooling tower degradation** — approach temperature drifts upward over the 8-week period\n',
    '3. **Night-time fan control bias** — tower fans run harder than necessary during low-load overnight hours\n',
  ]);

  // Find the main code cell and add commentary after it
  const mainCodeIdx = findCodeCellIndex(nb.cells, 0, 'Quick baseline visuals');
  if (mainCodeIdx >= 0) {
    insertAfter(nb.cells, mainCodeIdx, [
      markInjected(md([
        '## Baseline Visualizations\n',
        '\n',
        'The four plots above provide an initial diagnostic snapshot:\n',
        '\n',
        '**Top-left: Plant kW and Cooling Load over Time** — Total plant power consumption tracks cooling load, but the relationship shifts after early July (dashed line). This is the regime change we\'ll investigate.\n',
        '\n',
        '**Top-right: Chiller Efficiency vs Wet-Bulb** — kW/ton should increase with wet-bulb temperature (higher condensing pressure = more compressor work). The scatter shows this expected trend, but with notable outliers at low wet-bulb — a red flag.\n',
        '\n',
        '**Bottom-left: Cooling Tower Approach over Time** — Approach temperature (CW supply minus wet-bulb) shows a clear upward drift. A healthy tower maintains stable approach; rising approach signals fouling, fan degradation, or fill deterioration.\n',
        '\n',
        '**Bottom-right: CHW Delta-T vs Load** — This plot reveals the low-delta-T syndrome. At similar cooling loads, some hours show delta-T around 6°C (healthy) while others cluster near 4°C (degraded). The low-delta-T points force higher flow rates and pump energy.\n',
      ])),
    ]);
  }

  // Find export cell
  const exportIdx = findCodeCellIndex(nb.cells, 0, 'Export dataset');
  if (exportIdx >= 0) {
    insertAfter(nb.cells, exportIdx, [
      markInjected(md([
        '---\n',
        '\n',
        'The dataset is now exported as `chiller_plant_data.csv` for use in the remaining notebooks in this series. Each subsequent notebook loads this file and investigates a different aspect of the plant\'s performance.\n',
      ])),
    ]);
  }

  writeNb('01-chiller-plant-data-generation.ipynb', nb);
}

// ============================================================
// NB02 — EDA
// ============================================================
function patchNb02() {
  const nb = readNb('02-exploratory-data-analysis.ipynb');
  nb.cells = stripInjected(nb.cells);

  nb.cells[0] = md([
    '# Exploratory Data Analysis\n',
    '\n',
    '**Abriliam Consulting** — Industrial Energy Management\n',
    '\n',
    'Before building any models, we need to understand the shape and character of the data. This notebook examines the chiller plant dataset through summary statistics, time-series trends, and correlation analysis to surface anomalies and guide the diagnostic investigation.\n',
  ]);

  // After missing values / summary stats cell
  const statsIdx = findCodeCellIndex(nb.cells, 0, 'Missing values');
  if (statsIdx >= 0) {
    insertAfter(nb.cells, statsIdx, [
      markInjected(md([
        '### Data Quality Check\n',
        '\n',
        'No missing values across all 23 columns — the dataset is complete. Key observations from the summary statistics:\n',
        '\n',
        '- **Cooling load** ranges from 40 to 361 tons with a mean of 202 tons — typical part-load operation for a mid-size plant\n',
        '- **CHW delta-T** averages 5.2°C but has a wide standard deviation (0.96°C), hinting at the low-delta-T issue\n',
        '- **Plant kW/ton** ranges from 2.8 to 7.6 — the high end represents severely inefficient operation\n',
        '- **Approach temperature** averages 4.7°C, which is reasonable, but the range (2.5–9.0°C) suggests degradation over time\n',
      ])),
    ]);
  }

  // After the Plant kW, Tons, kW/Ton time series
  const timeSeriesIdx = findCodeCellIndex(nb.cells, 0, 'Plant kW, Tons, and kW/Ton');
  if (timeSeriesIdx >= 0) {
    insertAfter(nb.cells, timeSeriesIdx, [
      markInjected(md([
        '### Time-Series Overview\n',
        '\n',
        'The triple-axis time-series plot reveals several important patterns:\n',
        '\n',
        '- **Plant kW** (blue) and **Tons** (green) follow expected daily and weekly cycles — higher during occupied weekday hours, lower overnight and weekends\n',
        '- **kW/Ton** (red) spikes during low-load periods, particularly overnight. This is characteristic of a plant with significant fixed power consumption (pump minimums, tower fan base load) that can\'t scale down proportionally at low loads\n',
        '- The relationship between kW and Tons appears to shift after early July — the same cooling load requires more power\n',
      ])),
    ]);
  }

  // After SMA plot
  const smaIdx = findCodeCellIndex(nb.cells, 0, 'kW/Ton with 24-Period');
  if (smaIdx >= 0) {
    insertAfter(nb.cells, smaIdx, [
      markInjected(md([
        '### Moving Average Analysis\n',
        '\n',
        'The 240-hour (10-day) simple moving average of kW/ton shows a clear upward drift starting in early July. This long-term trend confirms that something changed in plant operations — the plant is becoming less efficient even after smoothing out weather and load variability. Weekend periods (shaded) consistently show higher kW/ton due to the part-load penalty.\n',
      ])),
    ]);
  }

  // After CW flow / kW/ton spline
  const cwFlowIdx = findCodeCellIndex(nb.cells, 0, 'CW Flow and kW/Ton');
  if (cwFlowIdx >= 0) {
    insertAfter(nb.cells, cwFlowIdx, [
      markInjected(md([
        '### Condenser Water Flow vs Efficiency\n',
        '\n',
        'Condenser water flow and chiller efficiency are correlated — higher CW flow corresponds to higher loads and generally better kW/ton. The spline smoothing helps visualize the underlying trend without hourly noise. Both metrics show seasonal variation driven by outdoor conditions.\n',
      ])),
    ]);
  }

  writeNb('02-exploratory-data-analysis.ipynb', nb);
}

// ============================================================
// NB03 — Regression Modeling
// ============================================================
function patchNb03() {
  const nb = readNb('03-regression-modeling.ipynb');
  nb.cells = stripInjected(nb.cells);

  nb.cells[0] = md([
    '# Regression Modeling & Baseline Development\n',
    '\n',
    '**Abriliam Consulting** — Industrial Energy Management\n',
    '\n',
    'This notebook builds weather-normalized regression models to establish a performance baseline for the chiller plant. The baseline allows us to separate weather-driven variation from operational changes — answering the question: *"Is the plant performing differently than expected for these conditions?"*\n',
    '\n',
    'We start with a simple single-variable regression (OAT vs chiller kW), then progress to a multivariable model incorporating load and occupancy, and finally apply **CUSUM analysis** to detect when operations changed.\n',
  ]);

  // After OAT vs chiller kW regression
  const oatRegIdx = findCodeCellIndex(nb.cells, 0, 'Chiller kW vs OAT with Regression');
  if (oatRegIdx >= 0) {
    insertAfter(nb.cells, oatRegIdx, [
      markInjected(md([
        '### Single-Variable Regression: OAT vs Chiller kW\n',
        '\n',
        'The simple linear regression of chiller power against outdoor air temperature shows a positive relationship — as expected, warmer weather drives higher chiller loads. However, the R-squared is moderate, indicating that OAT alone explains only part of the variation. Load magnitude and occupancy are also significant drivers.\n',
        '\n',
        'The scatter plot shows considerable spread around the regression line, particularly at higher temperatures. This spread represents the combined effects of varying occupancy patterns, time-of-day differences, and the operational changes we\'re investigating.\n',
      ])),
    ]);
  }

  // After multivariable regression
  const multiRegIdx = findCodeCellIndex(nb.cells, 0, 'Multivariable Regression Statistics');
  if (multiRegIdx >= 0) {
    insertAfter(nb.cells, multiRegIdx, [
      markInjected(md([
        '### Multivariable Regression: OAT + Tons + Occupancy\n',
        '\n',
        'Adding cooling load (tons) and occupancy fraction dramatically improves the model. The residual analysis shows:\n',
        '\n',
        '- **Residual plot**: Residuals are roughly centered around zero but show some heteroscedasticity (wider spread at higher predicted values). This is common in HVAC models — larger loads have more variability.\n',
        '- **Q-Q plot**: The residuals approximate a normal distribution, validating the regression assumptions.\n',
        '- **Histogram**: Roughly symmetric distribution of residuals, though with slightly heavier tails than a perfect normal.\n',
        '\n',
        'This multivariable model forms the basis for our change detection — we can now ask whether residuals shift systematically at any point in time.\n',
      ])),
    ]);
  }

  // After spline flow/temp plots
  const splineIdx = findCodeCellIndex(nb.cells, 0, 'Evaporator Pump Flow');
  if (splineIdx >= 0) {
    insertAfter(nb.cells, splineIdx, [
      markInjected(md([
        '### Hydraulic Trends\n',
        '\n',
        'The three-panel spline plot reveals the key relationships:\n',
        '\n',
        '- **CHW flow and delta-T** (top): Flow and temperature difference move inversely — when delta-T drops, flow must increase to maintain the same cooling output. This is the hydraulic signature of low-delta-T syndrome.\n',
        '- **CW flow and delta-T** (middle): Condenser-side hydraulics are more stable, tracking load as expected.\n',
        '- **OAT and kW/ton** (bottom): Outdoor temperature and efficiency are correlated, but the kW/ton trend shows drift beyond what weather alone explains.\n',
      ])),
    ]);
  }

  // After CUSUM
  const cusumIdx = findCodeCellIndex(nb.cells, 0, 'CUSUM Analysis');
  if (cusumIdx >= 0) {
    insertAfter(nb.cells, cusumIdx, [
      markInjected(md([
        '### CUSUM Change Detection\n',
        '\n',
        'The CUSUM (Cumulative Sum) chart is a powerful tool for detecting when a process shifts. We trained a baseline model on the first 24 hours, then tracked cumulative residuals for the remaining data.\n',
        '\n',
        'A flat CUSUM line means the process is behaving as the baseline predicts. A sustained upward slope means the plant is consistently consuming more energy than predicted — an operational change has occurred. The inflection point in the CUSUM identifies *when* the change happened, which can then be correlated with maintenance logs, control system changes, or equipment events.\n',
      ])),
    ]);
  }

  writeNb('03-regression-modeling.ipynb', nb);
}

// ============================================================
// NB04 — Hydraulic Regime Detection
// ============================================================
function patchNb04() {
  const nb = readNb('04-hydraulic-regime-detection.ipynb');
  nb.cells = stripInjected(nb.cells);

  nb.cells[0] = md([
    '# Hydraulic Regime Detection\n',
    '\n',
    '**Abriliam Consulting** — Industrial Energy Management\n',
    '\n',
    'This notebook investigates the condenser water loop hydraulics to determine whether the plant operated in distinct hydraulic regimes during the monitoring period. A "regime change" — such as a valve position change, pump staging difference, or bypass condition — would alter the relationship between pressure drop (delta-P) and flow, and could explain the efficiency degradation observed in earlier notebooks.\n',
    '\n',
    'We use a combination of scatter analysis, hydraulic coefficient calculation, and **Gaussian Mixture Model (GMM) clustering** to identify and classify operational regimes.\n',
  ]);

  // After DP vs tower fan spline plot
  const dpTowerIdx = findCodeCellIndex(nb.cells, 0, 'CW Hydraulics vs Fan Efficiency');
  if (dpTowerIdx >= 0) {
    insertAfter(nb.cells, dpTowerIdx, [
      markInjected(md([
        '### CW Loop Pressure vs Tower Fan Efficiency\n',
        '\n',
        'This dual-axis plot shows the condenser water loop pressure drop alongside tower fan power per ton of heat rejected. Two distinct operating bands are visible — the system appears to operate at different pressure setpoints during the monitoring period. The fan efficiency metric (kW per ton rejected) helps normalize for load variation.\n',
      ])),
    ]);
  }

  // After DP histogram
  const dpHistIdx = findCodeCellIndex(nb.cells, 0, 'Histogram of CW Loop');
  if (dpHistIdx >= 0) {
    insertAfter(nb.cells, dpHistIdx, [
      markInjected(md([
        '### Pressure Drop Distribution\n',
        '\n',
        'The histogram of CW loop delta-P reveals a **bimodal distribution** — two distinct clusters of operating pressure. This is strong evidence of a hydraulic regime change. A healthy, stable system would show a single peak that shifts with load. Two peaks suggest the system switched between configurations at some point during the monitoring period.\n',
      ])),
    ]);
  }

  // After DP vs tower fan scatter
  const dpScatterIdx = findCodeCellIndex(nb.cells, 0, 'Scatter Plot: CW Loop');
  if (dpScatterIdx >= 0) {
    insertAfter(nb.cells, dpScatterIdx, [
      markInjected(md([
        '### Pressure Drop vs Fan Power\n',
        '\n',
        'The scatter plot confirms two operating clusters. At higher differential pressures, the tower fans don\'t necessarily work harder — the excess pressure is being absorbed elsewhere in the system (possibly through a throttled valve or bypass). This is wasted pump energy.\n',
      ])),
    ]);
  }

  // After hydraulic coefficient histogram
  const kHydIdx = findCodeCellIndex(nb.cells, 0, 'Hydraulic Regimes');
  if (kHydIdx >= 0) {
    insertAfter(nb.cells, kHydIdx, [
      markInjected(md([
        '### Hydraulic Coefficient Analysis\n',
        '\n',
        'The hydraulic coefficient *k = delta-P / Q-squared* characterizes the system\'s flow resistance. In a fixed piping configuration, this coefficient should be roughly constant regardless of flow rate. A shift in *k* indicates a physical change — a valve opened or closed, a pump was staged differently, or a bypass condition changed.\n',
      ])),
    ]);
  }

  // After DP vs Q^2 scatter
  const dpQ2Idx = findCodeCellIndex(nb.cells, 0, 'two lines suggests');
  if (dpQ2Idx >= 0) {
    insertAfter(nb.cells, dpQ2Idx, [
      markInjected(md([
        '### Delta-P vs Q-Squared\n',
        '\n',
        'Plotting pressure drop against flow-squared should yield a single line for a fixed hydraulic configuration (since delta-P is proportional to Q-squared by the Darcy-Weisbach equation). The presence of **two distinct linear relationships** confirms that the condenser water system operated in two different hydraulic configurations during the monitoring period.\n',
      ])),
    ]);
  }

  // After DP over time scatter
  const dpTimeIdx = findCodeCellIndex(nb.cells, 0, 'CW Loop ΔP over Time');
  if (dpTimeIdx >= 0) {
    insertAfter(nb.cells, dpTimeIdx, [
      markInjected(md([
        '### Pressure Drop Over Time\n',
        '\n',
        'The time-series view of delta-P clearly shows when the regime change occurred — there\'s a visible step-change in the operating pressure around early July. This aligns with the efficiency degradation detected by the CUSUM analysis in Notebook 03.\n',
      ])),
    ]);
  }

  // After GMM clustering
  const gmmIdx = findCodeCellIndex(nb.cells, 0, 'GMM Elliptical Regimes');
  if (gmmIdx >= 0) {
    insertAfter(nb.cells, gmmIdx, [
      markInjected(md([
        '### GMM Clustering Results\n',
        '\n',
        'A **Gaussian Mixture Model** with two components cleanly separates the two hydraulic regimes. The point opacity represents classification confidence — darker points are confidently assigned to one regime, while lighter "bridge" points represent transitional hours.\n',
        '\n',
        'The two regimes correspond to:\n',
        '- **Low delta-P regime**: The system operating at normal differential pressure (pre-change)\n',
        '- **High delta-P regime**: Elevated differential pressure, likely due to a control setpoint change or valve position shift\n',
        '\n',
        'This unsupervised classification can be used to automatically segment operating data for regime-specific analysis and alerting.\n',
      ])),
    ]);
  }

  writeNb('04-hydraulic-regime-detection.ipynb', nb);
}

// ============================================================
// NB05 — Low Delta-T Syndrome
// ============================================================
function patchNb05() {
  const nb = readNb('05-low-delta-t-syndrome.ipynb');
  nb.cells = stripInjected(nb.cells);

  nb.cells[0] = md([
    '# Low Delta-T Syndrome Diagnosis\n',
    '\n',
    '**Abriliam Consulting** — Industrial Energy Management\n',
    '\n',
    'Low delta-T syndrome is one of the most common and costly problems in chilled water systems. When the temperature difference between supply and return water drops below design, the system must push more water to deliver the same cooling — dramatically increasing pump energy. It also degrades chiller performance by reducing evaporator heat transfer effectiveness.\n',
    '\n',
    'This notebook diagnoses low-delta-T conditions in the dataset using a combination of threshold analysis, scatter diagnostics, and efficiency segmentation.\n',
  ]);

  // After kW/ton vs WB and tons vs calculated tons scatter
  const scatterIdx = findCodeCellIndex(nb.cells, 0, 'Plant kW/Ton vs Wet Bulb');
  if (scatterIdx >= 0) {
    insertAfter(nb.cells, scatterIdx, [
      markInjected(md([
        '### Initial Scatter Diagnostics\n',
        '\n',
        '**Plant kW/ton vs Wet-Bulb Temperature**: At low wet-bulb conditions (below ~14°C), the plant should operate very efficiently since the chiller has a low lift. Instead, we see a cluster of high kW/ton points — the plant is working harder than it should when conditions are favorable. This is a hallmark of low-delta-T syndrome.\n',
        '\n',
        '**Plant Tons vs Calculated Evaporator Tons**: Comparing the load signal against the evaporator-side calculation (flow x delta-T) reveals measurement consistency. Deviations suggest either flow measurement error or genuinely degraded heat transfer.\n',
      ])),
    ]);
  }

  // After the big low-WB analysis cell
  const lowWbIdx = findCodeCellIndex(nb.cells, 0, 'Low-WB thresholds');
  if (lowWbIdx >= 0) {
    insertAfter(nb.cells, lowWbIdx, [
      markInjected(md([
        '### Low Wet-Bulb Analysis Results\n',
        '\n',
        'Isolating hours where wet-bulb temperature is below 14°C and examining the joint occurrence of:\n',
        '- **Bad efficiency** (high plant kW/ton)\n',
        '- **Low CHW delta-T** (below the 10th percentile for this subset)\n',
        '- **High CHW flow** (above the 90th percentile for this subset)\n',
        '\n',
        'The "classic signature" — all three conditions present simultaneously — identifies hours where the plant is definitively suffering from low-delta-T syndrome. The highlighted points in the kW/ton vs WB scatter plot cluster at low wet-bulb, confirming these are not weather-driven efficiency issues but hydraulic ones.\n',
        '\n',
        'The delta-T vs flow diagnostic plot (colored by kW/ton) shows the expected pattern: as flow increases and delta-T drops, efficiency degrades. The dashed threshold lines partition the space into "healthy" and "syndrome" regions.\n',
      ])),
    ]);
  }

  // After plant kW vs tons scatter
  const kwTonsIdx = findCodeCellIndex(nb.cells, 0, 'look for a power floor');
  if (kwTonsIdx >= 0) {
    insertAfter(nb.cells, kwTonsIdx, [
      markInjected(md([
        '### Power Floor Analysis\n',
        '\n',
        'The Plant kW vs Tons scatter reveals a minimum power floor — even at very low cooling loads, the plant consumes a baseline amount of energy for pumps, fans, and ancillary systems. This power floor is particularly important because it means the plant\'s kW/ton metric degrades rapidly at part-load. Combined with low-delta-T syndrome (which increases pump power), part-load hours become disproportionately expensive.\n',
      ])),
    ]);
  }

  // After inefficiency analysis
  const ineffIdx = findCodeCellIndex(nb.cells, 0, 'Inefficient hours');
  if (ineffIdx >= 0) {
    insertAfter(nb.cells, ineffIdx, [
      markInjected(md([
        '### Inefficiency Classification\n',
        '\n',
        'Flagging hours where plant kW/ton exceeds 4.0 (a generous threshold) and examining their characteristics:\n',
        '\n',
        '- Inefficient hours cluster at **low loads** — confirming the part-load penalty\n',
        '- They occur across the full range of wet-bulb temperatures, but are most concentrated at **low wet-bulb** where the plant should be performing well\n',
        '- The summary table quantifies the gap: median load during inefficient hours is significantly lower than during efficient hours, while median delta-T is also lower\n',
        '\n',
        'This analysis provides the evidence base for recommending operational changes: minimum load staging, CHW reset strategies, and pump speed optimization can all reduce the severity of low-delta-T syndrome.\n',
      ])),
    ]);
  }

  writeNb('05-low-delta-t-syndrome.ipynb', nb);
}

// ============================================================
// NB06 — Cooling Tower Performance
// ============================================================
function patchNb06() {
  const nb = readNb('06-cooling-tower-performance.ipynb');
  nb.cells = stripInjected(nb.cells);

  nb.cells[0] = md([
    '# Cooling Tower Performance Analysis\n',
    '\n',
    '**Abriliam Consulting** — Industrial Energy Management\n',
    '\n',
    'The cooling tower is the plant\'s primary heat rejection pathway. Its performance directly impacts chiller efficiency — every degree of excess approach temperature raises condenser pressure and increases compressor work. This notebook evaluates tower performance through approach temperature analysis, free cooling potential, and fan power optimization.\n',
  ]);

  // After CW dT and tons rejected spline
  const cwDtIdx = findCodeCellIndex(nb.cells, 0, 'Condenser ΔT and Tons Rejected');
  if (cwDtIdx >= 0) {
    insertAfter(nb.cells, cwDtIdx, [
      markInjected(md([
        '### Condenser Heat Rejection\n',
        '\n',
        'The condenser water delta-T and tons rejected follow expected load patterns. The tower must reject not only the building\'s cooling load but also the chiller\'s compressor heat — typically 1.2 to 1.3 times the evaporator load. Stable delta-T indicates the CW loop is sized appropriately for the load range.\n',
      ])),
    ]);
  }

  // After free cooling analysis
  const freeCoolIdx = findCodeCellIndex(nb.cells, 0, 'Free Cooling Feasibility');
  if (freeCoolIdx >= 0) {
    insertAfter(nb.cells, freeCoolIdx, [
      markInjected(md([
        '### Free Cooling Opportunity\n',
        '\n',
        'Free cooling (also called water-side economizer or strainer cycle) allows the cooling tower to directly cool the chilled water loop when outdoor conditions are cold enough — bypassing the chiller entirely. The analysis compares outdoor air temperature against the free-cooling threshold (CHW supply setpoint minus tower approach).\n',
        '\n',
        'The time-series view highlights periods where free cooling is feasible (green shading). For a summer dataset, these opportunities are limited to nighttime and early morning hours during cooler periods. In a year-round analysis, shoulder seasons would show substantially more free cooling potential.\n',
      ])),
    ]);
  }

  // After evaporator tons and efficiency
  const evapIdx = findCodeCellIndex(nb.cells, 0, 'Evaporator Tons and Chiller Efficiency');
  if (evapIdx >= 0) {
    insertAfter(nb.cells, evapIdx, [
      markInjected(md([
        '### Evaporator Performance vs Chiller Efficiency\n',
        '\n',
        'Plotting evaporator tons against chiller kW/ton over time reveals the inverse relationship between load and efficiency. During high-load periods, the chiller operates near its design point with good kW/ton. During low-load periods, fixed losses dominate and efficiency degrades. The efficiency spikes correlate with the low-delta-T syndrome identified in Notebook 05.\n',
      ])),
    ]);
  }

  // After 10h SMA triple axis
  const smaTripleIdx = findCodeCellIndex(nb.cells, 0, 'DP, CHW efficiency, and load factor');
  if (smaTripleIdx >= 0) {
    insertAfter(nb.cells, smaTripleIdx, [
      markInjected(md([
        '### Smoothed Operational Trends\n',
        '\n',
        'The 10-hour moving averages smooth out hourly noise to reveal underlying trends. The differential pressure (blue) shows a clear step-change — corresponding to the hydraulic regime shift detected in Notebook 04. Chiller efficiency (red) trends upward (worse) after the regime change, while load factor (green) follows seasonal weather patterns.\n',
      ])),
    ]);
  }

  // After approach + efficiency plot
  const approachEffIdx = findCodeCellIndex(nb.cells, 0, 'Approach Temp Area');
  if (approachEffIdx >= 0) {
    insertAfter(nb.cells, approachEffIdx, [
      markInjected(md([
        '### Tower Approach and Plant Efficiency\n',
        '\n',
        'The shaded area between CW supply temperature and wet-bulb represents the tower\'s approach — the gap the tower cannot close. A widening approach (growing shaded area) directly correlates with degraded plant efficiency (green line). This confirms the causal chain: tower degradation raises condenser water temperature, which increases chiller lift and power consumption.\n',
      ])),
    ]);
  }

  // After fan power and CW flow SMA
  const fanFlowIdx = findCodeCellIndex(nb.cells, 0, 'CW Fan Power and CW Pump Flow');
  if (fanFlowIdx >= 0) {
    insertAfter(nb.cells, fanFlowIdx, [
      markInjected(md([
        '### Fan Power and CW Flow Trends\n',
        '\n',
        'Tower fan power shows a gradual upward trend independent of CW flow, suggesting the fans are working harder to maintain (or failing to maintain) approach temperatures as the tower degrades. The fan power increase without a corresponding CW flow increase is characteristic of fouled fill or degraded fan performance.\n',
      ])),
    ]);
  }

  // After fan power 24h SMA
  const fan24Idx = findCodeCellIndex(nb.cells, 0, 'Tower Fan Power and 24-Period SMA');
  if (fan24Idx >= 0) {
    insertAfter(nb.cells, fan24Idx, [
      markInjected(md([
        '### Fan Power Daily Pattern\n',
        '\n',
        'The 24-hour SMA of tower fan power reveals the night-time control bias — fan power has a persistent overnight baseline that is higher than daytime minimums, even though cooling loads are much lower at night. This suggests an aggressive fan control schedule or a fixed-speed fan that doesn\'t modulate down sufficiently during low-load conditions.\n',
      ])),
    ]);
  }

  // After approach vs time colored by WB
  const approachTimeIdx = findCodeCellIndex(nb.cells, 0, 'Approach vs Time');
  if (approachTimeIdx >= 0) {
    insertAfter(nb.cells, approachTimeIdx, [
      markInjected(md([
        '### Approach Temperature Drift\n',
        '\n',
        'Coloring the approach time-series by wet-bulb bin normalizes for weather effects. The upward drift in approach is visible across all wet-bulb conditions — this is not simply a weather-driven phenomenon. The tower is genuinely degrading over the 8-week period, likely due to biological fouling, scale buildup, or mechanical degradation of the tower fill.\n',
        '\n',
        'The scatter plots of fan power vs approach and chiller kW/ton vs CW supply temperature quantify the cascading impact: higher approach drives higher CW supply temperature, which drives higher chiller power consumption. Each degree of excess approach costs measurable energy.\n',
      ])),
    ]);
  }

  writeNb('06-cooling-tower-performance.ipynb', nb);
}

// ============================================================
// NB07 — Plant Efficiency Summary
// ============================================================
function patchNb07() {
  const nb = readNb('07-plant-efficiency-summary.ipynb');
  nb.cells = stripInjected(nb.cells);

  nb.cells[0] = md([
    '# Plant Efficiency Summary & Energy Waste Quantification\n',
    '\n',
    '**Abriliam Consulting** — Industrial Energy Management\n',
    '\n',
    'This final notebook brings together the findings from the diagnostic series to quantify the total energy waste attributable to the identified operational faults. We classify inefficient hours by their dominant cause — chiller performance, pumping excess, or tower fan issues — and estimate the energy (MWh) tied to each fault category.\n',
    '\n',
    'This is the "so what?" notebook — translating diagnostic findings into actionable business metrics.\n',
  ]);

  // After the main efficiency analysis
  const effIdx = findCodeCellIndex(nb.cells, 0, 'Energy tied to inefficient operation');
  if (effIdx >= 0) {
    insertAfter(nb.cells, effIdx, [
      markInjected(md([
        '### Energy Waste Quantification\n',
        '\n',
        'Flagging all hours where plant kW/ton exceeds 4.0 and summing their energy consumption provides a conservative estimate of the energy tied to inefficient operation. The subsystem "blame assignment" uses dominance analysis — if a single subsystem (chiller, pumping, or tower fans) accounts for more than 50% of the plant\'s kW/ton during a bad hour, that hour is attributed to that subsystem.\n',
        '\n',
        'The bar charts show:\n',
        '- **Hours breakdown**: Which subsystem is most often responsible for inefficiency\n',
        '- **Average component share**: How the plant\'s per-ton energy consumption splits across subsystems during inefficient periods\n',
        '\n',
        'This analysis directly informs the priority of corrective actions — addressing the dominant source of waste first yields the largest savings.\n',
      ])),
    ]);
  }

  // After CW flow vs tons bad hours scatter
  const cwBadIdx = findCodeCellIndex(nb.cells, 0, 'Bad hours only: CW flow');
  if (cwBadIdx >= 0) {
    insertAfter(nb.cells, cwBadIdx, [
      markInjected(md([
        '### CW Flow During Inefficient Hours\n',
        '\n',
        'Examining condenser water flow during inefficient hours reveals a potential minimum flow constraint. The horizontal dashed line at 40 m³/h suggests a CW pump minimum — even at very low loads, the condenser water flow doesn\'t drop below this floor. This fixed flow at low loads contributes to the pumping-dominated inefficiency seen in the classification above.\n',
        '\n',
        '---\n',
        '\n',
        '## Summary of Findings\n',
        '\n',
        'Across this seven-notebook diagnostic series, we identified three distinct operational faults in the chiller plant:\n',
        '\n',
        '1. **Low delta-T syndrome** — CHW temperature differential collapsed from ~6°C to ~4.2°C around early July, forcing higher pump flows and degrading chiller evaporator performance\n',
        '2. **Cooling tower degradation** — Approach temperature drifted upward by approximately 1.5°C over the 8-week period, increasing condenser pressure and chiller power consumption\n',
        '3. **Night-time fan control bias** — Tower fans operate at elevated power during overnight hours despite minimal cooling loads\n',
        '\n',
        '### Recommended Actions\n',
        '\n',
        '| Priority | Action | Expected Impact |\n',
        '|----------|--------|----------------|\n',
        '| 1 | Investigate and correct the cause of low CHW delta-T (likely a control valve or bypass issue) | Reduce pump energy by 20-30%, improve chiller efficiency |\n',
        '| 2 | Inspect and clean cooling tower fill; check fan belt tension and blade pitch | Recover 1-1.5°C of approach, reducing chiller power |\n',
        '| 3 | Implement load-based fan speed control with overnight setback | Eliminate unnecessary fan energy during low-load hours |\n',
        '| 4 | Review CW pump minimum flow setpoint | Right-size the flow floor to actual minimum condenser requirements |\n',
      ])),
    ]);
  }

  writeNb('07-plant-efficiency-summary.ipynb', nb);
}

// ============================================================
// Run all patches
// ============================================================
patchNb01();
patchNb02();
patchNb03();
patchNb04();
patchNb05();
patchNb06();
patchNb07();

console.log('\nAll notebooks patched with commentary.');
