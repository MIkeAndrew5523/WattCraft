---
title: "Thermal Fingerprinting: Using Heating Degree Day Regression to Prioritize Building Envelope Retrofits Across a Municipal Housing Portfolio"
date: "2025-07-08"
tags: ["energy", "machine-learning", "water-wastewater", "climate"]
summary: "A screening methodology for community housing portfolios using gas billing data and degree-day analysis to rank buildings by thermal performance and prioritize envelope retrofits."
draft: true
---

## Abstract

Municipal housing portfolios face a persistent capital planning problem: too many buildings need envelope retrofits and not enough budget exists to audit them all. This post presents a screening methodology that extracts a thermal performance signal from monthly gas billing data using heating degree day (HDD) regression, grounded in the steady-state heat loss equation. The key output is a normalized thermal slope — a composite per-building metric that reflects the combined effect of envelope conductance, mechanical efficiency, occupancy behavior, and thermostat practice — that enables defensible ranking within building archetype groups. Envelope conductance is the dominant component, but the metric cannot isolate it from these other factors. The result is a prioritized candidate list for detailed energy audits, built entirely from data already being collected.

---

## 1. Introduction

Community housing agencies across Ontario are under simultaneous pressure to reduce operating costs, cut greenhouse gas emissions, and maintain aging building stock — all with capital budgets that haven't kept pace with the need. Across a typical municipal portfolio of several hundred residential buildings spanning townhouses, semi-detached units, and low-rise apartment blocks, the question is not whether envelope retrofits are needed but which buildings should be retrofitted first.

The conventional answer is to commission detailed energy audits. A proper ASHRAE Level II audit produces excellent data — insulation R-values, air leakage rates, window U-factors, mechanical system efficiencies — but it costs $3,000 to $8,000 per building and requires trained auditors with physical access. At those unit costs, auditing the full portfolio before making capital decisions is not financially realistic. The practical alternative is to audit selectively, but selective auditing without a defensible screening criterion means relying on complaints, visual condition assessments, or institutional memory to decide which buildings get attention. That approach misses the buildings that are quietly hemorrhaging energy without generating complaints.

The core argument of this post is that the thermal performance signal needed for screening already exists in the data stream. Every building in the portfolio has monthly gas billing records stretching back years, and Environment and Climate Change Canada publishes monthly heating degree day totals for regional weather stations. The relationship between gas consumption and outdoor temperature follows directly from the physics of heat transfer through building envelopes, and that relationship is extractable through ordinary least squares regression. The slope of the resulting regression line — gas consumed per heating degree day — is a composite signal of the building's thermal and mechanical performance, dominated by envelope conductance but also reflecting furnace efficiency, occupancy behavior, and thermostat practice.

This is a screening tool, not a replacement for engineering judgment or detailed audits. It will not tell you whether a building needs attic insulation or window replacement. What it will tell you is which buildings in the portfolio are consuming the most gas per unit of thermal demand relative to their size and geometry, and therefore where a detailed audit is most likely to find actionable savings. The methodology is repeatable, defensible, and costs almost nothing to run because it uses data already being collected for billing and weather monitoring purposes.

The remainder of this post derives the method from first principles, addresses the normalization problem that makes cross-building comparison meaningful, introduces an archetype classification system for fair comparison, demonstrates the approach on a synthetic 100-building portfolio, and discusses the limitations honestly. A companion Jupyter notebook implementing the methodology against real portfolio data will be published separately.

---

## 2. Theoretical Framework

The derivation begins with the steady-state heat loss equation, which describes the rate of thermal energy transfer through a building envelope as a function of the temperature difference between inside and outside air.

$$
Q_{\text{loss}} = \underbrace{U \!\cdot\! A}_{\text{envelope conductance}} \cdot\;\Delta T \tag{1}
$$

Here, $U$ is the thermal transmittance of the envelope assembly $(\text{W/m}^2\!\cdot\!\text{K})$, $A$ is the total envelope area through which heat is lost $(\text{m}^2)$, and $\Delta T$ is the temperature difference between the indoor conditioned space and the outdoor air. The product $UA$ is the overall thermal conductance of the envelope, expressed in watts per kelvin $(\text{W/K})$. A building with poor insulation, single-pane windows, or high air leakage will have a large $UA$ product. A well-insulated, tight building will have a small one. This is the physical quantity we are trying to estimate indirectly.

Equation 1 describes instantaneous heat loss, but gas bills measure the fuel consumed to replace that lost heat over a billing period. The furnace or boiler converting gas to useful heat does so at less than 100% efficiency, so gas consumption exceeds the theoretical heat loss by the inverse of the mechanical efficiency. Introducing $\eta$ as the lumped mechanical efficiency — encompassing the appliance's AFUE rating and distribution losses through ductwork or piping — gives the gas consumption required to offset envelope losses:

