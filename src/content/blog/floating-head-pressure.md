---
title: "Floating Head Pressure: Estimating and Verifying Compressor Energy Savings for Grocery Cold Storage Refrigeration"
date: "2026-03-07"
tags: ["refrigeration", "energy-efficiency", "m-and-v", "controls", "grocery"]
summary: "A temperature bin analysis and regression-based M&V framework for estimating and verifying compressor energy savings from floating condenser head pressure control on reciprocating rack systems with air-cooled condensers."
draft: true
---

## Abstract

Commercial refrigeration systems operating at fixed minimum condensing pressure waste compressor energy during every hour of cool and cold weather — the compressor does unnecessary work maintaining a discharge pressure that the outdoor conditions could pull down naturally. This post presents a methodology for estimating those wasted kilowatt-hours using thermodynamic analysis and the temperature bin method, then verifying actual savings post-implementation through regression-based measurement and verification aligned with IPMVP. The key output is annual compressor energy savings as a function of condensing pressure reduction across two retrofit tiers — a controls-only approach for systems with existing thermostatic expansion valves, and a full electronic expansion valve retrofit enabling deeper floating. The result is a repeatable savings estimation and verification framework applicable across commercial and industrial refrigeration.

---

## 1. Introduction

Refrigeration is the dominant electrical load in cold storage warehouses, supermarkets, ice rinks, and food processing plants — typically consuming 40% to 70% of total facility electricity. For a grocery cold storage warehouse running multiplex compressor racks around the clock, the compressor motors alone can account for the majority of the annual electricity bill. Any measure that reduces compressor power consumption by even a modest percentage translates to meaningful kilowatt-hours and dollars saved.

The legacy control strategy for most commercial refrigeration systems is fixed minimum condensing pressure. The condenser fans — whether controlled by variable frequency drives or simple staging — modulate to maintain a condensing pressure setpoint that does not change with outdoor conditions. When the outdoor air temperature drops below the point where the condenser could naturally pull the condensing pressure lower, the fans slow down or shut off entirely to prevent the pressure from falling further. The system is deliberately held at a higher condensing pressure than the weather would allow. This strategy exists for sound operational reasons: thermostatic expansion valves (TEVs) require a minimum pressure differential across the valve to feed refrigerant properly, oil return to the compressor crankcase becomes unreliable at very low compression ratios, hot gas defrost circuits need sufficient discharge pressure to function, and adequate liquid line subcooling must be maintained to prevent flash gas.

The opportunity is straightforward. Allowing the condensing pressure to float downward with outdoor ambient temperature reduces compressor work proportionally — the compressor does less work pushing refrigerant to a lower discharge pressure. The thermodynamic basis is the compression ratio: lower condensing pressure at the same evaporating pressure means a lower ratio, less work per unit of refrigerant mass flow, and higher coefficient of performance. This is not a subtle effect. On a cold January night in southern Ontario, a reciprocating compressor rack floating its condensing temperature down from $35\,\text{°C}$ to $18\,\text{°C}$ can draw 25% to 35% less power than the same rack held at the fixed setpoint.

Floating head pressure is one of the most cost-effective energy conservation measures in refrigeration — often the single highest-ROI measure available. Two implementation tiers exist depending on the expansion valve type. A controls-only retrofit works within the constraints of existing TEVs and captures moderate savings at low capital cost. A full electronic expansion valve (EEV) retrofit removes the TEV constraint and enables deeper floating across more operating hours, capturing significantly more energy at higher capital cost. Both tiers deliver measurable, verifiable savings.

This post derives the thermodynamic basis for floating head pressure savings, presents the temperature bin method for prospective savings estimation, describes both retrofit implementation tiers in practical detail, and provides a regression-based M&V framework for post-implementation verification. The worked example uses a grocery chain cold storage warehouse in southern Ontario operating reciprocating compressor racks with air-cooled condensers, but the methodology generalizes to any vapor-compression refrigeration system — industrial ammonia cold storage, supermarket multiplex racks, ice rinks, or chilled water systems with condenser water temperature reset. The condenser type (air-cooled, evaporative, or water-cooled) changes the approach temperature and the specific numbers, but the analytical framework is identical.

---

## 2. Thermodynamic Framework

The thermodynamic argument for floating head pressure is built on five relationships that connect outdoor weather to compressor power consumption. These are practical engineering relationships — not rigorous first-principles derivations — chosen because they capture the dominant physics and provide the equations needed to quantify the effect.

In any refrigeration system, the condensing temperature is not a free parameter — it is set by the temperature of the cooling medium entering the condenser plus the approach temperature required to drive heat transfer across the condenser surface:

$$
T_{\text{cond}} = T_{\text{amb}} + \Delta T_{\text{approach}} \tag{1}
$$

The approach temperature $\Delta T_{\text{approach}}$ is the temperature difference between the condensing refrigerant and the cooling medium entering the condenser. For air-cooled condensers, the cooling medium is outdoor dry-bulb air, and typical approach temperatures are $6\text{--}8\,\text{°C}$ ($10\text{--}15\,\text{°F}$) above dry-bulb at rated airflow. For evaporative condensers, the relevant ambient condition is wet-bulb temperature, with approaches of $6\text{--}8\,\text{°C}$ ($10\text{--}15\,\text{°F}$) above wet-bulb. For water-cooled shell-and-tube condensers, approach temperatures are tighter — $3\text{--}6\,\text{°C}$ ($5\text{--}10\,\text{°F}$) above entering water temperature. The approach temperature is a function of condenser surface area, fouling condition, and airflow or water flow rate. It is not constant, but for a given condenser operating at rated conditions, it is stable enough to treat as a parameter.

The compression ratio determines how hard the compressor works:

$$
CR = \frac{P_{\text{cond}}}{P_{\text{evap}}} \tag{2}
$$

Both pressures are absolute. The condensing pressure $P_{\text{cond}}$ and evaporating pressure $P_{\text{evap}}$ are determined by their respective saturation temperatures through the refrigerant's pressure-temperature relationship — available from refrigerant property tables, manufacturer software, or the Antoine equation. For any given refrigerant, higher condensing temperature means higher condensing pressure, which means a higher compression ratio at the same evaporating condition. The compression ratio is the fundamental driver of compressor work — it determines the pressure rise the compressor must deliver on every stroke.

The coefficient of performance captures the efficiency of the entire refrigeration cycle:

$$
\text{COP} = \frac{Q_{\text{evap}}}{W_{\text{comp}}} \tag{3}
$$

Here $Q_{\text{evap}}$ is the refrigeration effect — the useful cooling delivered at the evaporator — and $W_{\text{comp}}$ is the compressor shaft power. A higher COP means more cooling per unit of compressor work. The COP is not a fixed property of the equipment; it varies continuously with operating conditions.

The practical relationship connecting ambient conditions to system efficiency expresses the COP as a function of the operating temperatures:

$$
\text{COP} \approx \frac{T_{\text{evap}}}{T_{\text{cond}} - T_{\text{evap}}} \times \eta_{\text{comp}} \tag{4}
$$

