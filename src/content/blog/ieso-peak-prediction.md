---
title: "Predicting Ontario's Coincident Peaks: ML-Driven Forecasting for IESO Global Adjustment Optimization"
date: "2025-06-19"
tags: ["energy", "machine-learning", "utility", "demand-response"]
summary: "A machine learning framework for predicting Ontario's top-5 system demand hours under the Industrial Conservation Initiative, using weather-driven demand regression and a two-stage alert system to enable targeted load curtailment for Class A electricity customers."
draft: true
---

## The Short Version

Five hours determine your Global Adjustment bill for the next 12 months. Miss one and your Class A customer pays for it all year. Curtail on 40 false alarms and you've burned production revenue for nothing. This post walks through an ML framework I built to thread that needle — predicting Ontario's top-5 system demand peaks using 15 years of IESO data and weather-driven regression, with a two-stage alert system that catches peaks while keeping false alarms under 15 per season.

---

## 1. The $400K Question

If you manage energy costs for a Class A facility in Ontario, you already know the math. GA runs 60-70% of the total electricity bill. Even for a smaller facility — a 1.5 MW plant that opted in at the 500 kW threshold — the GA exposure from 5 peak hours can run $60K-$80K per year. Curtail to 0.3 MW during those 5 hours and you cut your Peak Demand Factor by 80%, saving $48K-$64K annually. For a 10 MW customer, the same math produces a $320K+ annual swing. All from 5 hours of operational adjustment.

The problem is timing. IESO identifies the peaks retroactively after the base period closes on April 30. You have to call them in real time. Miss one and you carry a bloated PDF for 12 months. False alarm and you've shut down production lines for nothing.

The patterns are well-known: ~90% of peaks land on hot summer weekday afternoons between 3 PM and 7 PM. But that heuristic alone triggers 30-50 curtailment days per season. And it misses the winter peaks that show up every few years — January 2014, January 2015, January 2018, February 2023 all produced top-5 hours driven by extreme cold.

This post builds a prediction system that does better. It predicts daily maximum Ontario Demand using publicly available IESO data and weather forecasts, classifies each day as RED/YELLOW/GREEN, and is backtested across multiple base periods. The goal: catch all 5 peaks with fewer than 15 false alarm days per season.

---

## 2. ICI Mechanics — The Billing Math

You probably know most of this, but the details matter for the model design.

Class A customers (>1 MW monthly peak, or >500 kW opt-in) pay GA based on their **Peak Demand Factor** — their share of total system demand during the 5 coincident peaks:

$$
\text{PDF} = \frac{\sum_{j=1}^{5} D_{\text{customer},j}}{\sum_{j=1}^{5} D_{\text{system},j}} \tag{1}
$$

Monthly GA charge is then:

$$
C_{\text{GA}} = \text{GA}_{\text{total}} \times \text{PDF} \tag{2}
$$

The PDF locks in for 12 months (July 1 through June 30), determined by peaks from the preceding base period (May 1 through April 30). GA rates have run $30-$50/MWh in recent years, and the total monthly pool can exceed $800M. Run the numbers on a 10 MW customer at full load during all 5 peaks versus curtailed to 2 MW, and you're looking at a $3M+ annual difference.