$$
Q_{\text{gas}} = \frac{Q_{\text{loss}}}{\eta} = \frac{UA}{\eta} \cdot \Delta T \tag{2}
$$

For this screening methodology, $\eta$ is treated as a portfolio constant — a simplifying assumption that preserves relative ranking, not a claim that all buildings are mechanically comparable. The community housing stock under analysis consists predominantly of buildings with mid-efficiency furnaces and boilers installed between the late 1980s and early 2000s. An assumed $\eta = 0.80$ is consistent with the AFUE ratings and age of this equipment. Where the true efficiency varies within a narrow band around this value — as it does for vintage equipment of similar type — the relative ranking of buildings by thermal performance is minimally affected even if the absolute magnitude of estimated $UA$ shifts. The assumption breaks down for buildings that have received mechanical upgrades: a building with a recently installed condensing furnace ($\eta \approx 0.95$) will show a lower slope than its envelope condition alone would produce, and the methodology will under-prioritize it for envelope work. Section 8 addresses this limitation and its practical mitigation.

To move from instantaneous heat loss to seasonal gas consumption, the temperature difference $\Delta T$ must be integrated over the heating season. This is precisely what heating degree days represent. The HDD total for a given period is the cumulative sum of the difference between a base temperature (representing the indoor setpoint minus internal heat gains) and the mean daily outdoor temperature, counted only on days when the outdoor temperature falls below the base:

$$
\text{HDD} = \sum_{d=1}^{N} \max\!\bigl(T_{\text{base}} - T_{\text{outdoor},\,d}\,,\; 0\bigr) \tag{3}
$$

The Canadian residential standard uses a base temperature of $18\,°\text{C}$, reflecting the assumption that a building with a $21\,°\text{C}$ thermostat setpoint receives approximately $3\,°\text{C}$ of "free heat" from occupants, lighting, appliances, and solar gains. This is a standardized proxy, not a building-specific truth — the actual balance point at which a particular building begins requiring heating depends on its internal gains from occupancy density, appliance loads, solar exposure, and the building's own thermal mass. For a relatively homogeneous residential portfolio where these factors are broadly similar across buildings, the fixed $18\,°\text{C}$ base produces consistent results. For portfolios with highly variable occupancy densities or mixed-use buildings, the fixed base temperature introduces additional ranking uncertainty, addressed in Section 8. Using Environment and Climate Change Canada's published monthly HDD values at the $18\,°\text{C}$ base, the seasonal gas consumption for a building becomes:

$$
Q_{\text{gas,seasonal}} = \frac{UA}{\eta} \cdot \text{HDD} + \underbrace{b}_{\substack{\text{baseload} \\ \text{(DHW, cooking)}}} \tag{4}
$$

The constant $b$ captures temperature-independent gas loads — domestic hot water heating, cooking, pilot lights — that appear on the gas bill regardless of outdoor temperature. These loads are approximately constant month-to-month and therefore appear as an additive offset rather than a term that scales with HDD.

Equation 4 maps directly to the standard linear regression form:

$$
Q_{\text{gas}} = m \cdot \text{HDD} + b \tag{5}
$$

where the slope $m$ and intercept $b$ are estimated by ordinary least squares from monthly observations. Comparing Equations 4 and 5 yields the key identity:

$$
\boxed{\;m = \frac{UA}{\eta}\;} \tag{6}
$$

The regression slope $m$ — an empirically estimated quantity derived from billing data and weather records — is physically interpretable as the building's overall envelope conductance divided by its mechanical efficiency. A steep slope means the building consumes more gas for each additional degree day of heating demand. A shallow slope means it does not.

A necessary caveat on what the slope actually captures: Equation 6 presents $m = UA/\eta$ as a clean two-parameter identity, but in practice the slope absorbs everything that affects gas consumption per degree day — not just envelope conductance and furnace efficiency. Thermostat setpoint behavior, occupancy density, ventilation practices, meter scope (whether the meter captures only space heating or also serves other gas loads), and even the building's solar exposure all contribute to the observed slope. The methodology cannot separate these effects from billing data alone. What it produces is a composite thermal-performance signal where envelope conductance is the dominant component but not the only one. This is a feature of the screening context, not a deficiency: buildings with high composite thermal demand — regardless of which component is driving it — are the buildings most likely to yield actionable findings under detailed audit. The screening identifies where to look; the audit determines what to fix.

The intercept $b$ is not discarded. It represents temperature-independent gas consumption and is a useful diagnostic in its own right — an unusually high intercept may signal excessive DHW consumption, gas-fired amenities, or metering issues. However, $b$ does not participate in the envelope performance ranking. It is a separate analytical dimension reserved for secondary investigation.