Temperatures here are in absolute units — Kelvin or Rankine. The term $\eta_{\text{comp}}$ is the compressor isentropic efficiency, typically 0.60 to 0.75 for semi-hermetic reciprocating compressors depending on the compression ratio and operating point. This expression is a simplification. It applies the Carnot COP structure, scaled by a single efficiency factor, to capture the dominant trend — as $T_{\text{cond}}$ increases, the denominator $T_{\text{cond}} - T_{\text{evap}}$ grows, and the COP degrades. The compressor works harder per unit of cooling delivered.

A necessary caveat: Equation 4 is a conceptual framework for understanding *why* floating head pressure reduces compressor power. It is not a predictive model for actual compressor performance. Real compressor power consumption depends on manufacturer-specific volumetric efficiency curves that degrade nonlinearly at high compression ratios, superheat and subcooling conditions at the compressor suction and discharge, valve timing losses in reciprocating machines, motor efficiency variation with loading, and heat transfer effects within the compressor shell. Published manufacturer performance maps — compressor kW and capacity as functions of saturated suction and saturated discharge temperatures at AHRI 540 standard rating conditions — are the appropriate basis for savings calculations. Equation 4 explains the direction and approximate magnitude of the effect; the polynomial fit to manufacturer data in Equation 8 does the actual work in the bin analysis.

Compressor power follows directly:

$$
W_{\text{comp}} = \frac{Q_{\text{evap}}}{\text{COP}} \tag{5}
$$

For a given refrigeration load $Q_{\text{evap}}$ — set by the facility's cooling demand, not by the condenser — lower $T_{\text{cond}}$ produces a lower compression ratio, higher COP, and lower $W_{\text{comp}}$. This is the thermodynamic basis for floating head pressure savings: every kilowatt-hour saved by this measure traces back to the reduction in condensing pressure at constant evaporating conditions.

At floating head pressure, the condenser fans typically run at higher speed — or more fans stage on — to reject heat at a lower condensing temperature, increasing condenser fan energy consumption. The compressor savings far exceed the fan penalty in virtually all practical operating conditions, because compressor motors are typically 70% to 85% of total rack power while condenser fan motors are 5% to 15%. The net energy balance is addressed quantitatively in Section 6.

---

## 3. Fixed vs. Floating — The Control Strategy

The energy savings opportunity becomes concrete when you examine what the control system is actually doing under each strategy — and why fixed head pressure was the default for so long.

Under fixed head pressure control, the condenser fan speed (via VFDs) or fan staging is controlled to maintain a minimum condensing pressure setpoint year-round. On a design summer day when the outdoor air is $33\,\text{°C}$ and the condensing temperature needs to be $40\,\text{°C}$, the fans run at full speed to reject heat across the $7\text{--}8\,\text{°C}$ approach. On a winter day when the outdoor air is $-10\,\text{°C}$, the condenser could easily pull the condensing temperature down to $-2\,\text{°C}$ or lower — but the control system will not allow it. The fans slow down or shut off entirely to prevent the condensing pressure from dropping below the setpoint. The system is deliberately held at a higher condensing pressure than the weather would allow, and the compressor does more work than the thermodynamics require.

Under floating head pressure control, the condensing pressure setpoint is allowed to follow the outdoor air temperature downward, subject to a system-specific minimum floor. When the outdoor air is cold, the condensing pressure drops, the compression ratio decreases, and the compressor draws less power. The condenser fans modulate to maintain the desired approach temperature above ambient rather than to hold a fixed pressure setpoint. The fans work harder to reject heat at a lower temperature differential — but the compressor savings overwhelm the fan penalty.

The minimum floor on floating head pressure is set by whichever operational constraint is most restrictive for the specific system. Four constraints define this floor, and each must be evaluated during system commissioning.

TEV pressure differential requirements are typically the binding constraint on TEV-equipped systems. Thermostatic expansion valves rely on the pressure difference between the liquid line — which is at condensing pressure minus liquid line losses — and the evaporator to drive refrigerant flow through the valve orifice. Below a minimum pressure differential, the TEV cannot feed the evaporator adequately. The result is starved evaporator coils, loss of superheat control, and unstable system operation. For most commercial TEVs on HFC refrigerants, this minimum differential corresponds to a condensing temperature approximately $8\text{--}12\,\text{°C}$ ($15\text{--}20\,\text{°F}$) above the evaporating temperature for medium-temperature circuits.

Oil return at low compression ratios is the second constraint. At very low compression ratios, the discharge gas velocity through the system piping drops, and oil that has migrated to the evaporator may not return to the compressor crankcase. This can cause compressor damage from oil starvation — a failure mode that does not announce itself gradually. Minimum compression ratios of 2.0:1 to 2.5:1 are commonly specified by compressor manufacturers to maintain adequate oil return velocity.

Hot gas defrost pressure requirements affect systems that use hot, high-pressure discharge gas to defrost evaporator coils. If the condensing pressure is too low, there is insufficient pressure differential to drive hot refrigerant through the defrost circuit, and defrost cycles become ineffective. Ice accumulation on evaporator coils degrades cooling capacity and increases the energy penalty in a different way. Systems using electric defrost do not have this constraint.

Liquid line subcooling is the fourth consideration. Adequate subcooling in the liquid line prevents flash gas formation between the condenser outlet and the expansion valve inlet. Flash gas reduces the mass flow of liquid refrigerant reaching the expansion valve and degrades system capacity. Lower condensing pressures reduce the available subcooling margin, particularly on systems with long liquid line runs or significant vertical risers.

Electronic expansion valves are the technology that removes the most restrictive constraint. EEVs use a stepper motor or pulse-width modulated solenoid to control refrigerant flow, and they operate across a much wider range of pressure differentials than TEVs. Some EEV models operate reliably with less than $1\,\text{bar}$ ($15\,\text{psi}$) of differential pressure. By replacing TEVs with EEVs, the minimum condensing temperature floor can be lowered significantly — often from $24\text{--}29\,\text{°C}$ ($75\text{--}85\,\text{°F}$) down to $15\text{--}21\,\text{°C}$ ($60\text{--}70\,\text{°F}$). Each additional degree of floating range captures more hours of cool-weather savings.

The control implementation for floating head pressure is straightforward. An outdoor air temperature sensor feeds PLC or BAS logic that computes a condensing pressure setpoint via a reset schedule — either linear or piecewise — as a function of outdoor temperature. The reset schedule has a hard minimum floor set by the most restrictive system constraint. The condenser fan VFD speed or staging logic responds to maintain the floating setpoint. On a $5\,\text{°C}$ day, the setpoint might be $13\,\text{°C}$ condensing (ambient plus $8\,\text{°C}$ approach), but the floor clamps it at $18\,\text{°C}$ for an EEV system. The fans modulate to hold $18\,\text{°C}$ condensing, and the compressor draws significantly less power than it would at the $35\,\text{°C}$ fixed setpoint.

---

## 4. Savings Estimation — The Temperature Bin Method

