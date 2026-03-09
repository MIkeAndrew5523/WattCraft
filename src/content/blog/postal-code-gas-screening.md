---
title: "Gas Bills by Postal Code: A Screening Tool for Municipal Envelope Incentive Programs"
date: "2026-03-09"
tags: ["energy", "building-performance", "municipal", "regression", "policy"]
summary: "Using aggregated natural gas consumption data by postal code and property tax roll characteristics to identify neighbourhoods with the worst-performing building envelopes — and target retrofit incentive dollars where they'll do the most good."
draft: true
---

## The Short Version

Municipalities want to spend retrofit incentive dollars where they'll have the most impact, but they can't audit every neighbourhood. This post walks through a screening method that takes two years of natural gas consumption data aggregated by postal code, regresses it against heating degree days, normalizes by building stock characteristics from the property tax roll, and ranks neighbourhoods by thermal intensity. The output is a prioritized list of postal codes where building envelopes are underperforming — and where incentive programs are most likely to find uptake and savings.

---

## 1. The Problem: Too Many Neighbourhoods, Not Enough Budget

Every municipality running a home retrofit incentive program faces the same question: where should the money go?

The naive approach is first-come-first-served — homeowners apply, the municipality processes applications in order, incentive dollars flow to whoever fills out the paperwork first. The problem is that self-selection bias dominates: early adopters with newer homes and higher incomes apply first, while the neighbourhoods with the worst envelopes and the most to gain often have the lowest application rates. The incentive dollars end up subsidizing upgrades in areas that needed them least.

The alternative is proactive targeting — identify the neighbourhoods where building envelopes are performing worst and concentrate outreach, marketing, and incentive allocation there. But that requires knowing something about the thermal performance of buildings across the entire municipality, and nobody has the budget to audit every postal code.

This is where aggregated utility data comes in. Gas utilities routinely provide municipalities with consumption data aggregated by postal code and customer type (residential, commercial, industrial) under community energy planning agreements. It's anonymized — no individual household data — but the postal-code-level aggregates carry a strong thermal performance signal. Combine that with property tax roll data from MPAC (which every Ontario municipality already has), and you have the ingredients for a screening tool that costs almost nothing to run.

---

## 2. Data Sources

Three datasets, all either free or already available to Ontario municipalities.

### Aggregated Natural Gas Consumption

Gas utilities (Enbridge, in most of Ontario) provide annual or monthly consumption data aggregated by postal code and consumer classification. The standard breakdown is residential, commercial, and industrial. For this analysis, we filter to residential consumers only — commercial and industrial gas use is driven by process loads and operating schedules that have nothing to do with building envelopes.

Two full calendar years of monthly data gives 24 observations per postal code. That's enough for a meaningful regression, and spanning two winters captures some year-to-year weather variation. More years would be better, but utility data agreements are often limited to recent periods.

**Key fields:** postal code (FSA or full 6-character), month, total residential gas consumption (m³ or GJ), residential customer count.

### Heating Degree Days

Environment and Climate Change Canada publishes monthly HDD at the 18°C base for weather stations across the country. For a municipality served by a single regional climate, one station is sufficient. For larger regions spanning meaningful elevation or lake-effect gradients, multiple stations or area-weighted averages may be warranted.

**Key field:** monthly HDD₁₈ for the regional weather station.

### Property Tax Roll (MPAC)

The Municipal Property Assessment Corporation (MPAC) maintains property-level data for every parcel in Ontario. Municipalities have access to this data for planning purposes. The relevant fields for normalization:

- **Building footprint area** (m²) — the ground-floor area of the structure
- **Number of storeys** — to estimate total above-grade heated area
- **Structure type** — detached, semi-detached, row/townhouse, low-rise apartment
- **Basement indicator** — finished, unfinished, or none (affects heated volume estimate)
- **Property count by postal code** — to compute per-property averages

We aggregate these by postal code to produce a building stock profile: average footprint, average storeys, dominant structure type, basement prevalence, and total estimated heated volume.

---

## 3. Why Postal Code Aggregation Works (and Where It Doesn't)

Individual building data would be ideal, but privacy restrictions prevent utilities from sharing it. Postal code aggregation is the practical compromise — and it works better than you might expect for screening purposes.

Canadian postal codes in urban areas typically cover 20–40 households on a single block face or apartment building. In suburban areas, a postal code might span 10–20 detached homes of similar vintage and construction. This geographic clustering means the postal code aggregate reflects a relatively homogeneous building stock — homes built in the same era, by the same builder, with similar envelope characteristics.

The homogeneity assumption breaks down in two situations:

**Mixed-vintage postal codes.** A postal code containing both 1960s bungalows and 2015 infill townhouses will have an average thermal intensity that represents neither group well. The tax roll data helps here — if the building type and storey distributions within a postal code are bimodal, the aggregate should be flagged rather than ranked.

**Apartment-dominated postal codes.** A single high-rise apartment building can dominate a postal code's gas consumption. The per-unit normalization changes fundamentally (shared walls, stacked units, central boiler plants), and the regression slope reflects mechanical system efficiency as much as envelope performance. These postal codes should be analyzed separately or excluded from the single-family screening.

For the typical Ontario suburban municipality — where most postal codes contain 15–30 similar-vintage single-family homes — the aggregation produces a useful signal.

---

## 4. The Regression: Gas Consumption vs. HDD

The physics is the same as individual building regression, just applied at the postal code level.

For each postal code, fit an OLS regression of monthly residential gas consumption against monthly HDD:

$$
Q_{\text{gas},i} = m \cdot \text{HDD}_i + b + \varepsilon_i \tag{1}
$$

where $Q_{\text{gas},i}$ is total residential gas consumption in postal code $k$ during month $i$, $\text{HDD}_i$ is the regional heating degree days for that month, $m$ is the thermal slope (gas per HDD), and $b$ is the temperature-independent baseload (DHW, cooking, pilot lights).

The slope $m$ is the aggregate thermal response of all residential buildings in the postal code. A steeper slope means more gas consumed per degree of outdoor temperature drop — which, all else equal, means more heat loss through the collective building envelope.

But "all else equal" is doing a lot of work. A postal code with 35 large detached homes will have a steeper raw slope than one with 20 small townhouses, even if the townhouses have worse insulation. The raw slope reflects the quantity and size of buildings, not just their thermal quality. That's why normalization is essential.

### Quality Checks

Before normalization, each postal code regression should pass:

- **R² > 0.80** — gas consumption should be strongly driven by outdoor temperature for residential postal codes. Lower R² suggests non-heating gas loads, data quality issues, or mixed consumer types.
- **Positive slope** — a negative slope is physically impossible for a heating-dominated postal code.
- **Reasonable baseload** — the intercept $b$ should be a small positive number (summer gas use for DHW and cooking). Negative intercepts indicate data alignment issues. Very high intercepts may indicate commercial gas loads miscoded as residential.
- **Minimum customer count** — postal codes with fewer than 10 residential customers should be excluded (small sample, volatile aggregates).

---

## 5. Normalization: From Raw Slope to Thermal Intensity

The normalization converts the raw regression slope into a metric that reflects envelope quality independent of building stock quantity and size.

### Step 1: Per-Property Slope

Divide the postal code's regression slope by the number of residential properties:

$$
m_{\text{per-prop}} = \frac{m_k}{N_k} \tag{2}
$$

This removes the effect of having more or fewer buildings in the postal code.

### Step 2: Heated Volume Estimate

Estimate the average heated volume per property using tax roll data:

$$
V_{\text{heated}} = A_{\text{footprint}} \times (H_{\text{above}} + f_{\text{bsmt}} \times H_{\text{below}}) \tag{3}
$$

where $A_{\text{footprint}}$ is the average building footprint area, $H_{\text{above}}$ is estimated above-grade heated height (storeys × 2.7 m typical floor-to-floor), $H_{\text{below}}$ is the basement height (2.4 m typical), and $f_{\text{bsmt}}$ is the basement heating fraction — 1.0 for finished basements, 0.5 for unfinished (partial heating), 0.0 for no basement.

### Step 3: Normalized Thermal Intensity

$$
\boxed{I_k = \frac{m_{\text{per-prop},k}}{V_{\text{heated},k}}} \tag{4}
$$

Units: GJ per HDD per m³ (or equivalent). This is the postal code's normalized thermal intensity — gas consumption per unit of heating demand per unit of heated building volume. Higher values indicate more gas per degree per cubic metre — a composite signal dominated by envelope conductance but also reflecting furnace efficiency, occupancy density, thermostat behaviour, and ventilation rates.

### Step 4: Structure Type Grouping

Even after volume normalization, structure type introduces systematic bias. Detached homes have four exposed walls; semi-detached have three; row houses have two (end units) or one (interior units). Comparing a postal code of detached bungalows against one of interior row houses without accounting for this is misleading.

Group postal codes by dominant structure type before ranking. Within each group, the normalized thermal intensity is a fair comparison.

---

## 6. Ranking and Targeting

With normalized thermal intensity computed for every qualifying postal code, the targeting analysis is straightforward.

**Within each structure type group**, rank postal codes from highest to lowest $I_k$. The top quartile — the 25% of postal codes with the highest normalized thermal intensity — forms the priority targeting list.