---

## 3. The Normalization Problem

The regression slope $m$ contains the thermal signal, but comparing raw slopes across buildings of different sizes produces misleading rankings. Consider two buildings with identical envelope quality — the same insulation, the same windows, the same air leakage rate per unit area. The larger building will have a steeper slope simply because it has more envelope area losing heat. This is the size bias, and it must be removed before any cross-building comparison is meaningful.

The size bias becomes visible by expanding the $UA$ product in the slope identity. Since $UA$ is the product of average thermal transmittance and total envelope area:

$$
UA = \bar{U} \cdot A_{\text{env}} \tag{7}
$$

and substituting into Equation 6:

$$
m = \frac{\bar{U} \cdot A_{\text{env}}}{\eta} \tag{8}
$$

The slope $m$ now depends on three quantities: the average envelope U-value (the performance metric we care about), the total envelope area (a geometric property of the building), and the mechanical efficiency (treated as constant). A $200\,\text{m}^2$ townhouse and a $400\,\text{m}^2$ townhouse of identical construction quality will have slopes differing by a factor of two, purely due to size. Ranking by raw slope would penalize the larger building despite identical thermal performance.

The correction is to normalize by a quantity proportional to building size. Conditioned floor area, $A_{\text{floor}}$, is available from property assessment records and serves as a practical proxy. Dividing the slope by floor area:

$$
\frac{m}{A_{\text{floor}}} = \frac{\bar{U} \cdot A_{\text{env}}}{\eta \cdot A_{\text{floor}}} \tag{9}
$$

The ratio $A_{\text{env}} / A_{\text{floor}}$ is a geometric constant that depends on building shape — a tall, narrow building has more envelope area per unit of floor area than a squat, wide one. Defining this ratio as the shape factor $k$:

$$
k \;\triangleq\; \frac{A_{\text{env}}}{A_{\text{floor}}} \tag{10}
$$

the normalized slope simplifies to:

$$
\boxed{\;\frac{m}{A_{\text{floor}}} = \frac{\bar{U} \cdot k}{\eta}\;} \tag{11}
$$

Since $\eta$ is treated as a portfolio constant and $k$ is approximately constant within a building archetype (buildings of the same type and geometry have similar shape factors), the normalized slope $m / A_{\text{floor}}$ becomes proportional to $\bar{U}$ within each archetype group. This is the metric that enables fair comparison: it isolates the per-unit-area thermal performance of the envelope from the confounding effect of building size.

Conditioned floor area is used here rather than actual envelope area because floor area is reliably available from property assessment databases, while envelope area typically is not. The shape factor $k$ bridges the gap — it converts the floor-area normalization into an effective envelope-area normalization. The price of this convenience is that the shape factor must be approximately constant within whatever grouping is used for comparison, which motivates the archetype classification described in the next section.

One additional nuance: the normalization works well for within-archetype ranking, where $k$ is reasonably stable. Cross-archetype comparison — ranking a mid-row townhouse against a detached single, for example — introduces additional uncertainty because $k$ differs between these building types. Cross-archetype rankings can still be produced but should be interpreted with appropriate caution and explicitly flagged as carrying inter-archetype geometric uncertainty.

---

## 4. Archetype Classification and Shape Factor Assignment

The normalization described in Section 3 depends on the shape factor k being approximately constant within each comparison group. In practice, this means the building portfolio must be stratified into archetype classes before ranking. Each archetype should be internally homogeneous in geometry and exposure — meaning the buildings within a class share similar floor plans, storey counts, and numbers of exposed wall faces.

For the community housing portfolio under analysis, five archetype classes capture the relevant geometric variation:

| Archetype Code | Description | Exposed Wall Faces | Notes |
|---|---|---|---|
| TH-2S | Two-storey townhouse (mid-row) | 2 of 4 | Party walls thermally neutral |
| TH-2S-END | Two-storey townhouse (end unit) | 3 of 4 | One additional exposed gable |
| SD | Semi-detached | 3 of 4 | One shared party wall |
| DT | Detached single | 4 of 4 | Full exposure |
| APT-LR | Low-rise apartment block | Whole building | Normalize per building, not per unit |

The party wall distinction matters. A mid-row townhouse (TH-2S) has only its front and rear walls exposed to the outdoors — the side walls are shared with adjacent heated units and contribute negligible heat loss. An end unit (TH-2S-END) adds one full gable wall to the exposed envelope, increasing its shape factor k and its expected energy intensity. Pooling mid-row and end units into a single archetype would systematically bias end units toward the top of the priority list regardless of their actual envelope condition.