The temperature bin method is the core analytical tool for estimating annual energy savings from floating head pressure. It takes the thermodynamic relationships from Section 2 and applies them across an entire year of weather data to produce a defensible, site-specific savings estimate. The approach is conceptually simple: divide the year's hourly outdoor temperatures into discrete bins, calculate the compressor power difference between the fixed and floating scenarios at each bin's temperature, multiply by the hours spent in that bin, and sum the results.

The analysis begins with TMY weather data for the facility location. TMY — Typical Meteorological Year — data provides 8,760 hourly outdoor dry-bulb temperatures representing a statistically typical year, constructed from long-term weather records. For Canadian locations, the appropriate dataset is CWEC (Canadian Weather for Energy Calculations), available from Environment and Climate Change Canada. For US locations, TMY3 data from the National Solar Radiation Database serves the same purpose. TMY data provides a representative annual weather distribution rather than any single year's actual weather, which makes the savings estimate reproducible and defensible for project justification.

The hourly temperatures are binned into discrete intervals. A bin width of $3\,\text{°C}$ (approximately $5\,\text{°F}$) provides adequate resolution without generating excessive computation. For each bin $i$, the bin midpoint temperature $T_{\text{amb},i}$ and the number of hours $h_i$ that the outdoor temperature falls within that bin over the 8,760-hour year are recorded. The sum of all bin hours must equal 8,760 as a basic consistency check.

For each bin, the condensing temperature is calculated under both the fixed and floating scenarios. For the fixed head pressure baseline, the condensing temperature is the greater of the ambient-plus-approach temperature and the current fixed setpoint:

$$
T_{\text{cond,fixed}} = \max(T_{\text{amb},i} + \Delta T_{\text{approach}},\; T_{\text{cond,setpoint}}) \tag{6}
$$

For the floating head pressure scenario, the same calculation applies but with the lower floating floor replacing the fixed setpoint:

$$
T_{\text{cond,float}} = \max(T_{\text{amb},i} + \Delta T_{\text{approach}},\; T_{\text{cond,floor}}) \tag{7}
$$

In the worked example, $T_{\text{cond,setpoint}}$ is $35\,\text{°C}$ — the current fixed condensing temperature for a typical grocery system on R-448A. The floating floor $T_{\text{cond,floor}}$ is $27\,\text{°C}$ for the TEV-constrained Tier 1 scenario and $18\,\text{°C}$ for the EEV-enabled Tier 2 scenario. The condenser approach temperature $\Delta T_{\text{approach}}$ is $8\,\text{°C}$ for the air-cooled condenser at rated airflow.

Compressor power at each bin's condensing temperature is calculated from manufacturer performance data, which is published as a function of saturated suction temperature and saturated discharge temperature. For a given evaporating temperature, a second-order polynomial fit in condensing temperature is typically adequate:

$$
W_{\text{comp},i} = f(T_{\text{cond},i},\; T_{\text{evap}}) \tag{8}
$$

The polynomial form $W_{\text{comp}} = a_0 + a_1 \cdot T_{\text{cond}} + a_2 \cdot T_{\text{cond}}^2$ captures the nonlinear relationship between condensing temperature and compressor power. Alternatively, the COP-based calculation from Equations 4 and 5 can be used directly, with the compressor isentropic efficiency $\eta_{\text{comp}}$ set to a representative value for the specific compressor type.

The power reduction per bin is the difference between the fixed and floating scenarios:

$$
\Delta W_i = W_{\text{comp,fixed},i} - W_{\text{comp,float},i} \tag{9}
$$

Converting to kilowatt-hours by multiplying by the bin hours:

$$
\Delta E_i = \Delta W_i \times h_i \tag{10}
$$

Summing across all bins gives the annual savings:

$$
\boxed{\Delta E_{\text{annual}} = \sum_{i=1}^{N} \Delta W_i \times h_i} \tag{11}
$$

This result can be expressed as annual kWh saved, as a percentage of baseline compressor energy, or as annual dollar savings at the facility's blended electricity rate.

Savings only accrue in bins where $T_{\text{amb},i} + \Delta T_{\text{approach}} < T_{\text{cond,setpoint}}$ — that is, hours when the weather is cool enough that the condenser could achieve a lower condensing temperature than the current fixed setpoint allows. In warm-weather bins where the ambient-plus-approach temperature exceeds the fixed setpoint, both scenarios produce the same condensing temperature and $\Delta W_i = 0$. For a grocery system in southern Ontario with a $35\,\text{°C}$ fixed setpoint and $8\,\text{°C}$ approach, savings begin accumulating whenever the outdoor temperature drops below $27\,\text{°C}$ — which is the vast majority of the year.

---

## 5. System-Specific Considerations

The worked example in this post uses a grocery cold storage warehouse with reciprocating compressor racks and air-cooled condensers, but the floating head pressure methodology applies across the full range of vapor-compression refrigeration systems. The thermodynamics do not care about the application — the relationships between condensing pressure, compression ratio, and compressor power hold regardless of what is being cooled. What changes between system types are the condenser approach temperatures, the specific operational constraints, and the magnitude of the opportunity.

Industrial ammonia systems in cold storage and food processing facilities typically use screw compressors with evaporative condensers. The existing fixed minimum condensing pressure is often $1,034\text{--}1,276\,\text{kPa}$ ($150\text{--}185\,\text{psig}$), corresponding to approximately $29\text{--}38\,\text{°C}$ saturated condensing temperature for ammonia. The connected compressor loads on these systems are large — $150\text{--}1,500\,\text{kW}$ ($200\text{--}2,000+\,\text{HP}$) — which means even modest percentage savings translate to significant absolute kWh reductions. Ammonia's thermodynamic properties amplify the COP improvement from reduced condensing pressure compared to HFC refrigerants, and oil management considerations differ fundamentally. Ammonia is immiscible with mineral oil, so oil separators and dedicated oil return systems handle lubrication independently of compression ratio. This removes one of the constraints that limits floating range on HFC systems.

Commercial DX systems in supermarkets, convenience stores, and restaurants use scroll or reciprocating compressors in multiplex rack configurations with air-cooled condensers. These systems typically operate on HFC or HFO refrigerants — R-404A, R-448A, R-449A, R-407A, or increasingly R-454C as the industry transitions to A2L refrigerants. The expansion valve type — TEV or EEV — determines the minimum floating setpoint, and this is the primary variable differentiating Tier 1 from Tier 2 retrofits. Multiplex racks add a layer of complexity because multiple suction groups — medium-temperature and low-temperature — share a common discharge header and condenser. The floating strategy must satisfy the most restrictive circuit, which is typically the medium-temperature group where the TEV pressure differential requirement is tightest relative to the evaporating temperature. Defrost strategy matters too: hot gas defrost systems impose a minimum discharge pressure requirement that electric defrost systems do not.

Ice rinks and arenas operate with ammonia or synthetic refrigerant systems and carry a year-round refrigeration load with strong ambient temperature variation — making them ideal candidates for floating head pressure. The refrigeration system maintains the ice sheet at a constant temperature regardless of outdoor conditions, so the load is effectively constant and the savings are purely a function of the reduced condensing temperature during cool and cold weather. Ice quality concerns at very low condensing pressures — specifically, refrigerant flow stability through the extensive ice sheet piping network — may set a practical floor above the theoretical minimum. These are often simple systems with one or two compressors, making implementation straightforward.

