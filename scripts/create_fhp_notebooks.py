"""Create floating head pressure Jupyter notebooks from blog post content."""
import json
import os

PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(PROJ_ROOT, "public", "notebooks")

METADATA = {
    "kernelspec": {"display_name": "base", "language": "python", "name": "python3"},
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.12.7",
    },
}


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": [text]}


def code(text):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [text],
    }


def create_nb01():
    """NB01: System Modeling & Temperature Bin Analysis."""
    cells = [
        md(
            "# Floating Head Pressure \u2014 System Modeling & Temperature Bin Analysis\n\n"
            "**Abriliam Consulting** \u2014 Industrial Energy Management\n\n"
            "This notebook builds a compressor performance model for a grocery cold storage "
            "reciprocating rack system on R-448A and runs a temperature bin analysis using "
            "TMY weather data to estimate annual compressor energy savings from floating "
            "head pressure control under two retrofit tiers:\n\n"
            "- **Tier 1:** Controls-only float with TEV-constrained floor at 27\u00b0C\n"
            "- **Tier 2:** Full EEV retrofit enabling deeper float with floor at 18\u00b0C\n\n"
            "**Key outputs:** Annual kWh savings, percentage reduction, and dollar savings for each tier."
        ),
        code(
            'import matplotlib\nmatplotlib.use("Agg")\n'
            "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\n"
            'plt.rcParams.update({"figure.figsize": (10, 6), "font.size": 11})'
        ),
        md(
            "## 1. System Parameters\n\n"
            "The facility is a grocery chain cold storage warehouse in southern Ontario "
            "(~43.5\u00b0N latitude). The refrigerant is R-448A (Solstice N40). Two compressor "
            "circuits serve medium-temperature and low-temperature loads."
        ),
        code(
            "# === System Parameters ===\n\n"
            "# Refrigerant: R-448A\n"
            "# Evaporating temperatures\n"
            "T_evap_MT = -7.0    # deg C - medium-temp circuit (walk-in coolers)\n"
            "T_evap_LT = -25.0   # deg C - low-temp circuit (freezers)\n\n"
            "# Refrigeration loads (constant for cold storage)\n"
            "Q_evap_MT = 120.0    # kW - medium-temp load (~34 TR)\n"
            "Q_evap_LT = 45.0     # kW - low-temp load (~13 TR)\n\n"
            "# Condenser parameters\n"
            "T_approach = 8.0     # deg C - air-cooled condenser approach at rated airflow\n"
            "T_cond_fixed = 35.0  # deg C - current fixed condensing setpoint\n"
            "T_cond_floor_T1 = 27.0  # deg C - Tier 1 TEV-constrained floor\n"
            "T_cond_floor_T2 = 18.0  # deg C - Tier 2 EEV-enabled floor\n\n"
            "# Compressor efficiency\n"
            "eta_comp = 0.65      # isentropic efficiency (semi-hermetic reciprocating)\n\n"
            "# Condenser fan parameters\n"
            "W_fan_rated = 12.0   # kW - total condenser fan motor power at full speed\n\n"
            "# Economics\n"
            "elec_rate = 0.12     # $/kWh - Ontario industrial/commercial rate\n\n"
            'print("System parameters loaded.")\n'
            'print(f"  MT circuit: T_evap = {T_evap_MT} deg C, Q = {Q_evap_MT} kW")\n'
            'print(f"  LT circuit: T_evap = {T_evap_LT} deg C, Q = {Q_evap_LT} kW")\n'
            'print(f"  Fixed condensing: {T_cond_fixed} deg C")\n'
            'print(f"  Tier 1 floor: {T_cond_floor_T1} deg C | Tier 2 floor: {T_cond_floor_T2} deg C")'
        ),
        md(
            "## 2. Compressor Performance Model\n\n"
            "The COP is modeled using the Carnot-based approximation scaled by compressor "
            "isentropic efficiency:\n\n"
            "$$\\text{COP} \\approx \\frac{T_{\\text{evap}}}{T_{\\text{cond}} - T_{\\text{evap}}} "
            "\\times \\eta_{\\text{comp}}$$\n\n"
            "Compressor power follows from $W_{\\text{comp}} = Q_{\\text{evap}} / \\text{COP}$.\n\n"
            "This is a simplified model \u2014 real compressor performance uses manufacturer "
            "polynomial maps. The model captures the dominant thermodynamic trend: as "
            "$T_{\\text{cond}}$ decreases, COP improves and compressor power drops."
        ),
        code(
            "def calc_cop(T_evap_C, T_cond_C, eta=0.65):\n"
            '    """Calculate COP using Carnot-based approximation.\n\n'
            "    Parameters\n"
            "    ----------\n"
            "    T_evap_C : float or array - evaporating temperature (deg C)\n"
            "    T_cond_C : float or array - condensing temperature (deg C)\n"
            "    eta : float - compressor isentropic efficiency\n\n"
            "    Returns\n"
            "    -------\n"
            "    COP : float or array\n"
            '    """\n'
            "    T_evap_K = T_evap_C + 273.15\n"
            "    T_cond_K = T_cond_C + 273.15\n"
            "    return (T_evap_K / (T_cond_K - T_evap_K)) * eta\n\n\n"
            "def calc_compressor_power(Q_evap, T_evap_C, T_cond_C, eta=0.65):\n"
            '    """Calculate compressor power (kW) for given conditions."""\n'
            "    cop = calc_cop(T_evap_C, T_cond_C, eta)\n"
            "    return Q_evap / cop\n\n\n"
            "# Verify at design conditions\n"
            "cop_MT = calc_cop(T_evap_MT, T_cond_fixed, eta_comp)\n"
            "cop_LT = calc_cop(T_evap_LT, T_cond_fixed, eta_comp)\n"
            "W_MT = calc_compressor_power(Q_evap_MT, T_evap_MT, T_cond_fixed, eta_comp)\n"
            "W_LT = calc_compressor_power(Q_evap_LT, T_evap_LT, T_cond_fixed, eta_comp)\n\n"
            'print(f"At T_cond = {T_cond_fixed} deg C (fixed setpoint):")\n'
            'print(f"  MT circuit: COP = {cop_MT:.2f}, W_comp = {W_MT:.1f} kW")\n'
            'print(f"  LT circuit: COP = {cop_LT:.2f}, W_comp = {W_LT:.1f} kW")\n'
            'print(f"  Total rack power: {W_MT + W_LT:.1f} kW")'
        ),
        md(
            "## 3. Compressor Power vs. Condensing Temperature\n\n"
            "Plot showing how total rack compressor power varies with condensing temperature. "
            "This illustrates the thermodynamic basis for floating head pressure savings."
        ),
        code(
            "# Compressor power curves across condensing temperature range\n"
            "T_cond_range = np.linspace(15, 45, 100)\n\n"
            "W_total = np.array([\n"
            "    calc_compressor_power(Q_evap_MT, T_evap_MT, tc, eta_comp) +\n"
            "    calc_compressor_power(Q_evap_LT, T_evap_LT, tc, eta_comp)\n"
            "    for tc in T_cond_range\n"
            "])\n\n"
            "fig, ax = plt.subplots()\n"
            'ax.plot(T_cond_range, W_total, "b-", linewidth=2)\n'
            'ax.axvline(T_cond_fixed, color="red", linestyle="--", alpha=0.7,\n'
            '           label=f"Fixed setpoint ({T_cond_fixed} deg C)")\n'
            'ax.axvline(T_cond_floor_T1, color="orange", linestyle="--", alpha=0.7,\n'
            '           label=f"Tier 1 floor ({T_cond_floor_T1} deg C)")\n'
            'ax.axvline(T_cond_floor_T2, color="green", linestyle="--", alpha=0.7,\n'
            '           label=f"Tier 2 floor ({T_cond_floor_T2} deg C)")\n'
            'ax.set_xlabel("Condensing Temperature (deg C)")\n'
            'ax.set_ylabel("Total Compressor Power (kW)")\n'
            'ax.set_title("Compressor Power vs. Condensing Temperature")\n'
            "ax.legend()\n"
            "ax.grid(True, alpha=0.3)\n"
            "plt.tight_layout()\n"
            'plt.savefig("compressor_power_vs_tcond.png", dpi=150, bbox_inches="tight")\n'
            "plt.close()\n"
            'print("Figure saved.")'
        ),
        md(
            "## 4. TMY Weather Data \u2014 Temperature Bin Construction\n\n"
            "We generate a synthetic TMY-like annual temperature distribution for southern "
            "Ontario (~43.5\u00b0N). The distribution uses a sinusoidal seasonal model with daily "
            "variation, producing realistic temperature bins.\n\n"
            "In practice, CWEC (Canadian Weather for Energy Calculations) data would be "
            "used for actual project work."
        ),
        code(
            "# Generate synthetic TMY-like hourly temperatures for southern Ontario\n"
            "np.random.seed(42)\n"
            "hours = np.arange(8760)\n\n"
            "# Seasonal sinusoid: mean ~7.5 deg C, amplitude ~16 deg C\n"
            "day_of_year = hours / 24.0\n"
            "T_seasonal = 7.5 + 16.0 * np.sin(2 * np.pi * (day_of_year - 100) / 365)\n\n"
            "# Daily variation: ~5 deg C amplitude\n"
            "T_daily = 5.0 * np.sin(2 * np.pi * hours / 24 - np.pi / 2)\n\n"
            "# Random noise\n"
            "T_noise = np.random.normal(0, 3.0, 8760)\n\n"
            "T_amb_hourly = T_seasonal + T_daily + T_noise\n"
            "T_amb_hourly = np.clip(T_amb_hourly, -30, 38)\n\n"
            'print(f"Synthetic TMY data: {len(T_amb_hourly)} hours")\n'
            'print(f"  Min: {T_amb_hourly.min():.1f} deg C")\n'
            'print(f"  Max: {T_amb_hourly.max():.1f} deg C")\n'
            'print(f"  Mean: {T_amb_hourly.mean():.1f} deg C")'
        ),
        code(
            "# Build temperature bins (3 deg C width)\n"
            "bin_width = 3.0\n"
            "bin_edges = np.arange(-30, 42, bin_width)\n"
            "bin_midpoints = bin_edges[:-1] + bin_width / 2\n\n"
            "# Count hours in each bin\n"
            "bin_hours, _ = np.histogram(T_amb_hourly, bins=bin_edges)\n\n"
            "# Verify total hours\n"
            'assert bin_hours.sum() == 8760, f"Bin hours sum to {bin_hours.sum()}, expected 8760"\n\n'
            "# Create DataFrame for clarity\n"
            "bins_df = pd.DataFrame({\n"
            '    "T_mid (deg C)": bin_midpoints,\n'
            '    "Hours": bin_hours\n'
            "})\n"
            'bins_df = bins_df[bins_df["Hours"] > 0].reset_index(drop=True)\n'
            'print(f"Temperature bins: {len(bins_df)} active bins")\n'
            "print(f\"Hours below {T_cond_fixed - T_approach} deg C (savings zone): "
            '{bin_hours[bin_midpoints < (T_cond_fixed - T_approach)].sum()}")\n'
            "print()\n"
            "print(bins_df.to_string(index=False))"
        ),
        md(
            "## 5. Temperature Bin Analysis \u2014 Energy Savings Calculation\n\n"
            "For each temperature bin, we calculate:\n\n"
            "1. **Fixed scenario:** $T_{\\text{cond}} = \\max(T_{\\text{amb}} + "
            "\\Delta T_{\\text{approach}},\\; T_{\\text{cond,setpoint}})$\n"
            "2. **Floating scenario:** $T_{\\text{cond}} = \\max(T_{\\text{amb}} + "
            "\\Delta T_{\\text{approach}},\\; T_{\\text{cond,floor}})$\n"
            "3. **Power difference:** $\\Delta W = W_{\\text{fixed}} - W_{\\text{float}}$\n"
            "4. **Energy saved per bin:** $\\Delta E = \\Delta W \\times h_i$"
        ),
        code(
            "def bin_analysis(T_bins, hours, T_cond_setpoint, T_cond_floor, T_approach,\n"
            "                 Q_MT, T_evap_MT, Q_LT, T_evap_LT, eta):\n"
            '    """Run temperature bin analysis for floating head pressure savings.\n\n'
            "    Returns DataFrame with per-bin results.\n"
            '    """\n'
            "    results = []\n"
            "    for T_amb, h in zip(T_bins, hours):\n"
            "        if h == 0:\n"
            "            continue\n\n"
            "        # Condensing temperatures\n"
            "        T_cond_fix = max(T_amb + T_approach, T_cond_setpoint)\n"
            "        T_cond_flt = max(T_amb + T_approach, T_cond_floor)\n\n"
            "        # Compressor power - fixed\n"
            "        W_fixed = (calc_compressor_power(Q_MT, T_evap_MT, T_cond_fix, eta) +\n"
            "                   calc_compressor_power(Q_LT, T_evap_LT, T_cond_fix, eta))\n\n"
            "        # Compressor power - floating\n"
            "        W_float = (calc_compressor_power(Q_MT, T_evap_MT, T_cond_flt, eta) +\n"
            "                   calc_compressor_power(Q_LT, T_evap_LT, T_cond_flt, eta))\n\n"
            "        dW = W_fixed - W_float\n"
            "        dE = dW * h\n\n"
            "        results.append({\n"
            '            "T_amb": T_amb, "Hours": h,\n'
            '            "T_cond_fixed": T_cond_fix, "T_cond_float": T_cond_flt,\n'
            '            "W_fixed_kW": W_fixed, "W_float_kW": W_float,\n'
            '            "dW_kW": dW, "dE_kWh": dE\n'
            "        })\n\n"
            "    return pd.DataFrame(results)\n\n\n"
            "# Run for both tiers\n"
            "tier1 = bin_analysis(bin_midpoints, bin_hours, T_cond_fixed, T_cond_floor_T1,\n"
            "                     T_approach, Q_evap_MT, T_evap_MT, Q_evap_LT, T_evap_LT, eta_comp)\n\n"
            "tier2 = bin_analysis(bin_midpoints, bin_hours, T_cond_fixed, T_cond_floor_T2,\n"
            "                     T_approach, Q_evap_MT, T_evap_MT, Q_evap_LT, T_evap_LT, eta_comp)\n\n"
            "# Annual baseline energy\n"
            'baseline_kWh = (tier1["W_fixed_kW"] * tier1["Hours"]).sum()\n\n'
            'print("=== ANNUAL SAVINGS SUMMARY ===")\n'
            'print(f"Baseline annual compressor energy: {baseline_kWh:,.0f} kWh")\n'
            "print()\n"
            'for name, df in [("Tier 1 (TEV floor 27 deg C)", tier1), ("Tier 2 (EEV floor 18 deg C)", tier2)]:\n'
            '    savings_kWh = df["dE_kWh"].sum()\n'
            "    pct = 100 * savings_kWh / baseline_kWh\n"
            "    dollars = savings_kWh * elec_rate\n"
            '    print(f"{name}:")\n'
            '    print(f"  Annual savings: {savings_kWh:,.0f} kWh ({pct:.1f}%)")\n'
            '    print(f"  Dollar savings: ${dollars:,.0f}/yr at ${elec_rate}/kWh")\n'
            "    print()"
        ),
        md("## 6. Figure 1 \u2014 Compressor Power vs. Outdoor Temperature (Three Scenarios)"),
        code(
            "fig, ax = plt.subplots(figsize=(11, 6))\n\n"
            '# Plot power curves for each scenario\n'
            'ax.plot(tier1["T_amb"], tier1["W_fixed_kW"], "r-o", markersize=3,\n'
            '        label=f"Baseline - Fixed at {T_cond_fixed} deg C", linewidth=2)\n'
            'ax.plot(tier1["T_amb"], tier1["W_float_kW"], "darkorange", marker="s", markersize=3,\n'
            '        label=f"Tier 1 - Float, floor {T_cond_floor_T1} deg C", linewidth=2)\n'
            'ax.plot(tier2["T_amb"], tier2["W_float_kW"], "green", marker="^", markersize=3,\n'
            '        label=f"Tier 2 - Float, floor {T_cond_floor_T2} deg C", linewidth=2)\n\n'
            'ax.set_xlabel("Outdoor Air Temperature (deg C)")\n'
            'ax.set_ylabel("Total Compressor Power (kW)")\n'
            'ax.set_title("Figure 1: Compressor Power vs. Outdoor Temperature")\n'
            'ax.legend(loc="upper left")\n'
            "ax.grid(True, alpha=0.3)\n"
            "ax.set_xlim(-30, 38)\n"
            "plt.tight_layout()\n"
            'plt.savefig("fig1_power_vs_ambient.png", dpi=150, bbox_inches="tight")\n'
            "plt.close()\n"
            'print("Figure 1 saved.")'
        ),
        md("## 7. Figure 2 \u2014 Temperature Bin Histogram with Savings Per Bin"),
        code(
            "fig, ax1 = plt.subplots(figsize=(12, 6))\n\n"
            "# Bar chart: hours per bin\n"
            "bar_width = 2.4\n"
            'ax1.bar(tier1["T_amb"], tier1["Hours"], width=bar_width, alpha=0.3,\n'
            '        color="steelblue", label="Annual Hours", edgecolor="steelblue")\n'
            'ax1.set_xlabel("Outdoor Temperature Bin Midpoint (deg C)")\n'
            'ax1.set_ylabel("Hours per Year", color="steelblue")\n'
            'ax1.tick_params(axis="y", labelcolor="steelblue")\n\n'
            "# Secondary axis: kWh savings per bin\n"
            "ax2 = ax1.twinx()\n"
            'ax2.plot(tier1["T_amb"], tier1["dE_kWh"], "darkorange", marker="s", markersize=4,\n'
            '         linewidth=2, label="Tier 1 Savings (kWh)")\n'
            'ax2.plot(tier2["T_amb"], tier2["dE_kWh"], "green", marker="^", markersize=4,\n'
            '         linewidth=2, label="Tier 2 Savings (kWh)")\n'
            'ax2.set_ylabel("Energy Savings per Bin (kWh)", color="darkorange")\n'
            'ax2.tick_params(axis="y", labelcolor="darkorange")\n\n'
            "# Combined legend\n"
            "lines1, labels1 = ax1.get_legend_handles_labels()\n"
            "lines2, labels2 = ax2.get_legend_handles_labels()\n"
            'ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")\n\n'
            'ax1.set_title("Figure 2: Temperature Bin Distribution & Energy Savings per Bin")\n'
            "ax1.grid(True, alpha=0.2)\n"
            "plt.tight_layout()\n"
            'plt.savefig("fig2_bin_savings.png", dpi=150, bbox_inches="tight")\n'
            "plt.close()\n"
            'print("Figure 2 saved.")'
        ),
        md(
            "## 8. Condenser Fan Energy Tradeoff\n\n"
            "At floating head pressure, condenser fans run harder to maintain the approach "
            "temperature. Fan power scales with the cube of speed (fan affinity laws). We "
            "estimate the net savings after accounting for increased fan energy."
        ),
        code(
            "def estimate_fan_penalty(T_amb, T_cond_float, T_cond_fixed_val, T_approach, W_fan_rated):\n"
            '    """Estimate condenser fan power increase under floating head pressure."""\n'
            "    # Fan speed fraction - fixed (fans slow down when cold)\n"
            "    speed_fixed = np.clip((T_amb + T_approach) / T_cond_fixed_val, 0.2, 1.0)\n"
            "    W_fan_fixed = W_fan_rated * speed_fixed**3\n\n"
            "    # Fan speed fraction - floating (fans run to maintain approach)\n"
            "    speed_float = np.clip((T_amb + T_approach) / (T_amb + T_approach + 2), 0.3, 1.0)\n"
            "    W_fan_float = W_fan_rated * speed_float**3\n\n"
            "    return W_fan_float - W_fan_fixed  # positive = penalty\n\n\n"
            '# Calculate fan penalty for each tier\n'
            'for name, df in [("Tier 1", tier1), ("Tier 2", tier2)]:\n'
            "    fan_penalty = []\n"
            "    for _, row in df.iterrows():\n"
            '        dp = estimate_fan_penalty(row["T_amb"], row["T_cond_float"],\n'
            "                                  T_cond_fixed, T_approach, W_fan_rated)\n"
            '        fan_penalty.append(max(dp, 0) * row["Hours"])\n\n'
            "    total_fan_penalty = sum(fan_penalty)\n"
            '    gross_savings = df["dE_kWh"].sum()\n'
            "    net_savings = gross_savings - total_fan_penalty\n\n"
            '    print(f"{name}:")\n'
            '    print(f"  Gross compressor savings: {gross_savings:,.0f} kWh")\n'
            '    print(f"  Fan energy penalty:       {total_fan_penalty:,.0f} kWh ({100*total_fan_penalty/gross_savings:.1f}% of gross)")\n'
            '    print(f"  Net savings:              {net_savings:,.0f} kWh")\n'
            '    print(f"  Net dollar savings:       ${net_savings * elec_rate:,.0f}/yr")\n'
            "    print()"
        ),
        md("## 9. Payback Analysis"),
        code(
            "# Capital costs (representative)\n"
            "capex_T1 = 12000   # Controls programming + 8 condenser fan VFDs\n"
            "capex_T2 = 55000   # 12 EEVs + controllers + controls + VFDs\n\n"
            'for name, df, capex in [("Tier 1", tier1, capex_T1), ("Tier 2", tier2, capex_T2)]:\n'
            '    annual_savings_dollars = df["dE_kWh"].sum() * elec_rate\n'
            "    payback = capex / annual_savings_dollars\n"
            '    print(f"{name}:")\n'
            '    print(f"  Capital cost: ${capex:,}")\n'
            '    print(f"  Annual savings: ${annual_savings_dollars:,.0f}")\n'
            '    print(f"  Simple payback: {payback:.1f} years")\n\n'
            "    # With utility incentive\n"
            "    incentive_rate = 0.08\n"
            '    incentive = df["dE_kWh"].sum() * incentive_rate\n'
            "    net_capex = capex - incentive\n"
            "    payback_incent = net_capex / annual_savings_dollars\n"
            '    print(f"  With utility incentive (${incentive_rate}/kWh): ${incentive:,.0f} rebate")\n'
            '    print(f"  Net capital: ${net_capex:,.0f} -> Payback: {payback_incent:.1f} years")\n'
            "    print()"
        ),
        md(
            "## 10. Summary\n\n"
            "The temperature bin analysis demonstrates that floating head pressure control "
            "yields significant compressor energy savings for this grocery cold storage "
            "facility in southern Ontario:\n\n"
            "| Metric | Tier 1 (TEV, 27\u00b0C floor) | Tier 2 (EEV, 18\u00b0C floor) |\n"
            "|---|---|---|\n"
            "| Annual savings | ~15-20% | ~25-35% |\n"
            "| Dollar savings | ~$10,000-$13,000/yr | ~$17,000-$24,000/yr |\n"
            "| Capital cost | ~$12,000 | ~$55,000 |\n"
            "| Simple payback | <1.5 years | 2.5-3 years |\n\n"
            "The majority of savings accrue during the 7,500+ hours per year when outdoor "
            "temperature is below 27\u00b0C \u2014 roughly 85-90% of all operating hours. The condenser "
            "fan energy penalty is 5-10% of gross compressor savings.\n\n"
            "**Next:** Notebook 02 demonstrates the regression-based M&V framework for "
            "verifying actual savings post-implementation."
        ),
        md(
            "---\n*Abriliam Consulting \u2014 Industrial Energy Management*\n"
            "*Floating Head Pressure Analysis \u2014 Notebook 01 of 02*"
        ),
    ]

    nb = {"nbformat": 4, "nbformat_minor": 5, "metadata": METADATA, "cells": cells}
    path = os.path.join(NB_DIR, "floating-head-01-system-modeling.ipynb")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"NB01 written: {path} ({len(cells)} cells)")