For the apartment block archetype (APT-LR), normalization is performed at the whole-building level rather than the per-unit level. Individual apartment units within a block share floors, ceilings, and interior partition walls with adjacent conditioned spaces, making per-unit heat loss allocation ambiguous. Where a single gas meter serves the entire building, the regression is run on total building consumption. Where individual units are metered separately, aggregation to the building level is required before regression.

With archetypes defined, envelope area must be estimated for each building. The methodology uses a two-tier approach depending on data availability and archetype regularity.

Tier 1 is preferred for archetypes with regular, repeated geometry — which describes most community housing stock. For each archetype, representative unit dimensions are measured or obtained from construction drawings for a small number of buildings, and a shape factor $k$ is computed directly. This shape factor is then applied to all buildings in the archetype. For example, if representative TH-2S units have a floor area of $93\,\text{m}^2$, an envelope area (two exposed walls plus roof plus ground floor) of $138\,\text{m}^2$, the shape factor is $k = 138 / 93 = 1.48$. This value applies to all mid-row townhouses in the portfolio, eliminating the need for individual building geometry calculations.

Tier 2 is used when archetype geometry is variable or representative dimensions are not available. In this case, envelope area is estimated from floor area and storey count using a square footprint approximation. The calculation proceeds as follows. The footprint area is estimated by dividing conditioned floor area by the number of storeys:

$$
A_{\text{fp}} = \frac{A_{\text{floor}}}{n} \tag{12}
$$

Assuming a square footprint, the perimeter is:

$$
P = 4\,\sqrt{A_{\text{fp}}} \tag{13}
$$

The exposed wall area depends on the number of exposed faces relative to the total of four possible faces, and on the ceiling height (assumed at $2.7\,\text{m}$ as a portfolio constant):

$$
A_{\text{walls}} = P \cdot h \cdot n \cdot \frac{f_{\text{exp}}}{4} \tag{14}
$$

The total estimated envelope area adds the footprint (representing the roof for top-floor exposure and the ground floor for slab-on-grade or basement losses):

$$
A_{\text{env,est}} = A_{\text{walls}} + A_{\text{fp}} \tag{15}
$$

The $2.7\,\text{m}$ ceiling height is an explicit assumption, stated here rather than buried in a calculation. For the housing stock under analysis — predominantly 1970s through 1990s construction — this is a reasonable portfolio constant. Buildings with non-standard ceiling heights (finished basements with lower clearances, for example) introduce modest error that is unlikely to materially affect ranking position.

Ranking is conducted within archetype groups first. Each building's normalized slope is compared only against other buildings of the same archetype, producing a within-archetype priority list. An optional cross-portfolio ranking can be produced by combining all archetypes, but this ranking should carry explicit caveats about inter-archetype shape factor uncertainty and should not be used as the sole basis for capital allocation decisions without engineering review.

---

## 5. The Angle Interpretation — A Communication Device

The normalized thermal slope $m / A_{\text{floor}}$ is the analytical metric, but its units — cubic metres of gas per heating degree day per square metre of floor area — are not intuitive for non-technical audiences. For presentations to municipal councils or housing boards, a geometric restatement can aid communication without altering the underlying ranking. This section describes that restatement. It adds no analytical value beyond what the normalized slope already provides — it is a visualization aid, not new analysis.

Define the thermal angle $\theta$ as:

$$
\theta \;\triangleq\; \arctan\!\left(\frac{m}{A_{\text{floor}}}\right) \tag{16}
$$

This is the angle that the building's normalized regression line makes with the horizontal axis in a plot of gas intensity versus HDD. A steep normalized slope produces a large $\theta$; a shallow slope produces a small one. Because $\arctan$ is monotonically increasing over positive real numbers, the transformation preserves rank order exactly — the building with the highest normalized slope will have the highest angle. No ties are introduced and no ordering reversals occur.

For technical audiences comfortable with regression coefficients, the normalized slope is the more direct metric. For audiences that respond better to visual and geometric language, the angle framing can be substituted without loss of ranking fidelity. In practice, presenting a bar chart of "thermal angles" ranked from steepest to shallowest communicates screening results more effectively in capital planning meetings than a chart of normalized regression coefficients, even though the two charts contain identical information.

---

## 6. Data Requirements and Regression Methodology

The methodology requires three categories of input data, all of which are typically available from existing municipal records and public weather data sources.

The first and most critical input is monthly gas billing data for each building in the portfolio. A minimum of three full years of billing history (36 monthly observations) is required to produce statistically meaningful regressions. Five to six years (60 to 72 observations) is ideal, as additional years smooth out anomalous periods — a mild winter, a boiler breakdown, a period of vacancy — and improve the stability of the slope estimate. Monthly resolution is essential. Annual gas totals, while easier to compile, are statistically inadequate: three years of annual data produces a regression with only three data points, which yields an artificially high R-squared with no meaningful confidence interval. Monthly data provides genuine variance in both gas consumption and HDD within each year, makes outlier months visible and removable, and produces R-squared values that meaningfully discriminate between well-behaved and anomalous buildings.