These are the neighbourhoods where:
- Building envelopes are losing the most heat per unit of heated space
- Retrofit measures (insulation, air sealing, window replacement) are most likely to produce measurable gas savings
- Homeowners may have the most to gain from incentive programs — and the most to lose from inaction as gas prices rise

**The targeting output is a table:** postal code, dominant structure type, estimated building vintage (if available from MPAC), normalized thermal intensity, rank within group, and a flag for the priority quartile. This table feeds directly into municipal incentive program design — door-to-door outreach, targeted mailer campaigns, neighbourhood-level audit blitzes, and geographically weighted incentive allocations.

### Combining with Demographic Data

The thermal screening identifies where envelopes are worst. Overlaying census income data identifies where homeowners are least able to self-fund retrofits. The intersection — high thermal intensity and low household income — is where publicly funded incentive programs deliver the most equity value. This demographic overlay is outside the scope of the analytical methodology but is a natural extension for program design.

---

## 7. Synthetic Demonstration

The companion notebooks demonstrate the methodology on a synthetic dataset representing a mid-size Ontario municipality: 150 postal codes, 24 months of simulated residential gas consumption, and MPAC-derived building stock profiles.

The synthetic data is calibrated to reproduce the statistical properties of a real Ontario community — gas consumption ranges, HDD patterns, building stock distributions — while allowing controlled variation in the true underlying thermal performance. Because the ground truth is known by construction, the synthetic analysis can verify internal consistency and illustrate each processing step.

Key outputs from the notebooks:
- Regression quality summary (R² distribution, flagged postal codes)
- Normalization effect visualization (raw slope rank vs. normalized rank — they change substantially)
- Priority postal code maps and targeting tables
- Sensitivity analysis on normalization parameters (basement fraction, storey height assumptions)

---

## 8. Limitations

**Aggregation masks within-postal-code variation.** A high-ranking postal code likely contains a mix of well-performing and poorly-performing homes. The screening identifies the neighbourhood, not the individual building. The detailed audit that follows the screening — at the individual property level — is where building-specific recommendations emerge.

**Vintage data would help but isn't always available.** MPAC records include year of construction for many properties, but coverage is inconsistent. Where available, vintage is a powerful additional normalizer — a postal code of 1955 bungalows with high thermal intensity is a different story than one of 2005 homes with high intensity (the latter suggests construction quality issues, the former is expected).

**Furnace efficiency is a confound.** A postal code with high thermal intensity might reflect poor envelopes or old, inefficient furnaces or both. The regression slope captures the total thermal-plus-mechanical response. An area with uniformly old mid-efficiency furnaces (80% AFUE) will rank worse than the same area with high-efficiency condensing furnaces (96% AFUE), even if the envelopes are identical. This doesn't invalidate the screening — both envelope and mechanical upgrades are legitimate retrofit targets — but it means a high rank doesn't guarantee the savings are in the envelope specifically.

**Consumer type coding isn't always clean.** Small commercial accounts (home-based businesses, mixed-use buildings) sometimes appear in the residential classification. At the postal code level, a few miscoded accounts won't materially affect the regression, but a postal code dominated by a miscoded commercial load (a church, a community centre) will produce a misleading slope.

**Two years is the minimum.** A single anomalous winter (unusually mild or unusually cold) can bias the regression for postal codes where the building stock is sensitive to temperature extremes. Two years provides some smoothing; three or more would be better.

**The method identifies where, not why.** The thermal intensity metric is a screening signal, not a diagnosis. A high-ranking postal code needs site-level investigation to determine whether the issue is insulation, air leakage, windows, mechanical systems, or occupant behaviour. The screening puts the flashlight on the right neighbourhoods — the audit determines what to fix.

---

## 9. Implementation Notes

**Data request to the utility.** Frame the request under the municipality's community energy plan or climate action plan. Request monthly residential gas consumption by postal code (6-character) for the most recent 24–36 months, with customer count per postal code per month. Enbridge has a standard process for these requests under their community energy partnership framework.

**MPAC data extract.** Most Ontario municipalities have MPAC data in their GIS or property tax systems. The relevant fields are: roll number, postal code, structure type code, storey count, footprint area, and basement indicator. Aggregate by postal code before the analysis — individual property records should not leave the municipal GIS environment.

**Refresh cycle.** Run the screening annually as new gas consumption data becomes available. Year-over-year changes in a postal code's normalized thermal intensity can indicate whether retrofit programs are producing measurable aggregate improvement — a macro-level M&V signal.

**Integration with existing programs.** The targeting table can inform Enbridge Home Efficiency Rebate Plus program outreach, Canada Greener Homes Grant successor programs, municipal property tax incentive programs (like PACE financing where available), and community-level thermal upgrade campaigns.