One nuance worth flagging: IESO publishes **AQEW** (Adjusted Quantity of Energy Withdrawn) that accounts for behind-the-meter generation and storage — consistently 400-900 MW lower than Ontario Demand. The model targets Ontario Demand for prediction (it's what you can observe in real time) but the financial valuation uses AQEW, since that's what actually determines billing.

---

## 3. Historical Peak Patterns

Fifteen base periods of data (2012-2025, with demand records back to 2010) establish the constraints. Here's what the patterns actually look like.

**Season:** ~90% of top-5 peaks fall in June-August, with July the most common month. September peaks show up occasionally during late-season heat events. Winter peaks are rare but real — January 2014, 2015, 2018, and February 2023 all produced top-5 hours. A system that ignores winter will eventually miss one.

**Time of day:** Peaks cluster tightly in the HE 16-18 window (3 PM to 6 PM EST). HE 17 is the single most frequent peak hour. Occasional early peaks (HE 12-14) show up during extreme heat when A/C load ramps ahead of schedule.

**Day of week:** Every top-5 peak in the historical record has occurred on a weekday. Zero weekend or statutory holiday peaks — ever. This is the strongest structural constraint in the dataset. Any model alerting on a Saturday is broken.

**Demand range:** Annual #1 peaks span roughly 20,900 MW (mild 2017-18 summer) to 24,900 MW (2013-14 sustained heat). The trend is flat to slightly declining despite population growth — embedded generation (behind-the-meter solar, CHP, distributed gen) has grown from ~260 MWh of peak-hour contribution in 2010 to ~1,400 MWh by 2024, structurally suppressing metered peaks. The model needs to account for this drift or it'll over-predict and flood you with false alarms.

**Temperature-demand relationship:** Approximately linear above ~22°C, with each additional degree driving 300-500 MW of additional peak demand depending on humidity and system conditions. Below 22°C, A/C load is negligible and the relationship flattens out.

**The displacement threshold — this is the key insight.** The real question isn't "what will today's demand be?" — it's "will today's demand beat the current 5th-highest peak in the running tracker?" Early in the season the threshold might be 19,000 MW; by late August it could be 22,500 MW. The model doesn't need perfect demand prediction — it needs to beat a moving target. That's a fundamentally easier problem, and it gets easier as the season progresses and the threshold stabilizes.

---

## 4. Data Sources

Two primary sources — IESO demand records and Open-Meteo weather — both free and public. The engineering challenge isn't access, it's alignment.

**IESO hourly demand** is published at `reports-public.ieso.ca/public/Demand/PUB_Demand_[YYYY].csv`, one file per calendar year. Columns: Date, Hour (hour-ending, EST), Market Demand, Ontario Demand. Coverage back to 2002. First three rows are metadata (backslash-prefixed) — skip them during parsing.

**IESO ICI demand** in base-period format is at `reports-public.ieso.ca/public/ICIDemand/PUB_ICIDemand.csv`, organized May 1 through April 30. The 2021 base period file is effectively empty and needs to be reconstructed from calendar-year files.

**IESO peak tracker** at `reports-public.ieso.ca/public/ICIPeakTracker/PUB_ICIPeakTracker_[YYYY].xml` gives the running top-10 peaks in XML format — this provides your real-time displacement threshold.

**Open-Meteo weather** — historical hourly data back to 2010 from `archive-api.open-meteo.com/v1/archive`, forecasts from `api.open-meteo.com/v1/forecast` with 7-day horizon. No API key required. Toronto reference point: 43.65°N, 79.38°W.

**Timestamp alignment — watch this one carefully.** IESO uses hour-ending convention in EST (they stay on EST year-round, no EDT shift). Open-Meteo uses hour-beginning in UTC. If you don't handle this correctly, your demand-weather pairs will be offset by one hour during summer — exactly when alignment matters most. The pipeline converts everything to `America/Toronto` timezone-aware pandas datetimes and handles DST transitions explicitly.

---

## 5. Feature Engineering

Every feature is here because it has a physical or operational reason to influence demand — not because a correlation search found it. The hierarchy: weather drivers first, then temporal structure, then demand momentum and peak context.

### Weather Features (Primary Drivers)

Daily max temperature ($T_{\max}$) is the strongest single predictor. But raw temperature misses the humidity effect — a 33°C day with high humidity generates substantially more A/C demand than the same temperature dry, because HVAC systems handle both sensible and latent load. The **humidex** captures this:

$$
H = T + \frac{5}{9}\left(6.11 \cdot e^{5417.7530 \left(\frac{1}{273.16} - \frac{1}{273.15 + T_d}\right)} - 10\right) \tag{3}
$$

where $T$ is dry-bulb and $T_d$ is dewpoint, both in °C.

**Cooling Degree Hours** capture cumulative heat exposure rather than just the peak:

$$
\text{CDH}_{\text{daily}} = \sum_{h=1}^{24} \max(0,\; T_h - 18) \tag{4}
$$

CDH matters because building thermal mass accumulates heat all day. By 4 PM, the cooling load reflects everything since 8 AM, not just the instantaneous temperature. Multi-day heat events amplify this — day 3 of a heat wave peaks higher than day 1 at the same afternoon temperature. A 3-day rolling CDH window and 3-day rolling average temperature both capture this lag.

### Temporal Features

Month, day of week, `is_weekday`, and `is_ontario_holiday` (Family Day, Good Friday, Victoria Day, Canada Day, Civic Holiday, Labour Day, Thanksgiving, Christmas, Boxing Day, New Year's Day). These aren't adding predictive power in the regression sense — they're adding structural constraint. If the model predicts 23,000 MW on a Saturday, the temporal features should kill that signal.

### Demand Momentum

Previous day's maximum demand is the most direct momentum signal. The 7-day rolling max provides wider context — if the system's been running hot all week, today's probability is elevated even if yesterday was slightly cooler. Morning demand at 10 AM is an intraday leading indicator available before the peak window opens.

### Peak Context Features

These are unique to the ICI problem. The current 5th-peak threshold (the displacement target), peaks accumulated so far this base period, days since last peak (peaks cluster in multi-day heat waves), and maximum demand observed so far. These tell the model what counts as a "peak" in the current base period — a moving target that tightens as the season progresses.

All features are computed with strict temporal ordering within each base period. The threshold on day $t$ uses only information through day $t-1$. No look-ahead leakage.

---

## 6. Why Regression, Not Classification

This is the most consequential design decision in the whole framework.

The naive approach is to classify each day as "peak" or "not peak." The problem: 5 peak days out of 365 is a 1.4% positive rate. A classifier that predicts "not a peak" every single day is 98.6% accurate and completely useless. SMOTE, class weighting — they help, but at this imbalance ratio you're always trading recall against precision, and you can't afford to lose either.

Regression sidesteps the problem entirely. Instead of "is this a peak day?" — predict what today's maximum demand will be:

$$
\hat{D}_{\max} = f(T_{\max},\; H,\; \text{CDH},\; \text{dow},\; \text{month},\; D_{\max,t-1},\; \ldots) \tag{5}
$$

Every day has a valid regression target. No rare events, no imbalance, no synthetic oversampling. The model learns the full demand surface from 13,000 MW winter lows to 25,000 MW summer peaks, and peak prediction falls out naturally when you compare the output against the displacement threshold.

Bonus: regression residuals give you built-in uncertainty quantification. Predicted 22,500 MW with 300 MW standard deviation against a 22,000 MW threshold? You know you're in the danger zone. Predicted 22,500 MW against a 20,000 MW threshold? High confidence — curtail.

### Alert System

The regression output converts to actionable alerts:

$$
\boxed{\text{Alert} = \begin{cases} \text{RED} & \text{if } \hat{D}_{\max} > D_{\text{5th}} + 500\,\text{MW} \\ \text{YELLOW} & \text{if } |\hat{D}_{\max} - D_{\text{5th}}| \leq 500\,\text{MW} \\ \text{GREEN} & \text{if } \hat{D}_{\max} < D_{\text{5th}} - 500\,\text{MW} \end{cases}} \tag{6}
$$

The 500 MW buffer is tunable. Narrower = more alerts, higher recall, more false alarms. Wider = fewer alerts, risk missing peaks. The asymmetry is stark: a missed peak costs 12 months of inflated GA; a false alarm costs one afternoon of curtailment. Err toward more RED alerts.

### Two-Stage Prediction

**Stage 1 (7 AM):** Morning forecast using weather forecast, previous day's demand, and peak context features. Gives operations 6-8 hours of lead time before the peak window.

**Stage 2 (noon onward, hourly):** Compares the actual demand trajectory against historical peak-day profiles. If demand at 1 PM is tracking above the 90th percentile of historical peak-day trajectories, escalate. Below the 50th percentile, de-escalate. This stage uses observed data, not forecasts — uncertainty shrinks as the peak window approaches.

---

## 7. Model Training & Selection

**Data split — by base period, not random.** Training: base periods 2010-2021 (~60 peak events, ~4,380 daily observations). Validation: 2022-2023. Test: 2024, held out entirely. Random splitting would let the model train on July 2023 and predict June 2023 — temporal leakage that inflates metrics and misrepresents real performance.

### Three approaches compared:

**Model A — Demand regression (primary).** Target: daily maximum Ontario Demand in MW.

- *Linear regression* — captures the dominant temperature-demand relationship but misses nonlinear interactions. RMSE in the 800-1,200 MW range. Useful as a floor.
- *Random Forest* — handles feature interactions and threshold effects naturally. Meaningful RMSE improvement. Feature importance output is useful for sanity checking.
- *XGBoost/LightGBM* — expected best performer. Sequential error correction focuses on residuals, handles missing values and categoricals natively. Gradient boosting consistently wins on demand prediction benchmarks with strong weather drivers.

**Model B — Peak day classification (comparison).** Direct binary classification on `is_peak_day` with balanced class weights. Included to demonstrate why regression is better: at a 1.4% positive rate, classification can't deliver high recall and manageable false alarms simultaneously.

**Model C — Expert heuristic (baseline).** Alert if forecast T_max > 30°C AND weekday AND June-August. This is what an experienced energy manager does without a model. Perfectly interpretable, completely unable to adapt to the current displacement level or heat event severity.

**What matters:** Recall — the fraction of actual peak days that get RED alerts. Missing a peak costs 12 months of inflated GA. A false alarm costs one afternoon. Prioritize recall, subject to keeping total false alarm days under ~15 per season.

**SHAP analysis** on the best-performing model confirms the expected hierarchy: temperature features dominate (max temp, humidex, CDH), followed by demand momentum (previous day's max, 7-day rolling max), then calendar features and peak context. The SHAP dependence plots show the nonlinear interaction structure — marginal impact of each additional degree increases at higher temperatures, amplified by humidity.

---

## 8. Backtesting Results

Walk-forward backtesting across base periods 2019-2024. For each period, the model trains only on prior data and predicts under the same information constraints as real-time deployment — weather forecast available at 7 AM, previous day's demand, running peak context. No future information.

**The confusion matrix tells the story.** True positives: peak days that got RED alerts. False negatives: missed peaks (the expensive ones). False positives: false alarm curtailments. The alert calendar visualization — every day color-coded RED/YELLOW/GREEN with stars on actual peak days — gives you the at-a-glance view of whether the model is working.

**3-hour window accuracy** is high given the tight HE 16-18 clustering. Identifying the day is the hard part; identifying the hour within the day is relatively straightforward once you've committed to curtailment.

**Performance varies by year.** The hard years: base periods with winter peaks (2023's February peak), mild summers with low displacement thresholds where every warm day looks like a peak, and extreme heat events with clustered peaks where precision degrades. Years with narrow margins between the 5th and 6th peak are inherently difficult — they challenge human experts too.

No model achieves perfect performance across all base periods. The relevant comparison is against the alternatives: fewer missed peaks than the heuristic, fewer false alarms than the naive "curtail every hot day" strategy, and a systematic framework you can monitor and improve year over year.

---

## 9. Financial Valuation

RMSE and recall are meaningful to us. Dollars saved are meaningful to the CFO. This section translates.

**Reference customer:** A 1.5 MW Class A facility — a small manufacturing plant or a large commercial building that's opted in at the 500 kW threshold. Baseline demand of 1.5 MW during operating hours. Curtailment capability down to 0.3 MW by shedding non-critical loads (HVAC setback, production line shutdown, lighting). Each curtailment event costs roughly $2,000-$5,000 in lost production, comfort complaints, or restart overhead.

For this facility, the GA math works like this: at full 1.5 MW load during all 5 peaks, the PDF translates to roughly $60K-$80K in annual GA charges (depending on the GA pool size that year). Curtailing to 0.3 MW during those 5 hours — an 80% reduction — cuts the PDF proportionally, saving $48K-$64K annually. Even at the lower end, that's a significant line item for a facility this size.

Four scenarios compared:

**Scenario A — No curtailment.** Full load during all peaks. Maximum GA exposure. The baseline.

**Scenario B — Model-guided curtailment.** Curtail on every RED alert. If the model triggers 15 RED alerts and catches all 5 peaks, the facility pays curtailment costs on 10 false alarm days (~$30K-$50K) but saves $48K-$64K in GA. Net positive.

**Scenario C — Perfect foresight.** Curtail only during the actual 5 peak hours. The theoretical maximum — no false alarms. Useful as a benchmark for what the model leaves on the table.

**Scenario D — Naive strategy.** Curtail every hot weekday in June-August. Catches most peaks but triggers 30-50 curtailment days. At $3,500 per event average, that's $105K-$175K in curtailment costs against $48K-$64K in GA savings — the math doesn't work for smaller facilities.

The **net curtailment value**:

$$
\boxed{V_{\text{net}} = \Delta C_{\text{GA}} - C_{\text{curtail}} \times N_{\text{alerts}}} \tag{7}
$$

The model's value over the naive strategy comes from precision. If the naive strategy triggers 40 curtailment days and the model triggers 15, that's 25 avoided curtailment events. At $3,500 each, that's $87,500 in avoided disruption. For a 1.5 MW facility, the model is the difference between ICI participation being profitable or not.

For larger facilities the numbers scale up proportionally — a 10 MW customer faces $400K+ in GA exposure, curtailment events cost $15K-$25K each, and the model's value is measured in hundreds of thousands of dollars per year.

---

## 10. Limitations & What Can Go Wrong

**Weather forecast accuracy is the binding constraint.** A 2°C forecast error shifts predicted demand by 500-1,000 MW — enough to flip a day's alert level. The 24-hour forecast for Toronto is typically within 1-2°C; a 5-day forecast can be off by 3-4°C. The two-stage design mitigates this (Stage 2 uses actual demand, not forecasts), but the morning alert that triggers curtailment planning depends on weather model skill. Ensemble forecasts (GFS, ECMWF, NAM averaged) would smooth model-specific biases.

**Structural demand shifts.** EV adoption is pushing up evening demand — if Level 2 home charging overlaps the current 4-6 PM peak window, peak timing could shift. Behind-the-meter solar suppresses afternoon net demand. New large loads (data centers, battery manufacturing, electrolyzers) could reshape the demand profile entirely. A model trained on 2010-2024 data reflects that era's demand structure. It needs periodic retraining to stay relevant.

**Embedded generation drift.** Behind-the-meter generation during peak hours has grown from ~260 MWh (2010) to ~1,400 MWh (2024). This structurally lowers the peak demand ceiling over time. If the model doesn't account for this, it over-predicts and drowns you in false alarms.

**Regulatory risk.** The 5-peak structure, base period timing, and Class A thresholds are all policy decisions that can change. A shift to 10 peaks or monthly coincident peaks would alter the problem fundamentally. The framework adapts (change the displacement target), but calibration would need a full refresh.

**Retraining cycle:** Retrain annually after each base period closes on May 1. The May 1 to June 1 window — before the first likely summer peak — is the natural maintenance period. Monitor throughout the season for forecast bias drift or demand pattern deviations from unexpected load changes.

**The real deployment challenge isn't technical.** A Flask/FastAPI service with scheduled data pulls, a joblib model artifact, and email/SMS/Slack webhooks is straightforward to build. The hard part is organizational: getting operations teams to trust the alerts, establishing curtailment procedures, and managing the friction of shutting down production lines based on a model's recommendation. That's a change management problem, not an engineering problem.