The second input is monthly heating degree day totals from a regional weather station. Environment and Climate Change Canada publishes monthly HDD at the 18 degrees C base for stations across the country, and these records are freely available. The weather station should be reasonably representative of the portfolio's microclimate — for a housing portfolio concentrated within a single municipality, a single weather station is generally adequate. For portfolios spanning large geographic areas, multiple stations or area-weighted averages may be appropriate.

The third input is building attribute data: conditioned floor area (from property assessment records or housing authority databases), storey count (from the same sources), and archetype classification (from records review or a brief site survey — typically a drive-by is sufficient to classify exposure and confirm storey count).

The regression itself is straightforward. For each building, an ordinary least squares (OLS) regression is run with monthly gas consumption as the dependent variable and monthly HDD as the independent variable:

$$
\underbrace{Q_{\text{gas},\,i}}_{\text{monthly gas}} \;=\; m \cdot \text{HDD}_i \;+\; b \;+\; \varepsilon_i \tag{17}
$$

OLS is a pragmatic choice for a screening model. The relationship between gas consumption and HDD is approximately linear over the heating season (following from Equation 4), and the method is computationally trivial to implement. Real buildings, however, often introduce complications that the linear model treats as residual noise: billing-period misalignment with calendar months, nonlinear behavior at temperature extremes where supplemental heating or thermostat setback strategies shift the response, changing balance points from occupancy variation, and occasional baseload shifts from equipment cycling or vacancy. OLS captures the dominant trend despite these effects, which is sufficient for screening purposes. More sophisticated regression techniques — robust regression, ridge regression, mixed-effects models — could be applied but add complexity without materially changing the screening results for well-behaved buildings. The point is that OLS is a defensible screening model, not a definitive building physics model.

Each building's regression should pass a set of quality checks before its slope is used in the portfolio ranking. An $R^2$ above 0.85 is generally achieved for buildings where gas consumption is dominated by space heating, the envelope condition is stable, and occupancy is consistent — it is a reasonable rule of thumb for well-behaved heating-dominated buildings, not a universal threshold. $R^2$ values below this level warrant investigation — common causes include substantial non-heating gas loads (a gas-fired pool heater, for example), meter scope issues (a meter serving multiple buildings or a building served by multiple meters), occupancy disruptions, or a mid-period equipment change that shifted the building's thermal signature.

Residual plots should be inspected for systematic seasonal patterns. Random scatter around zero is the expectation. A U-shaped residual pattern — where the model over-predicts consumption in shoulder months and under-predicts in deep winter — may indicate a non-linear relationship at temperature extremes, possibly due to supplemental electric heating or thermostat setback strategies. A sinusoidal residual pattern may indicate that a non-heating seasonal load (such as a gas-fired cooling absorption chiller, though these are rare in residential stock) is confounding the regression.

Negative intercepts ($b < 0$) should be flagged as physically implausible. The intercept represents temperature-independent gas consumption — DHW, cooking, pilot lights — and should be a small positive number. A negative $b$ suggests a data alignment issue (billing period dates not matching the HDD calculation period), a metering error, or a building that uses an alternative fuel for non-heating loads. Buildings with $b < 0$ should be excluded from the ranking until the data issue is resolved.

Conversely, unusually high intercepts are worth flagging as a secondary audit priority. A high $b$ indicates that the building has substantial gas consumption unrelated to outdoor temperature, which may signal an oversized or inefficient DHW system, continuous gas appliance loads, or gas consumption being metered for spaces or equipment outside the building envelope. These buildings may offer savings opportunities in non-envelope categories even if their thermal slope is unremarkable.

---

## 7. Synthetic Portfolio Analysis — 100 Buildings

To illustrate the methodology's mechanics in a controlled setting, I constructed a synthetic dataset representing a 100-building community housing portfolio in southern Ontario. The synthetic data is designed to mimic the statistical properties of a real municipal portfolio while allowing controlled variation in the parameters of interest. Because the true underlying performance of each building is known by construction, the synthetic analysis can demonstrate internal consistency and the effect of each processing step — but it does not constitute empirical validation. That requires application to real billing data with audit follow-up, which is the subject of the companion notebook.