Chilled water systems in building HVAC represent the direct analog. For water-cooled centrifugal or screw chillers, condenser water temperature reset is the chiller equivalent of floating head pressure. Reducing the condenser water supply temperature from the cooling tower lowers the chiller's condensing pressure and improves COP through exactly the same thermodynamic mechanism described in Section 2. The cooling tower approach temperature and outdoor wet-bulb conditions determine the floor. Many modern chillers support aggressive condenser water reset natively, but the methodology in this post applies directly to estimating savings from expanding the reset range or implementing it on older systems that currently operate at fixed condenser water temperatures.

---

## 6. Retrofit Implementation — TEV Systems vs. EEV Upgrades

Implementing floating head pressure on an existing refrigeration system is a system-level control change, not simply a setpoint adjustment. Lowering the condensing pressure shifts the operating envelope for every component on the high side of the system — compressors, condenser, receiver, liquid lines, and expansion devices all experience different pressures, temperatures, and refrigerant flow conditions than they were originally commissioned at. A successful implementation must account for these interactions.

Liquid line stability is the first system-level concern. At lower condensing pressures, the pressure drop available to drive liquid refrigerant from the condenser through the liquid line to the expansion valves is reduced. On systems with long liquid line runs — common in grocery cold storage where the machine room may be 30 meters or more from the farthest display case — or significant vertical risers, the reduced driving pressure can produce flash gas in the liquid line before the refrigerant reaches the expansion valve. Flash gas reduces mass flow to the evaporator, starves the coil, and degrades capacity. Liquid line pressure drop calculations should be revisited at the proposed minimum condensing temperature, and mechanical subcoolers or liquid-to-suction heat exchangers may be required for Tier 2 retrofits with aggressive floating floors.

High-side receiver behavior changes with floating head pressure. In systems equipped with a receiver between the condenser and the liquid line, the receiver serves as a buffer for charge migration as the condensing pressure varies. Under fixed head pressure, the charge distribution is relatively stable. Under floating head pressure, refrigerant migrates between the condenser, receiver, and liquid line as pressures shift — more charge resides in the condenser at lower pressures because the refrigerant density decreases and the condenser volume must hold the same mass at a lower density. Systems with marginal receiver capacity or inadequate total charge may experience operational instability at the extremes of the floating range. Charge optimization should be part of any floating head pressure commissioning.

Rack control logic — the compressor staging and capacity control algorithms — may need recalibration. Staging algorithms tuned for fixed head pressure assume a relatively stable discharge condition and manage suction pressure by staging compressors on and off. Under floating head pressure, the discharge pressure varies significantly with ambient temperature, which changes the individual compressor power draw and the effective capacity per staged compressor. On some rack controllers, the staging hysteresis and timing parameters need adjustment to avoid short-cycling at the new operating conditions. This is a controls tuning task, not a hardware change, but it requires attention during commissioning.

Two implementation paths exist, determined primarily by the expansion valve type installed at the evaporators. Both tiers deliver measurable compressor energy savings. The difference is how far down the condensing temperature can float and how much capital is required.

Tier 1 is the controls-only retrofit for systems with existing TEVs. The mechanical hardware stays in place — no expansion valves are replaced. The implementation involves lowering the condensing pressure setpoint to the minimum the installed TEVs can tolerate, which is system-specific but typically corresponds to a condensing temperature floor of approximately $24\text{--}29\,\text{°C}$ ($75\text{--}85\,\text{°F}$) for grocery medium-temperature applications. An outdoor air temperature reset schedule is programmed into the PLC or BAS: as outdoor temperature drops below the point where the current fixed setpoint is naturally achievable, the condensing pressure setpoint drops linearly or in a piecewise schedule with outdoor temperature, down to the TEV-limited floor. Condenser fan VFDs or staging logic must be configured to modulate condenser capacity — the fans speed up or additional fans stage on as the setpoint drops to maintain the target approach temperature. Capital cost for Tier 1 is low, typically $5,000 to $20,000 depending on system size, covering controls programming and condenser fan motor VFDs if not already installed. Savings are moderate — limited by the TEV's minimum pressure differential requirement — but the payback is fast. This tier is the right choice for systems where the remaining asset life or capital budget does not justify a full EEV retrofit.

Tier 2 is the full EEV retrofit enabling deeper floating. TEVs are replaced with electronic expansion valves at each evaporator circuit. EEVs use stepper motors or pulse-width modulated solenoids and tolerate much lower pressure differentials — some models operate reliably with less than $1\,\text{bar}$ ($15\,\text{psi}$) of differential. This allows the condensing temperature to float much further down, often to within $3\text{--}6\,\text{°C}$ ($5\text{--}10\,\text{°F}$) approach to outdoor air, with a minimum condensing temperature floor as low as $15\text{--}21\,\text{°C}$ ($60\text{--}70\,\text{°F}$). The implementation includes condenser fan VFDs (if not already present from a Tier 1 project), a full outdoor air reset schedule with the lower floor, and superheat controllers with zone temperature sensors for closed-loop EEV modulation. Each EEV maintains its own superheat setpoint independently of condensing pressure, which is what enables stable operation across such a wide range. Capital cost for Tier 2 is moderate to high — typically $20,000 to $80,000+ depending on the number of evaporator circuits, with each EEV plus controller plus wiring running approximately $1,500 to $3,000 installed per circuit. Savings are significantly higher than Tier 1 because the system captures many more hours of cool and cold weather operation where the condensing temperature can follow ambient further down. This tier is the right choice for systems in northern climates with many operating hours below the TEV floor, facilities with long remaining asset life, or projects where utility incentive programs offset the capital cost.

The condenser fan energy tradeoff applies to both tiers and must be accounted for in any honest savings analysis. At floating head pressure, the condenser fans run at higher speed to reject heat at a lower condensing temperature — the approach temperature must be maintained even as the condensing setpoint drops. This increases fan energy consumption. However, fan affinity laws dictate that fan power scales with the cube of speed:

$$
W_{\text{fan}} \propto \left(\frac{n}{n_{\text{design}}}\right)^3 \tag{12}
$$

Even at full speed, condenser fan motors are typically 5% to 15% of total rack power, while compressor motors are 70% to 85%. A 10% to 20% increase in condenser fan power is far outweighed by a 15% to 40% decrease in compressor power. The net energy balance captures both effects:

$$
\Delta W_{\text{net}} = \Delta W_{\text{comp}} - \Delta W_{\text{fans}} \tag{13}
$$

Here $\Delta W_{\text{comp}}$ is the compressor power reduction (positive represents savings) and $\Delta W_{\text{fans}}$ is the condenser fan power increase (positive represents penalty). The net savings are positive across virtually all operating conditions above the minimum condensing temperature floor, but the fan penalty magnitude depends on condenser design and condition — and it should be measured or calculated explicitly rather than assumed at a nominal percentage.