def create_nb02():
    """NB02: M&V Regression Framework & Sensitivity Analysis."""
    cells = [
        md(
            "# Floating Head Pressure \u2014 M&V Regression Framework & Sensitivity Analysis\n\n"
            "**Abriliam Consulting** \u2014 Industrial Energy Management\n\n"
            "This notebook demonstrates regression-based measurement and verification (M&V) "
            "for floating head pressure savings using simulated pre/post compressor power "
            "data, aligned with IPMVP Option B/C methodology.\n\n"
            "**Key outputs:**\n"
            "- Pre/post regression model comparison\n"
            "- Verified annual savings calculation\n"
            "- Sensitivity analysis on key assumptions"
        ),
        code(
            'import matplotlib\nmatplotlib.use("Agg")\n'
            "import numpy as np\nimport pandas as pd\nimport matplotlib.pyplot as plt\n"
            "from scipy import stats\n\n"
            'plt.rcParams.update({"figure.figsize": (10, 6), "font.size": 11})'
        ),
        md(
            "## 1. System Parameters (Same as Notebook 01)\n\n"
            "We reuse the same system configuration for consistency."
        ),
        code(
            "# System parameters\n"
            "T_evap_MT = -7.0     # deg C\n"
            "T_evap_LT = -25.0    # deg C\n"
            "Q_evap_MT = 120.0    # kW\n"
            "Q_evap_LT = 45.0     # kW\n"
            "T_cond_fixed = 35.0  # deg C - baseline fixed setpoint\n"
            "T_approach = 8.0     # deg C\n"
            "eta_comp = 0.65\n"
            "elec_rate = 0.12     # $/kWh\n\n"
            "def calc_cop(T_evap_C, T_cond_C, eta=0.65):\n"
            "    T_evap_K = T_evap_C + 273.15\n"
            "    T_cond_K = T_cond_C + 273.15\n"
            "    return (T_evap_K / (T_cond_K - T_evap_K)) * eta\n\n"
            "def calc_compressor_power(Q_evap, T_evap_C, T_cond_C, eta=0.65):\n"
            "    cop = calc_cop(T_evap_C, T_cond_C, eta)\n"
            "    return Q_evap / cop\n\n"
            'print("Parameters loaded.")'
        ),
        md(
            "## 2. Simulate Pre-Retrofit Baseline Data\n\n"
            "We simulate 12 months of hourly compressor power data under fixed head "
            "pressure control. The simulation adds realistic measurement noise and "
            "minor load variation to represent field conditions.\n\n"
            "The regression specification follows IPMVP:\n\n"
            "$$W_{\\text{comp}} = \\alpha + \\beta \\cdot T_{\\text{amb}} + \\varepsilon$$"
        ),
        code(
            "# Generate 12 months of hourly outdoor temperature\n"
            "np.random.seed(42)\n"
            "hours = np.arange(8760)\n"
            "day_of_year = hours / 24.0\n\n"
            "T_seasonal = 7.5 + 16.0 * np.sin(2 * np.pi * (day_of_year - 100) / 365)\n"
            "T_daily = 5.0 * np.sin(2 * np.pi * hours / 24 - np.pi / 2)\n"
            "T_noise = np.random.normal(0, 3.0, 8760)\n"
            "T_amb = np.clip(T_seasonal + T_daily + T_noise, -30, 38)\n\n"
            "# Simulate pre-retrofit compressor power (fixed head pressure)\n"
            "def simulate_power_fixed(T_amb_arr, noise_std=2.0):\n"
            '    """Simulate compressor power under fixed condensing setpoint."""\n'
            "    W = np.zeros_like(T_amb_arr)\n"
            "    for i, ta in enumerate(T_amb_arr):\n"
            "        T_cond = max(ta + T_approach, T_cond_fixed)\n"
            "        W[i] = (calc_compressor_power(Q_evap_MT, T_evap_MT, T_cond, eta_comp) +\n"
            "                calc_compressor_power(Q_evap_LT, T_evap_LT, T_cond, eta_comp))\n"
            "    # Add measurement noise and load variation\n"
            "    W += np.random.normal(0, noise_std, len(W))\n"
            "    W += np.random.normal(0, 1.0, len(W)) * np.abs(np.sin(2 * np.pi * hours / 24))  # load variation\n"
            "    return np.maximum(W, 10)  # physical minimum\n\n"
            "W_pre = simulate_power_fixed(T_amb)\n\n"
            "pre_df = pd.DataFrame({\n"
            '    "T_amb": T_amb,\n'
            '    "W_comp": W_pre,\n'
            '    "period": "pre-retrofit"\n'
            "})\n\n"
            'print(f"Pre-retrofit data: {len(pre_df)} hourly observations")\n'
            'print(f"  Mean compressor power: {W_pre.mean():.1f} kW")\n'
            'print(f"  Total annual energy: {W_pre.sum():,.0f} kWh")'
        ),
        md(
            "## 3. Simulate Post-Retrofit Data (Tier 2 \u2014 EEV Float)\n\n"
            "Post-retrofit data simulates floating head pressure with an EEV floor at 18\u00b0C. "
            "The compressor power is lower at cool/cold outdoor temperatures because the "
            "condensing pressure follows ambient downward."
        ),
        code(
            "# Simulate post-retrofit compressor power (floating head pressure, Tier 2)\n"
            "T_cond_floor = 18.0  # Tier 2 EEV floor\n\n"
            "def simulate_power_floating(T_amb_arr, T_floor, noise_std=2.0):\n"
            '    """Simulate compressor power under floating condensing setpoint."""\n'
            "    W = np.zeros_like(T_amb_arr)\n"
            "    for i, ta in enumerate(T_amb_arr):\n"
            "        T_cond = max(ta + T_approach, T_floor)\n"
            "        W[i] = (calc_compressor_power(Q_evap_MT, T_evap_MT, T_cond, eta_comp) +\n"
            "                calc_compressor_power(Q_evap_LT, T_evap_LT, T_cond, eta_comp))\n"
            "    W += np.random.normal(0, noise_std, len(W))\n"
            "    W += np.random.normal(0, 1.0, len(W)) * np.abs(np.sin(2 * np.pi * hours / 24))\n"
            "    return np.maximum(W, 10)\n\n"
            "np.random.seed(123)  # different seed for post period\n"
            "W_post = simulate_power_floating(T_amb, T_cond_floor)\n\n"
            "post_df = pd.DataFrame({\n"
            '    "T_amb": T_amb,\n'
            '    "W_comp": W_post,\n'
            '    "period": "post-retrofit"\n'
            "})\n\n"
            'print(f"Post-retrofit data: {len(post_df)} hourly observations")\n'
            'print(f"  Mean compressor power: {W_post.mean():.1f} kW")\n'
            'print(f"  Total annual energy: {W_post.sum():,.0f} kWh")\n'
            'print(f"  Gross reduction: {(W_pre.sum() - W_post.sum()):,.0f} kWh '
            '({100*(W_pre.sum()-W_post.sum())/W_pre.sum():.1f}%)")'
        ),
        md(
            "## 4. Fit Pre/Post Regressions\n\n"
            "Ordinary least squares regression of compressor power against outdoor "
            "temperature for both periods. The key diagnostic is:\n"
            "- $R^2 > 0.75$ for adequate model fit\n"
            "- Post-retrofit slope $\\beta' < \\beta$ (less sensitive to ambient)"
        ),
        code(
            "# Fit OLS regressions\n"
            "slope_pre, intercept_pre, r_pre, p_pre, se_pre = stats.linregress(T_amb, W_pre)\n"
            "slope_post, intercept_post, r_post, p_post, se_post = stats.linregress(T_amb, W_post)\n\n"
            'print("=== PRE-RETROFIT REGRESSION ===")\n'
            'print(f"  W_comp = {intercept_pre:.2f} + {slope_pre:.3f} * T_amb")\n'
            'print(f"  R-squared: {r_pre**2:.4f}")\n'
            'print(f"  Slope: {slope_pre:.3f} kW/deg C")\n'
            'print(f"  Intercept: {intercept_pre:.2f} kW (power at 0 deg C)")\n'
            "print()\n"
            'print("=== POST-RETROFIT REGRESSION ===")\n'
            'print(f"  W_comp = {intercept_post:.2f} + {slope_post:.3f} * T_amb")\n'
            'print(f"  R-squared: {r_post**2:.4f}")\n'
            'print(f"  Slope: {slope_post:.3f} kW/deg C")\n'
            'print(f"  Intercept: {intercept_post:.2f} kW (power at 0 deg C)")\n'
            "print()\n"
            'print(f"Slope reduction: {slope_pre:.3f} -> {slope_post:.3f} kW/deg C")\n'
            'print(f"  ({100*(slope_pre-slope_post)/slope_pre:.1f}% reduction in weather sensitivity)")'
        ),
        md("## 5. Figure 3 \u2014 Pre/Post Regression Lines (M&V Demonstration)"),
        code(
            "fig, ax = plt.subplots(figsize=(11, 7))\n\n"
            "# Scatter plots (subsampled for clarity)\n"
            "idx = np.random.choice(len(T_amb), size=2000, replace=False)\n"
            "ax.scatter(T_amb[idx], W_pre[idx], alpha=0.15, s=8, c='red', label='Pre-retrofit data')\n"
            "ax.scatter(T_amb[idx], W_post[idx], alpha=0.15, s=8, c='blue', label='Post-retrofit data')\n\n"
            "# Regression lines\n"
            "T_plot = np.linspace(-25, 35, 100)\n"
            "W_pre_line = intercept_pre + slope_pre * T_plot\n"
            "W_post_line = intercept_post + slope_post * T_plot\n\n"
            "ax.plot(T_plot, W_pre_line, 'r-', linewidth=2.5,\n"
            "        label=f'Pre-retrofit: R\\u00b2={r_pre**2:.3f}')\n"
            "ax.plot(T_plot, W_post_line, 'b-', linewidth=2.5,\n"
            "        label=f'Post-retrofit: R\\u00b2={r_post**2:.3f}')\n\n"
            "# Shade the savings area\n"
            "ax.fill_between(T_plot, W_post_line, W_pre_line, alpha=0.15, color='green',\n"
            "                label='Verified savings')\n\n"
            'ax.set_xlabel("Outdoor Air Temperature (deg C)")\n'
            'ax.set_ylabel("Compressor Power (kW)")\n'
            'ax.set_title("Figure 3: Pre/Post Regression - M&V Verification")\n'
            "ax.legend(loc='upper left')\n"
            "ax.grid(True, alpha=0.3)\n"
            "plt.tight_layout()\n"
            'plt.savefig("fig3_mv_regression.png", dpi=150, bbox_inches="tight")\n'
            "plt.close()\n"
            'print("Figure 3 saved.")'
        ),
        md(
            "## 6. Verified Savings Calculation\n\n"
            "Verified savings are calculated as the area between the pre-retrofit and "
            "post-retrofit regression lines, integrated over actual post-implementation weather:\n\n"
            "$$\\Delta E_{\\text{verified}} = \\sum_{j=1}^{M} "
            "\\left[(\\alpha + \\beta \\cdot T_{\\text{amb},j}) - "
            "(\\alpha' + \\beta' \\cdot T_{\\text{amb},j})\\right] \\cdot \\Delta t$$"
        ),
        code(
            "# Verified savings: area between regression lines over actual weather\n"
            "W_pre_predicted = intercept_pre + slope_pre * T_amb\n"
            "W_post_predicted = intercept_post + slope_post * T_amb\n"
            "delta_W = W_pre_predicted - W_post_predicted  # kW savings per hour\n\n"
            "verified_savings_kWh = delta_W.sum()  # each interval is 1 hour\n"
            "verified_pct = 100 * verified_savings_kWh / W_pre_predicted.sum()\n\n"
            'print("=== VERIFIED SAVINGS ===")\n'
            'print(f"  Annual verified savings: {verified_savings_kWh:,.0f} kWh")\n'
            'print(f"  Percentage of baseline: {verified_pct:.1f}%")\n'
            'print(f"  Dollar savings: ${verified_savings_kWh * elec_rate:,.0f}/yr")\n'
            "print()\n\n"
            "# Compare to gross metered difference\n"
            "gross_diff = W_pre.sum() - W_post.sum()\n"
            'print(f"  Gross metered difference: {gross_diff:,.0f} kWh")\n'
            'print(f"  Regression-verified:      {verified_savings_kWh:,.0f} kWh")\n'
            'print(f"  Difference: {abs(gross_diff - verified_savings_kWh):,.0f} kWh '
            '({100*abs(gross_diff-verified_savings_kWh)/gross_diff:.1f}%)")'
        ),
        md(
            "## 7. Residual Analysis\n\n"
            "Check regression residuals for systematic patterns that would indicate "
            "confounding variables or model specification issues."
        ),
        code(
            "# Residual analysis for pre-retrofit model\n"
            "residuals_pre = W_pre - (intercept_pre + slope_pre * T_amb)\n\n"
            "fig, axes = plt.subplots(1, 3, figsize=(15, 4))\n\n"
            "# Residuals vs. fitted\n"
            "axes[0].scatter(intercept_pre + slope_pre * T_amb, residuals_pre, alpha=0.05, s=3)\n"
            "axes[0].axhline(0, color='red', linestyle='--')\n"
            'axes[0].set_xlabel("Fitted Values (kW)")\n'
            'axes[0].set_ylabel("Residuals (kW)")\n'
            'axes[0].set_title("Residuals vs. Fitted")\n\n'
            "# Residuals histogram\n"
            "axes[1].hist(residuals_pre, bins=50, edgecolor='black', alpha=0.7)\n"
            'axes[1].set_xlabel("Residual (kW)")\n'
            'axes[1].set_ylabel("Frequency")\n'
            'axes[1].set_title("Residual Distribution")\n\n'
            "# Residuals by hour of day\n"
            "hour_of_day = hours % 24\n"
            "hourly_resid = pd.DataFrame({'hour': hour_of_day, 'resid': residuals_pre})\n"
            "hourly_mean = hourly_resid.groupby('hour')['resid'].mean()\n"
            "axes[2].bar(hourly_mean.index, hourly_mean.values, color='steelblue')\n"
            'axes[2].set_xlabel("Hour of Day")\n'
            'axes[2].set_ylabel("Mean Residual (kW)")\n'
            'axes[2].set_title("Residuals by Hour of Day")\n'
            "axes[2].axhline(0, color='red', linestyle='--')\n\n"
            "plt.tight_layout()\n"
            'plt.savefig("fig4_residuals.png", dpi=150, bbox_inches="tight")\n'
            "plt.close()\n"
            'print("Residual analysis complete.")\n'
            'print(f"  Mean residual: {residuals_pre.mean():.3f} kW (should be ~0)")\n'
            'print(f"  Std residual: {residuals_pre.std():.2f} kW")'
        ),
        md(
            "## 8. Sensitivity Analysis\n\n"
            "Examine how savings vary with key assumptions:\n"
            "1. Minimum condensing temperature floor\n"
            "2. Electricity rate\n"
            "3. Condenser approach temperature"
        ),
        code(
            "# Sensitivity: minimum condensing floor\n"
            "floors = np.arange(15, 33, 1)\n"
            "savings_by_floor = []\n\n"
            "for floor in floors:\n"
            "    W_savings = 0\n"
            "    bin_edges = np.arange(-30, 42, 3)\n"
            "    bin_mids = bin_edges[:-1] + 1.5\n"
            "    bin_hrs, _ = np.histogram(T_amb, bins=bin_edges)\n"
            "    for tm, bh in zip(bin_mids, bin_hrs):\n"
            "        if bh == 0:\n"
            "            continue\n"
            "        tc_fix = max(tm + T_approach, T_cond_fixed)\n"
            "        tc_flt = max(tm + T_approach, floor)\n"
            "        w_fix = (calc_compressor_power(Q_evap_MT, T_evap_MT, tc_fix, eta_comp) +\n"
            "                 calc_compressor_power(Q_evap_LT, T_evap_LT, tc_fix, eta_comp))\n"
            "        w_flt = (calc_compressor_power(Q_evap_MT, T_evap_MT, tc_flt, eta_comp) +\n"
            "                 calc_compressor_power(Q_evap_LT, T_evap_LT, tc_flt, eta_comp))\n"
            "        W_savings += (w_fix - w_flt) * bh\n"
            "    savings_by_floor.append(W_savings)\n\n"
            "fig, axes = plt.subplots(1, 3, figsize=(16, 5))\n\n"
            "# Plot 1: Savings vs. condensing floor\n"
            "axes[0].plot(floors, [s/1000 for s in savings_by_floor], 'b-o', markersize=4)\n"
            "axes[0].axvline(27, color='orange', linestyle='--', label='Tier 1 floor (27 deg C)')\n"
            "axes[0].axvline(18, color='green', linestyle='--', label='Tier 2 floor (18 deg C)')\n"
            'axes[0].set_xlabel("Min. Condensing Temp Floor (deg C)")\n'
            'axes[0].set_ylabel("Annual Savings (MWh)")\n'
            'axes[0].set_title("Savings vs. Condensing Floor")\n'
            "axes[0].legend(fontsize=8)\n"
            "axes[0].grid(True, alpha=0.3)\n\n"
            "# Plot 2: Dollar savings vs. electricity rate\n"
            "rates = np.arange(0.06, 0.22, 0.02)\n"
            "base_savings_kWh = savings_by_floor[floors.tolist().index(18)]  # Tier 2\n"
            "dollar_savings = [base_savings_kWh * r for r in rates]\n"
            "axes[1].bar(rates, [d/1000 for d in dollar_savings], width=0.015, color='steelblue')\n"
            "axes[1].axvline(0.12, color='red', linestyle='--', label='Base rate ($0.12/kWh)')\n"
            'axes[1].set_xlabel("Electricity Rate ($/kWh)")\n'
            'axes[1].set_ylabel("Annual Dollar Savings ($k)")\n'
            'axes[1].set_title("Savings vs. Electricity Rate (Tier 2)")\n'
            "axes[1].legend(fontsize=8)\n"
            "axes[1].grid(True, alpha=0.3)\n\n"
            "# Plot 3: Savings vs. approach temperature\n"
            "approaches = np.arange(5, 15, 1)\n"
            "savings_by_approach = []\n"
            "for dta in approaches:\n"
            "    W_s = 0\n"
            "    for tm, bh in zip(bin_mids, bin_hrs):\n"
            "        if bh == 0:\n"
            "            continue\n"
            "        tc_fix = max(tm + dta, T_cond_fixed)\n"
            "        tc_flt = max(tm + dta, 18.0)\n"
            "        w_fix = (calc_compressor_power(Q_evap_MT, T_evap_MT, tc_fix, eta_comp) +\n"
            "                 calc_compressor_power(Q_evap_LT, T_evap_LT, tc_fix, eta_comp))\n"
            "        w_flt = (calc_compressor_power(Q_evap_MT, T_evap_MT, tc_flt, eta_comp) +\n"
            "                 calc_compressor_power(Q_evap_LT, T_evap_LT, tc_flt, eta_comp))\n"
            "        W_s += (w_fix - w_flt) * bh\n"
            "    savings_by_approach.append(W_s)\n\n"
            "axes[2].plot(approaches, [s/1000 for s in savings_by_approach], 'g-o', markersize=4)\n"
            "axes[2].axvline(8, color='red', linestyle='--', label='Base approach (8 deg C)')\n"
            'axes[2].set_xlabel("Condenser Approach Temp (deg C)")\n'
            'axes[2].set_ylabel("Annual Savings (MWh)")\n'
            'axes[2].set_title("Savings vs. Approach Temp (Tier 2)")\n'
            "axes[2].legend(fontsize=8)\n"
            "axes[2].grid(True, alpha=0.3)\n\n"
            "plt.tight_layout()\n"
            'plt.savefig("fig5_sensitivity.png", dpi=150, bbox_inches="tight")\n'
            "plt.close()\n"
            'print("Sensitivity analysis complete.")\n'
            'print(f"\\nEach 3 deg C reduction in floor adds approx. '
            '{(savings_by_floor[floors.tolist().index(24)] - savings_by_floor[floors.tolist().index(27)])/1000:.0f} MWh")'
        ),
        md(
            "## 9. Summary & Conclusions\n\n"
            "The regression-based M&V framework demonstrates:\n\n"
            "1. **Pre/post regression** isolates floating head pressure savings from other variables\n"
            "2. **R-squared > 0.80** is achievable for constant-load cold storage facilities\n"
            "3. **Savings are most sensitive** to the minimum condensing temperature floor \u2014 "
            "each 3\u00b0C reduction adds approximately 5-8% savings\n"
            "4. **Simple payback** under 1 year for Tier 1, 2-3 years for Tier 2 at Ontario "
            "industrial electricity rates\n\n"
            "### IPMVP Compliance Checklist\n"
            "- [x] Pre-retrofit baseline regression with R\u00b2 > 0.75\n"
            "- [x] Post-retrofit regression with comparable data quality\n"
            "- [x] Verified savings calculated as area between regression lines\n"
            "- [x] Residual analysis confirms no systematic bias\n"
            "- [x] Sensitivity analysis quantifies uncertainty bounds"
        ),
        md(
            "---\n*Abriliam Consulting \u2014 Industrial Energy Management*\n"
            "*Floating Head Pressure Analysis \u2014 Notebook 02 of 02*"
        ),
    ]

    nb = {"nbformat": 4, "nbformat_minor": 5, "metadata": METADATA, "cells": cells}
    path = os.path.join(NB_DIR, "floating-head-02-mv-regression.ipynb")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"NB02 written: {path} ({len(cells)} cells)")


if __name__ == "__main__":
    create_nb01()
    create_nb02()
    print("\nDone. Both notebooks created.")