The dataset consists of 100 buildings distributed across four archetypes (TH-2S, TH-2S-END, SD, and DT), each with 36 months of simulated gas billing data — three full calendar years. Monthly HDD values are drawn from the historical range for a southern Ontario climate zone, approximately 3,400 to 4,000 HDD per year at the 18 degrees C base, with realistic month-to-month variation reflecting the continental climate pattern of cold winters and warm summers. True normalized slopes for each building are drawn from a uniform distribution spanning a realistic performance range, from well-insulated buildings with low gas intensity to poorly insulated buildings with high gas intensity. Random noise is added to each monthly observation to simulate billing estimation variability, meter reading timing misalignment, and weather station representativeness error.

The purpose here is to walk through the mechanics — regression fitting, normalization, ranking, and the effect of size-bias correction — in a context where the answer is known, so each step can be verified against ground truth.

**Figure 1** presents regression lines for six buildings selected to span the priority range, from highest normalized slope (worst thermal performance) to lowest (best thermal performance).

*[Figure 1 — generated by companion notebook, coming soon]*
*Figure 1: Sample regression lines for six buildings spanning the priority range. Steeper slopes indicate higher gas consumption per heating degree day — the thermal fingerprint of a leakier envelope or less efficient heating system. The spread across the portfolio demonstrates the discriminating power of the method: the worst-performing building consumes roughly three to four times more gas per HDD than the best-performing building of comparable size.*

**Figure 2** shows the full 100-building portfolio ranked by normalized thermal slope in descending order.

*[Figure 2 — generated by companion notebook, coming soon]*
*Figure 2: Portfolio ranking by normalized thermal slope ($m / A_{\text{floor}}$). Each bar represents one building. The top quartile (shaded) represents the 25 buildings recommended for detailed energy audit. The distribution shows a characteristic long tail: a relatively small number of buildings account for a disproportionate share of excess gas consumption, illustrating the screening logic of the approach.*

**Figure 3** illustrates the normalization effect with a pair of scatter plots.

*[Figure 3 — generated by companion notebook, coming soon]*
*Figure 3: The normalization effect. Panel (a) plots raw regression slope $m$ against conditioned floor area, revealing a strong positive correlation — larger buildings have steeper slopes simply because they have more envelope area, not because their envelopes perform worse. Panel (b) plots the normalized slope $m / A_{\text{floor}}$ against conditioned floor area. The correlation disappears, demonstrating that the normalization removes the size bias and isolates the per-unit-area thermal performance signal.*

The synthetic results illustrate several properties of the methodology in this controlled setting. The regression fits are well-behaved: $R^2$ values exceed 0.85 for over 90% of the buildings, consistent with the expectation that monthly gas consumption in a heating-dominated residential building correlates strongly with HDD. The raw slope ranking is visibly confounded by building size (Figure 3a), illustrating the need for normalization. The normalized ranking (Figure 3b) removes this confound and produces a priority list that reflects thermal performance rather than geometry. The top quartile — the 25 buildings with the steepest normalized slopes — forms the natural candidate list for detailed audit. These buildings are not confirmed as the worst performers (regression to the mean is a real concern, discussed in Section 8), but they are the buildings where a detailed audit is most likely to yield actionable findings. Whether these patterns hold as cleanly in real portfolio data — with its messier billing records, meter scope ambiguities, and occupancy variations — is the question the companion notebook addresses.

The intercept distribution across the portfolio also provides useful secondary information. Buildings with intercepts more than two standard deviations above the portfolio mean are flagged for investigation of non-heating gas loads. In the synthetic dataset, these outliers correspond to buildings where the simulated baseload was deliberately set high, illustrating the flag's discriminating power in this controlled setting.

---

## 8. Limitations and Analytical Caveats

Every screening methodology rests on assumptions, and this one is no exception. The value of the tool depends on understanding where those assumptions hold and where they introduce uncertainty. The following limitations are addressed individually, each paired with a mitigation or contextual framing.

The mechanical efficiency $\eta$ is assumed constant across the portfolio at $0.80$. In reality, individual buildings may have undergone furnace or boiler replacements — a building that received a high-efficiency condensing furnace ($\eta \approx 0.95$) five years ago will have a lower slope than its envelope condition alone would produce, causing the methodology to under-prioritize it for envelope work. The mitigation is practical: housing authorities typically maintain equipment replacement records, and buildings with recent mechanical upgrades can be flagged and interpreted with this context. If equipment records are available, a building-specific $\eta$ can be substituted into Equation 6 to recover a corrected $UA$ estimate, though this refinement moves the analysis closer to a building-specific audit and away from the portfolio screening intent.

Occupancy is assumed stable across the analysis window. For community housing, this assumption is generally defensible — units are continuously occupied, and turnover between tenants typically involves minimal vacancy. However, extended vacancies (renovation periods, units held offline for maintenance) will suppress gas consumption during the vacancy months and flatten the regression slope, making the building appear to perform better than it does. If vacancy records are available, the affected months should be excluded from the regression. If not, buildings known to have experienced extended vacancies should be flagged and interpreted accordingly.