Condenser sizing matters. A condenser selected with generous surface area at design conditions will maintain a reasonable approach temperature at moderate fan speeds during cool weather, keeping the fan penalty small. An undersized condenser — or one operating beyond its original design load due to system modifications — may require full fan speed to hold the floating setpoint, which drives the fan penalty toward the upper end of the range. Coil fouling from dust, cottonwood seed, or grease buildup degrades heat transfer and forces higher fan speeds to compensate, effectively increasing the approach temperature and the fan energy cost. Restricted condenser airflow from snow accumulation, structural obstructions, or recirculation between condenser sections has the same effect. The practical implication is that condenser maintenance — coil cleaning, fan belt or direct-drive motor inspection, airflow verification — becomes more operationally important under floating head pressure than it is under fixed head pressure, because the system relies on full condenser capacity to capture the savings. A coil that is 20% fouled under fixed head pressure may not noticeably affect performance because the fans simply slow down to maintain the setpoint. The same fouled coil under floating head pressure prevents the condensing temperature from reaching the lower setpoint the controls are requesting, and the savings are silently eroded. For this reason, the net savings estimate should use the actual condenser condition rather than rated performance, and a sensitivity check on approach temperature is prudent.

Simplified analyses that ignore the fan energy penalty entirely overestimate net savings by 5% to 15%. Analyses that assume a nominal fan penalty without checking condenser condition may still misstate the net result by several percentage points. The companion notebook includes the fan energy calculation and allows the approach temperature to be adjusted to reflect site-specific condenser performance.

The following table summarizes the decision framework for selecting between the two tiers:

| Criterion | Tier 1 — TEV Float | Tier 2 — EEV Retrofit |
|---|---|---|
| **Capital Cost** | $5K-$20K | $20K-$80K+ |
| **Mechanical Changes** | None — controls + VFDs only | EEV installation at each evaporator |
| **Condensing Temp Floor** | ~24-29°C (75-85°F) | ~15-21°C (60-70°F) |
| **Savings Potential** | 10-20% of compressor energy | 20-40% of compressor energy |
| **Complexity** | Low — programming + VFDs | Moderate — new valves, controllers, wiring |
| **Simple Payback** | 0.5-2 years | 2-4 years |
| **Best Fit** | Short remaining asset life, limited budget | Northern climates, new builds, utility incentives |

---

## 7. Data Requirements and Regression Methodology (M&V)

The bin analysis from Section 4 produces a prospective savings estimate — it tells you what the savings should be based on thermodynamic calculations and typical weather. Verification requires measuring what actually happened after implementation. This section describes how to verify actual savings using regression-based measurement and verification aligned with IPMVP Option C (Whole Facility) or Option B (Retrofit Isolation) with submetered data.

The pre-retrofit baseline data collection establishes the relationship between compressor power and outdoor temperature before the floating head pressure strategy is implemented. The critical measurement is submetered compressor rack power in kilowatts — ideally at 15-minute intervals, with hourly as the minimum acceptable resolution. If submetering is not feasible, total electrical panel power for the compressor rack is acceptable, but condenser fans should be on a separate circuit or their contribution estimated and subtracted. Outdoor air temperature should be recorded from an on-site sensor or from the nearest Environment Canada or NOAA weather station at the same interval as the power data. The minimum data duration is 3 months covering a range of outdoor temperatures, but a full 12-month annual cycle is strongly preferred to capture the complete ambient temperature range and any seasonal patterns. Cold storage facilities with near-constant refrigeration loads — product temperature maintenance, not variable production processes — are ideal candidates for this approach because the refrigeration load is effectively constant and compressor power variation is driven almost entirely by ambient temperature.

The regression specification for the baseline period is a simple linear model:

$$
W_{\text{comp}} = \alpha + \beta \cdot T_{\text{amb}} + \varepsilon \tag{14}
$$

In this model, $W_{\text{comp}}$ is the average compressor power in kilowatts for each time interval, $T_{\text{amb}}$ is the outdoor air temperature, $\alpha$ is the intercept representing compressor power at $T_{\text{amb}} = 0\,\text{°C}$, $\beta$ is the slope in kW per degree of ambient temperature representing the sensitivity of compressor power to weather, and $\varepsilon$ is the residual error term. The slope $\beta$ is the quantity of primary interest — it captures how much additional power the compressor draws for each degree of increase in outdoor temperature.

The simple linear model is a starting point. Field conditions frequently warrant a more nuanced regression specification, and the practitioner should select the form that best fits the data rather than forcing a linear model onto a nonlinear system. Three alternatives deserve consideration depending on system behavior and data quality.

First, a piecewise linear regression with a changepoint at the fixed setpoint threshold. Under fixed head pressure, compressor power is approximately flat below the setpoint temperature (because the condensing pressure is clamped) and rises with ambient temperature above it. A single linear regression across the full temperature range averages these two regimes and produces a poor fit in both. Fitting two slopes — one below the changepoint and one above — often improves $R^2$ by 0.10 to 0.15 and produces more physically meaningful coefficients. The changepoint temperature is typically known from the control setpoint, so it does not need to be estimated from the data.

Second, a multivariable regression incorporating load indicators alongside ambient temperature. For facilities where the refrigeration load is not constant — mixed-use grocery with variable store hours, food processing with production schedules, or systems with intermittent large door openings — ambient temperature alone will not explain enough of the variance in compressor power. Adding a second independent variable such as daily production hours, door-open duration from BAS logging, or defrost cycle count can separate the ambient-driven effect from the load-driven effect and isolate the floating head pressure savings with greater precision. The form becomes $W_{\text{comp}} = \alpha + \beta_1 \cdot T_{\text{amb}} + \beta_2 \cdot X_{\text{load}} + \varepsilon$, where $X_{\text{load}}$ is the load proxy variable.

Third, a bin-based comparison as an alternative to continuous regression. Rather than fitting a regression line through the data, the pre-retrofit and post-retrofit datasets can be binned by outdoor temperature — using the same bins as the prospective bin analysis — and the average compressor power compared bin-by-bin. This approach makes no assumption about the functional form of the kW-vs-temperature relationship and handles nonlinearities, staging effects, and changepoints naturally. The tradeoff is that each bin requires sufficient data points for the average to be statistically meaningful, which demands longer data collection periods than regression typically requires.

The post-retrofit regression uses identical data collection — submetered compressor kW and outdoor temperature at the same intervals and for the same duration as the baseline period. The same regression form is applied: $W_{\text{comp}} = \alpha' + \beta' \cdot T_{\text{amb}} + \varepsilon'$. The expected result is a lower slope ($\beta' < \beta$), because floating head pressure makes the compressor power less sensitive to ambient temperature. Under fixed head pressure, the compressor power is flat (at the fixed-setpoint level) below the setpoint threshold and rises with temperature above it. Under floating head pressure, the compressor power tracks ambient more smoothly at a lower level across the cool and cold temperature range. The post-retrofit regression line sits below the pre-retrofit line across most of the temperature range, and the vertical distance between the lines represents the savings at each temperature.

The verified savings calculation sums the difference between the pre-retrofit prediction and the post-retrofit prediction across all post-implementation time intervals:

$$
\boxed{\Delta E_{\text{verified}} = \sum_{j=1}^{M} \left[(\alpha + \beta \cdot T_{\text{amb},j}) - (\alpha' + \beta' \cdot T_{\text{amb},j})\right] \cdot \Delta t} \tag{15}
$$

The sum runs over all post-implementation time intervals $j$, and $\Delta t$ is the interval duration in hours. This is the area between the pre-retrofit and post-retrofit regression lines, integrated over the actual post-implementation weather. It uses the pre-retrofit model to predict what the compressor would have consumed under the same weather conditions without the floating head pressure retrofit, then subtracts the actual post-retrofit consumption.

Several quality checks must be applied to validate the regression results. The pre-retrofit regression should achieve $R^2 > 0.75$ — compressor power should correlate strongly with outdoor temperature for a constant-load facility, and values below 0.75 suggest either a variable load or a data quality problem. Residual plots should be inspected for time-of-day patterns, weekday/weekend effects, or seasonal drift, any of which indicate a confounding variable that the single-variable regression is not capturing. Data periods with unusual load conditions — extended defrost cycles, product loading events, equipment outages — should be flagged and excluded from the regression. If the pre-retrofit and post-retrofit periods have significantly different weather distributions, the savings should be normalized to TMY weather for reporting by projecting both regression lines onto TMY hourly temperatures. The analysis should confirm that IPMVP Option C or Option B requirements are satisfied: independent variables must explain a sufficient fraction of the variance, and the baseline model should be validated against a hold-out period if one is available.

---

## 8. Worked Example — Savings Estimation

This section applies the methodology to a specific system with realistic parameters. The companion Jupyter notebook performs the complete bin analysis and generates the figures; the numbers presented here are representative of the expected results.

The facility is a grocery chain cold storage warehouse in southern Ontario, approximately $43.5\,\text{°N}$ latitude, operating year-round. The refrigerant is R-448A (Solstice N40) — a common lower-GWP replacement for R-404A with similar thermodynamic properties. The medium-temperature circuit consists of 4 semi-hermetic reciprocating compressors on a common suction header in a multiplex configuration, serving walk-in coolers for produce, dairy, and deli at an evaporating temperature of $T_{\text{evap}} = -7\,\text{°C}$ ($19.4\,\text{°F}$) with a total connected refrigeration load of approximately $120\,\text{kW}$ ($34\,\text{TR}$). The low-temperature circuit consists of 3 semi-hermetic reciprocating compressors on a separate suction header, serving walk-in freezers and ice cream cases at $T_{\text{evap}} = -25\,\text{°C}$ ($-13\,\text{°F}$) with approximately $45\,\text{kW}$ ($13\,\text{TR}$) of connected load. The condenser is a rooftop air-cooled unit with 8 fans and a total fan motor power of approximately $12\,\text{kW}$. The current control strategy holds a fixed minimum condensing temperature of $35\,\text{°C}$ ($95\,\text{°F}$), with condenser fans modulating to maintain this setpoint year-round. All evaporators are equipped with TEVs. The design condensing temperature is $40\,\text{°C}$ ($104\,\text{°F}$) at design outdoor temperature of $33\,\text{°C}$ ($91\,\text{°F}$).

A note on the load assumption: the bin analysis treats the refrigeration load as approximately constant — compressor power variation is attributed entirely to condensing temperature changes driven by ambient weather. For a dedicated cold storage warehouse maintaining product at fixed setpoints, this is a reasonable approximation, but it is not exact. Door openings during receiving and shipping introduce transient loads that vary with facility activity. Product loading events — receiving warm product into the cooler — create short-duration load spikes. Defrost schedules impose cyclical load swings as evaporator coils are periodically heated and then re-cooled. Ambient heat gain through the building envelope varies seasonally, adding a slow load component that correlates with outdoor temperature and partially confounds the condensing-temperature effect. These load variations are real, and they are why the regression-based M&V in Section 7 — which captures actual system behavior including load variation — is the appropriate tool for verified savings, while the bin analysis serves as the planning estimate. For facilities with more variable loads — mixed-use grocery with sales floor cases, food processing with batch schedules — the constant-load approximation becomes less defensible, and the multivariable regression approach described in Section 7 should be used.

Three scenarios are analyzed. The baseline holds condensing at $35\,\text{°C}$ year-round. The Tier 1 TEV float allows the condensing temperature to track ambient plus the $8\,\text{°C}$ approach temperature, with a floor at $27\,\text{°C}$ ($80\,\text{°F}$). The Tier 2 EEV retrofit floats with the same approach but with a floor at $18\,\text{°C}$ ($65\,\text{°F}$). The condenser approach temperature is $\Delta T_{\text{approach}} = 8\,\text{°C}$ ($14\,\text{°F}$), representative of a clean, properly sized air-cooled condenser at rated airflow. The compressor isentropic efficiency is set at $\eta_{\text{comp}} = 0.65$, representative for semi-hermetic reciprocating compressors at typical operating conditions. The electricity rate is $\$0.12/\text{kWh}$ for Ontario industrial/commercial supply.

Using CWEC weather data for the Toronto/Hamilton region, the 8,760 hourly temperatures are binned into $3\,\text{°C}$ intervals. Southern Ontario's climate produces winter lows approaching $-25\,\text{°C}$ and summer highs near $35\,\text{°C}$, with an annual mean around $7\text{--}8\,\text{°C}$. The critical observation is that the outdoor temperature is below $27\,\text{°C}$ — the threshold above which the fixed setpoint is naturally achieved at $8\,\text{°C}$ approach — for roughly 7,500 to 8,000 hours of the year. That is 85% to 90% of all operating hours. During those hours, the compressor is doing unnecessary work under the fixed setpoint strategy.

*[Figure 1: Compressor Power vs. Outdoor Temperature — Three curves overlaid showing total rack compressor power (kW, medium-temp + low-temp combined) as a function of outdoor air temperature for baseline fixed at 35°C, Tier 1 float with floor at 27°C, and Tier 2 float with floor at 18°C. The curves converge at high outdoor temperatures where all scenarios produce the same condensing temperature and diverge at low temperatures where the floating strategies capture progressively larger savings. — generated by companion notebook]*

At the baseline $35\,\text{°C}$ fixed condensing temperature, the combined medium-temp and low-temp compressor rack draws approximately $65\text{--}75\,\text{kW}$, depending on the specific compressor performance data. At $27\,\text{°C}$ condensing (the Tier 1 floor), the same rack draws approximately $50\text{--}60\,\text{kW}$ — a reduction of roughly $15\,\text{kW}$. At $18\,\text{°C}$ condensing (the Tier 2 floor), the rack draws approximately $40\text{--}48\,\text{kW}$ — a reduction of roughly $25\text{--}27\,\text{kW}$ from the fixed baseline. These power reductions apply only during the hours when the outdoor temperature is cool enough to achieve the lower condensing temperature. At the $35\,\text{°C}$ design day, all three scenarios produce the same condensing temperature and the same compressor power.