Thermostat setpoints are assumed consistent across the portfolio. This assumption is strongest when heating is landlord-controlled (a central boiler with a building-wide setpoint) and weakest when individual tenants control their own thermostats. A tenant who keeps their unit at $24\,°\text{C}$ will produce a steeper slope than the same unit occupied by a tenant at $19\,°\text{C}$, independent of envelope quality. In community housing with centralized heating controls, this assumption holds reasonably well. In portfolios with individual tenant control, it introduces occupant behavior noise into the ranking. This noise does not invalidate the screening — it adds variance around the true thermal performance — but it means the ranking should be understood as reflecting combined envelope-plus-behavior performance rather than envelope performance in isolation.

The HDD base temperature is fixed at $18\,°\text{C}$, the Canadian residential standard. The true balance point temperature — below which heating is required — varies with internal gains from occupants, appliances, and solar exposure. A building with high internal gains has a lower balance point and will not begin heating until outdoor temperatures drop further, producing a lower effective HDD and a flatter slope. For a relatively homogeneous residential portfolio where internal gain levels are similar across buildings, this effect is small. For mixed-use portfolios or buildings with highly variable occupancy densities, the fixed base temperature introduces additional ranking uncertainty.

Gas meter scope is assumed to capture space heating and a modest baseload (DHW, cooking, pilot lights). If a meter also serves equipment outside the building envelope — a detached garage heater, a heated swimming pool — the regression slope will be inflated by loads unrelated to envelope performance. Conversely, if space heating is partially served by electric baseboard heaters (common in Ontario as supplemental heating), the gas-based slope will understate the true thermal demand. Meter scope issues are best identified during the archetype classification step, where a brief site survey can confirm what equipment is connected to each meter.

The square footprint assumption used in Tier 2 envelope area estimation (Equation 13) introduces geometric uncertainty for buildings with non-square footprints. An L-shaped building, for example, has more perimeter per unit of floor area than the square assumption predicts, and its envelope area will be underestimated. The recommended mitigation is a sensitivity analysis: varying the estimated perimeter by plus or minus 15% and checking whether the building's ranking position changes materially. If it does, the building warrants a Tier 1 shape factor calculation using actual dimensions.

Shape factor comparison across archetypes is the most significant source of structural uncertainty in the methodology. Within an archetype group — comparing mid-row townhouses against other mid-row townhouses, for example — the shape factor $k$ is approximately constant and the normalized slope ranking is a fair comparison. Across archetype groups, $k$ varies by construction (a detached single has a higher shape factor than a mid-row townhouse), and the normalized slope reflects both envelope quality and geometric differences. Cross-archetype rankings can be produced and are useful for portfolio-level visualization, but capital allocation decisions should weight within-archetype rankings more heavily and treat cross-archetype comparisons as indicative rather than definitive.

Finally, regression to the mean is a statistical reality that affects any ranked list derived from noisy data. A building that ranks in the top quartile may be there partly because its data happened to include an unusually cold billing period, a meter reading timing anomaly, or a temporary occupancy spike that inflated its apparent slope. The correct interpretation of the ranked list is not "these are the 25 worst buildings" but "these are the 25 buildings most likely to yield findings in a detailed audit." Some of the top-ranked buildings will turn out, upon investigation, to have data anomalies rather than genuine envelope deficiencies. This is expected and acceptable — the purpose of the screening is to reduce the audit population from 100 buildings to 25, not to eliminate the need for audits entirely.

---

## 9. Recommended Workflow

The following workflow takes the methodology from data collection through capital planning integration. It is designed for an energy analyst or sustainability coordinator with access to utility billing records, property assessment data, and basic statistical software (Python with pandas and scikit-learn, R, or even a well-structured spreadsheet for small portfolios).

**Classify each building into an archetype** using property assessment records, housing authority databases, or a brief site survey. Capture building type (townhouse, semi-detached, detached, apartment block), storey count, and the number of exposed wall faces. For community housing portfolios with standardized construction, this classification can often be completed from records alone, supplemented by satellite imagery for exposure confirmation. The archetype table in Section 4 provides the recommended scheme.

**Assign a shape factor $k$** to each building. For archetypes with regular, repeated geometry (Tier 1), compute a shape factor from representative unit dimensions and apply it to all buildings in the class. For archetypes with variable geometry (Tier 2), compute the shape factor individually using the square footprint approximation in Equations 12 through 15. The ceiling height assumption of 2.7 m is applied as a portfolio constant.