*[Figure 2: Temperature Bin Histogram with Savings Per Bin — Dual-axis chart with primary axis showing a bar chart of annual hours in each temperature bin (the weather distribution for southern Ontario) and secondary axis showing overlaid kWh savings per bin for Tier 1 and Tier 2. The majority of savings come from the 3,000+ hours per year when outdoor temperature is below the fixed setpoint threshold, with the cold-weather bins contributing disproportionately because the power reduction per bin is largest at the lowest temperatures. — generated by companion notebook]*

When the bin-by-bin savings are summed using Equation 11, the Tier 1 TEV-constrained float produces approximately 15% to 20% reduction in annual compressor energy consumption. For a rack consuming approximately 550,000 to 600,000 kWh annually at the fixed setpoint, this translates to roughly 85,000 to 110,000 kWh saved per year, or $10,000 to $13,000 at $\$0.12/\text{kWh}$. At a Tier 1 capital cost of approximately $12,000 (controls programming plus 8 condenser fan VFDs), the simple payback is under 1.5 years. The Tier 2 EEV retrofit produces approximately 25% to 35% reduction in annual compressor energy — roughly 140,000 to 200,000 kWh saved per year, or $17,000 to $24,000 annually. At a Tier 2 capital cost of approximately $55,000 (12 EEVs with controllers, controls programming, and VFDs), the simple payback is 2.5 to 3 years. Utility incentive programs that pay $0.05 to $0.10 per kWh of verified savings can offset 30% to 50% of the Tier 2 capital cost, bringing the payback below 2 years.

The condenser fan energy penalty — included in these net savings figures — is approximately 5% to 10% of gross compressor savings. The fans run harder at floating head pressure, but the cubic relationship in Equation 12 means the fan power increase is small relative to the compressor power reduction. The net savings remain strongly positive across all operating conditions.

These savings figures are estimation ranges, not deterministic predictions. They reflect the combined uncertainty in several input parameters, and each source of uncertainty should be understood. The compressor performance model — whether the COP-based approximation from Equation 4 or a polynomial fit to manufacturer data — introduces uncertainty, particularly at the low condensing temperatures enabled by Tier 2 where published performance data may not extend. TMY weather data represents a statistically typical year; actual weather in any given year will deviate, producing higher or lower savings depending on whether the winter is milder or harsher than average. The condenser approach temperature is treated as constant in the bin analysis, but in practice it varies with fouling condition, airflow, and wind direction — a fouled condenser with a $10\,\text{°C}$ actual approach rather than the assumed $8\,\text{°C}$ will produce lower savings because the condensing temperature cannot reach the target setpoint. The constant-load assumption, discussed above, adds further variance for facilities with significant load modulation. None of these uncertainties invalidates the estimate — the direction of savings is unambiguous and the approximate magnitude is robust across reasonable parameter ranges. But the bin analysis is a planning tool for project justification. The regression-based M&V described in Section 7 provides the verified, site-specific result that should be used for incentive reporting and performance accounting.

*[Figure 3: Pre/Post Regression Lines (M&V Demonstration) — Simulated scatter plot of compressor kW vs. outdoor temperature with fitted regression lines for pre-retrofit (higher slope, representing fixed head pressure operation) and post-retrofit (lower slope, representing floating head pressure). The area between the regression lines, shaded, represents verified savings integrated over the post-implementation weather data. R-squared values annotated for both regressions demonstrate adequate model fit. — generated by companion notebook]*

---

## 9. Limitations and Analytical Caveats

Every savings estimate carries assumptions. The following limitations should be understood when applying this framework, and each is paired with a practical mitigation.

The minimum condensing temperature floor varies by system and must be determined per installation through commissioning and testing. The floors used in this analysis — $27\,\text{°C}$ for the TEV-constrained scenario and $18\,\text{°C}$ for the EEV-enabled scenario — are representative of typical grocery refrigeration systems on HFC refrigerants, but they are not universal. Some TEV systems with oversized valves or high-side receivers tolerate lower floors. Some EEV systems have other binding constraints — oil return, defrost circuit pressure, or specific controller limitations — that set the floor higher than expected. The mitigation is straightforward: determine the actual minimum floor for each specific system through manufacturer consultation and controlled testing during commissioning.

Part-load behavior is not fully captured by the simple bin analysis. The method assumes that compressors operate at a single capacity point within each temperature bin. In practice, reciprocating compressors cycle on and off or unload cylinders to match capacity to load, and part-load efficiency differs from full-load efficiency. For multiplex racks with multiple staged compressors, the aggregate rack behavior partially captures this effect because the rack load-matches by staging individual compressors on and off, but individual compressor cycling dynamics — particularly the energy penalty of frequent starts and stops — are lost. The mitigation is to use time-averaged power data from submetering rather than instantaneous snapshots, which smooths the cycling effects and produces results consistent with the bin analysis assumptions.

The condenser fan energy tradeoff has been addressed in Section 6, but it bears repeating: floating head pressure reduces compressor power and increases condenser fan power. The net benefit must be confirmed by including fan energy in the analysis. The worked example accounts for both, but simplified analyses that ignore the fan penalty overestimate net savings by 5% to 15%. For systems with undersized condensers or fouled condenser coils, the fan penalty may be higher because the fans must work harder to maintain the approach temperature.

Refrigerant charge management introduces an operational variable that the bin analysis does not capture. At varying condensing pressures, the distribution of refrigerant charge between the condenser, receiver, evaporators, and liquid line shifts. Systems with marginal refrigerant charge or without a receiver may experience operational issues — liquid slugging, flash gas in the liquid line, or inadequate subcooling — at very low condensing pressures. Charge optimization should be performed as part of the floating head pressure implementation, and sufficient receiver volume or charge management controls should be confirmed.

Interaction with other energy conservation measures is a real concern when multiple ECMs are implemented simultaneously. Floating head pressure interacts with compressor VFDs — both reduce compressor power, and the savings are not simply additive because each measure changes the baseline for the other. It interacts with economizer subcoolers, which become less effective at lower condensing pressures because the available temperature differential for subcooling is reduced. It interacts with heat recovery systems, which require elevated condensing temperatures to produce useful heat — implementing floating head pressure on a system with active heat recovery may reduce or eliminate the recovered heat. These interactions must be evaluated explicitly when multiple ECMs are in the project scope.

Seasonal load variation affects the validity of the constant-load assumption. The worked example assumes near-constant refrigeration load, which is appropriate for dedicated cold storage maintaining product at a fixed setpoint. Facilities with variable production schedules — food processing plants, breweries, seasonal production lines — will show load-driven variation in compressor power that confounds the ambient temperature regression. For these applications, load normalization or a multi-variable regression model (kW vs. $T_{\text{amb}}$ plus production volume or product throughput) is required to isolate the floating head pressure savings from load-driven changes.

Manufacturer-specific compressor performance curves introduce uncertainty in the polynomial fit used in the bin analysis. Published performance data is typically available only at standard AHRI 540 rating conditions, and extrapolation outside these conditions — particularly to the low condensing temperatures enabled by Tier 2 — introduces uncertainty. The mitigation is to validate the polynomial fit against actual submetered performance data during the baseline period and to use the regression-based M&V in Section 7 rather than the bin analysis alone for final savings reporting.

Weather data representativeness is a consideration for any TMY-based analysis. TMY data represents a statistically typical year, not any specific year. Actual savings in a given year will differ from the TMY estimate depending on how that year's weather deviates from the long-term average. A mild winter produces fewer savings than the TMY predicts; a harsh winter produces more. For M&V reporting, actual weather data from the post-implementation period should be used — not TMY — and the bin analysis TMY estimate should be treated as the project justification figure, not the verification figure.

---

## 10. Recommended Workflow

The following workflow takes a project from initial system characterization through verified savings reporting. It produces both a prospective savings estimate for project justification and a retrospective verified savings figure for performance confirmation.

**Characterize the existing system.** Document the compressor type (reciprocating, screw, or scroll), refrigerant, condenser type (air-cooled, evaporative, or water-cooled), number of circuits and suction groups, evaporating temperatures for each circuit, and the current condensing pressure or condensing temperature setpoint.

**Determine the expansion valve type** at each evaporator — TEV or EEV. This determination dictates which retrofit tier applies and sets the minimum condensing temperature floor. Walk down every evaporator circuit and confirm the valve type. Mixed systems — some circuits on TEVs and others on EEVs — are not uncommon in facilities that have undergone partial retrofits.

**Identify the minimum allowable condensing pressure.** Evaluate all four constraints: TEV pressure differential requirements, oil return at low compression ratios, hot gas defrost pressure needs, and liquid line subcooling margins. The most restrictive constraint sets the hard floor. Consult the valve manufacturer's minimum operating pressure differential data for TEV systems, or the EEV controller documentation for minimum differential pressure ratings on EEV systems.

**Obtain or develop compressor performance data.** Manufacturer performance maps — compressor kW and capacity as functions of saturated suction temperature and saturated discharge temperature — are the preferred source. AHRI-rated performance data at standard conditions provides validated data points. Fit a polynomial model of compressor kW as a function of condensing temperature at the actual evaporating temperature for each circuit.

**Collect TMY weather data** for the facility location. Use CWEC files for Canadian locations and TMY3 for US locations. Parse the hourly dry-bulb temperatures and construct temperature bins at $3\,\text{°C}$ intervals. Verify that the bin hours sum to 8,760.

**Run the bin analysis** using Equations 6 through 11 to estimate annual savings for Tier 1 and/or Tier 2 scenarios. Include the condenser fan energy tradeoff from Equations 12 and 13. The companion Jupyter notebook automates this calculation for the grocery cold storage worked example and can be adapted to other system parameters.

**Evaluate the retrofit economics.** Compare Tier 1 capital cost (controls programming plus condenser fan VFDs) against Tier 2 (EEV hardware plus controls plus VFDs), with both compared to estimated annual net energy savings. Check for utility incentive programs — many Canadian provincial programs and US utility demand-side management programs offer prescriptive or custom incentives for refrigeration efficiency improvements that can offset 30% to 50% of capital cost.

**Install submetering and collect baseline data** before implementing any changes. Submetered compressor rack kW and outdoor air temperature at 15-minute or hourly intervals, covering a minimum of 3 months with a representative range of outdoor temperatures. A full 12-month baseline is strongly preferred for regression quality and to capture the complete annual temperature cycle. Without baseline data, post-implementation verification is not possible.

**Implement the floating head pressure control strategy.** Program the outdoor air temperature reset schedule into the PLC or BAS, set the minimum condensing temperature floor, commission the condenser fan VFD control logic, and — for Tier 2 — install and commission EEVs with superheat controllers at each evaporator circuit. Commissioning should include controlled testing at progressively lower condensing temperatures to confirm stable operation before setting the final floor.

**Collect post-implementation data** — the same measurements, same intervals, and same duration as the baseline period. A minimum of 3 months covering a comparable temperature range is required; 12 months matching the baseline period is the standard for IPMVP compliance.

**Run the pre/post regression comparison.** Fit $W_{\text{comp}}$ vs. $T_{\text{amb}}$ regressions for both periods using Equation 14, calculate verified savings using Equation 15, and validate the regression quality. Confirm $R^2 > 0.75$ for both regressions, inspect residual plots for systematic patterns, and flag any data periods with unusual operating conditions.

**Report verified savings.** Express the results as annual kWh saved, annual dollars saved at the facility's blended electricity rate, and percentage of baseline compressor energy consumption. Format the results for utility incentive program submissions, internal capital planning documentation, and greenhouse gas emissions reporting.

This workflow produces both a prospective estimate (bin analysis, before implementation) and a verified figure (regression M&V, after implementation). The two should be compared. If verified savings are significantly lower than estimated, investigate operating conditions, actual control setpoints, load changes, and condenser performance to identify the discrepancy.

---

## 11. Conclusion

Floating head pressure is among the most cost-effective energy conservation measures available in commercial and industrial refrigeration. The thermodynamic basis is direct: lowering the condensing temperature reduces the compression ratio, improves the coefficient of performance, and reduces compressor power consumption for the same refrigeration load. Two implementation tiers — a controls-only retrofit for TEV-equipped systems and a full EEV retrofit for deeper floating — both deliver measurable, verifiable compressor energy savings with strong payback periods.

The temperature bin method provides a defensible prospective savings estimate using TMY weather data and manufacturer compressor performance data. It translates the thermodynamic relationships into a site-specific annual kWh figure that can justify capital investment and support utility incentive applications. The methodology is transparent, reproducible, and grounded in physical relationships rather than rules of thumb.

Regression-based M&V aligned with IPMVP closes the loop by providing post-implementation savings verification. The pre/post regression comparison isolates the floating head pressure effect from other variables and produces a verified savings figure suitable for incentive program reporting, capital planning, and GHG accounting. For constant-load facilities like cold storage warehouses, a simple linear regression of compressor kW against outdoor temperature achieves adequate fit and produces clear, defensible results.

Capital costs are low for Tier 1 (controls and VFDs, typically $5,000 to $20,000) and moderate for Tier 2 (EEV hardware and controls, typically $20,000 to $80,000+), with simple payback periods often under 2 years for Tier 1 and 2 to 4 years for Tier 2. Utility incentive programs available in most Canadian provinces and many US jurisdictions can reduce the effective capital cost significantly.

The methodology generalizes across refrigeration applications. Grocery cold storage, food processing, ice rinks, supermarket multiplex racks, and chilled water systems with condenser water temperature reset all follow the same thermodynamic relationships. The condenser type, approach temperature, and system-specific minimum floor change the numbers, but the analytical framework — bin analysis for estimation, regression for verification — applies directly.

The companion Jupyter notebook implements the complete bin analysis for the grocery cold storage worked example, generates all three figures, and includes sensitivity analysis on the key assumptions. It is designed to be adapted to other system parameters by modifying the input variables.

Floating head pressure is not a new idea — it has been standard practice in industrial ammonia refrigeration for decades. What has changed is the availability of affordable EEV hardware, modern PLC and BAS control platforms, and submetering infrastructure that make implementation and verification straightforward for commercial systems. The methodology in this post provides the analytical framework to justify, implement, and verify the savings.