**Collect monthly gas billing data** — a minimum of three years per building — aligned to monthly HDD values from the nearest representative weather station. Billing periods rarely align perfectly with calendar months, so prorate billing data to calendar months or compute HDD values matching the actual billing period dates. The latter is more accurate but requires billing period start and end dates.

**Run an OLS regression** for each building with monthly gas consumption as the dependent variable and monthly HDD as the independent variable (Equation 17). This produces a slope $m$ and intercept $b$ for each building.

**Apply quality checks.** The $R^2$ value should generally exceed 0.85 for well-behaved heating-dominated buildings. Inspect residual plots for seasonal patterns. Flag negative intercepts as physically implausible. Note unusually high intercepts as secondary audit candidates.

**Compute the normalized thermal slope.** Two normalization approaches are available depending on the intended comparison scope. For within-archetype ranking, the simpler $m / A_{\text{floor}}$ is sufficient because $k$ is approximately constant within the archetype and cancels in the relative comparison. For cross-archetype ranking, the more general $m / A_{\text{env,est}}$ should be used, with envelope area estimated from Tier 1 representative dimensions or the Tier 2 square footprint approximation. The two metrics are related through $k$ and produce equivalent within-archetype rankings, but they are not interchangeable for cross-archetype comparison where $k$ differences must be accounted for.

**Rank buildings within each archetype group** by normalized thermal slope, from highest (worst thermal performance, highest audit priority) to lowest.

**Optionally, produce a cross-portfolio ranking** combining all archetype groups. This ranking should carry explicit caveats about inter-archetype geometric uncertainty and should be presented alongside — not in place of — the within-archetype rankings.

**Flag buildings with anomalously high intercepts** (more than two standard deviations above the archetype mean) as secondary audit priorities. These may have substantial non-envelope savings opportunities in DHW, cooking, or other baseload categories.

**Define the audit candidate list.** The top quartile within each archetype group — the 25% of buildings with the highest normalized thermal slopes — forms the prioritized list for detailed energy audits. This quartile threshold is a practical default; the actual cutoff should be calibrated to the available audit budget and the number of buildings the housing authority can investigate in a given planning cycle.

**Close the loop after retrofits.** Re-run the regression using post-retrofit billing data. A reduction in the regression slope is the measurable signal that the retrofit improved the building's thermal performance. This before-and-after comparison, using the same methodology applied during screening, provides a defensible M&V framework for reporting savings to municipal councils and provincial funding agencies.

This workflow connects directly to municipal climate action planning. The ranked priority list provides an evidence base for capital improvement submissions, the normalized slopes provide a quantitative performance metric for GHG reduction target tracking, and the before-and-after regression comparison provides a verification mechanism that satisfies reporting requirements.

---

## 10. Conclusion

The thermal fingerprinting methodology described in this post extracts a building-level thermal performance signal from two datasets that every municipal housing authority already collects: monthly gas bills and regional weather records. By grounding the analysis in the steady-state heat loss equation and mapping it to a simple linear regression, the approach produces a physically interpretable metric — the normalized thermal slope — that ranks buildings by composite thermal-mechanical performance within archetype groups. The metric captures envelope conductance as its dominant component, but also reflects mechanical efficiency, occupancy behavior, and thermostat practice. The result is a prioritized candidate list for detailed energy audits, generated at negligible incremental cost.

The method does not replace professional engineering judgment. It does not tell an energy manager whether a building needs blown-in attic insulation, triple-glazed windows, or air sealing work — that determination requires a site visit, diagnostic testing, and a detailed cost-benefit analysis. What it does is answer the prior question: which buildings, out of the dozens or hundreds in the portfolio, should receive that detailed attention first? In a resource-constrained environment where auditing every building is not financially feasible, the screening step is what makes selective auditing defensible rather than arbitrary.

The methodology is low-cost because it uses existing data. It is repeatable because the regression procedure is fully specified. It is transparent because every assumption — the constant mechanical efficiency, the fixed HDD base temperature, the shape factor approximation, the ceiling height — is stated explicitly and can be tested or modified by the analyst. And it is extensible: the same regression framework that produces the screening ranking also provides the before-and-after measurement framework for verifying retrofit performance.

This positions the methodology as the first stage of a two-stage process. Stage one is screening: rank the portfolio, identify the top quartile, and direct audit resources accordingly. Stage two is detailed investigation: conduct ASHRAE-level audits on the prioritized buildings, develop scope-specific retrofit recommendations, and estimate costs and savings for capital planning submissions. The screening stage makes the audit stage efficient by concentrating it where the thermal signal is strongest.

A companion Jupyter notebook implementing this methodology against a real municipal portfolio dataset will be published as a separate post. The notebook will include the data cleaning pipeline, the regression fitting and quality-check workflow, the normalization and ranking calculations, and the visualization code for producing the figures shown in this post.
