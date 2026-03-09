"""Create 3 community envelope screening .ipynb notebooks."""
import json, os

def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": [source]}

def code(source):
    return {"cell_type": "code", "metadata": {}, "source": [source],
            "execution_count": None, "outputs": []}

def nb(cells):
    return {"nbformat": 4, "nbformat_minor": 5,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python", "version": "3.11.0"}},
            "cells": cells}

# --- Notebook 01: Data Acquisition & Exploratory Analysis ---
nb01 = nb([
    md("# 01 — Data Acquisition & Exploratory Analysis\n\nIngest aggregated natural gas consumption by postal code, regional HDD data, and MPAC property tax roll summaries. Filter to residential consumers and perform exploratory analysis on gas-temperature relationships."),
    md("## 1.1 — Environment Setup"),
    code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom pathlib import Path\n\nsns.set_theme(style='whitegrid', palette='colorblind')\nplt.rcParams['figure.figsize'] = (12, 6)\nplt.rcParams['figure.dpi'] = 100\n\nprint('Environment ready.')"),
    md("## 1.2 — Generate Synthetic Gas Consumption Data\n\nSimulate 150 postal codes × 24 months of residential natural gas consumption.\nEach postal code has a true thermal slope, baseload, and customer count."),
    code("""np.random.seed(42)

N_POSTAL = 150
N_MONTHS = 24
MONTHS = pd.date_range('2024-01-01', periods=N_MONTHS, freq='MS')

# Monthly HDD for southern Ontario (approximate)
hdd_template = np.array([650, 580, 480, 250, 80, 10, 0, 0, 30, 200, 400, 600])
hdd_monthly = np.tile(hdd_template, 2) + np.random.normal(0, 25, N_MONTHS)
hdd_monthly = np.maximum(hdd_monthly, 0)

# Postal code characteristics
postal_codes = [f'N2{chr(65+i//26)}{chr(65+i%26):1s}{np.random.randint(1,9)}{chr(65+np.random.randint(0,26))}{np.random.randint(0,9)}'
                for i in range(N_POSTAL)]

# True thermal slopes (GJ per HDD) — range from well-insulated to leaky
true_slopes = np.random.uniform(0.02, 0.12, N_POSTAL)
# Customer counts per postal code
customer_counts = np.random.randint(10, 40, N_POSTAL)
# Baseload (GJ/month — DHW, cooking)
baseloads = np.random.uniform(1.5, 4.0, N_POSTAL) * customer_counts

print(f'Generated {N_POSTAL} postal codes with {N_MONTHS} months of data.')
print(f'HDD range: {hdd_monthly.min():.0f} to {hdd_monthly.max():.0f}')"""),
    md("## 1.3 — Assemble Gas Consumption DataFrame"),
    code("""rows = []
for j, pc in enumerate(postal_codes):
    for i, month in enumerate(MONTHS):
        gas = (true_slopes[j] * customer_counts[j] * hdd_monthly[i]
               + baseloads[j]
               + np.random.normal(0, baseloads[j] * 0.15))
        gas = max(gas, baseloads[j] * 0.3)  # floor at minimal baseload
        rows.append({
            'postal_code': pc,
            'month': month,
            'gas_gj': round(gas, 2),
            'hdd': round(hdd_monthly[i], 1),
            'customer_count': customer_counts[j],
            'consumer_type': 'residential'
        })

gas_df = pd.DataFrame(rows)
print(f'Gas consumption DataFrame: {gas_df.shape}')
gas_df.head(10)"""),
    md("## 1.4 — Generate MPAC Property Tax Roll Summary\n\nSynthetic building stock characteristics per postal code: footprint, storeys, structure type, basement indicator."),
    code("""structure_types = ['detached', 'semi-detached', 'row', 'low-rise-apt']
type_weights = [0.50, 0.20, 0.25, 0.05]

mpac_rows = []
for j, pc in enumerate(postal_codes):
    stype = np.random.choice(structure_types, p=type_weights)
    storeys = np.random.choice([1, 1.5, 2, 2.5, 3],
                                p=[0.25, 0.15, 0.35, 0.15, 0.10])
    footprint = {'detached': np.random.uniform(80, 160),
                 'semi-detached': np.random.uniform(60, 120),
                 'row': np.random.uniform(45, 90),
                 'low-rise-apt': np.random.uniform(200, 500)}[stype]
    has_basement = np.random.choice([1.0, 0.5, 0.0], p=[0.55, 0.30, 0.15])

    mpac_rows.append({
        'postal_code': pc,
        'structure_type': stype,
        'avg_storeys': storeys,
        'avg_footprint_m2': round(footprint, 1),
        'basement_fraction': has_basement,
        'property_count': customer_counts[j],
        'true_slope': true_slopes[j],  # ground truth for validation
    })

mpac_df = pd.DataFrame(mpac_rows)
print(f'MPAC summary: {mpac_df.shape}')
mpac_df.head(10)"""),
    md("## 1.5 — Exploratory Analysis: Gas vs. HDD"),
    code("""# Pick 6 representative postal codes spanning the slope range
sorted_idx = np.argsort(true_slopes)
sample_idx = sorted_idx[np.linspace(0, N_POSTAL-1, 6, dtype=int)]
sample_pcs = [postal_codes[i] for i in sample_idx]

fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True, sharey=False)
for ax, pc in zip(axes.flat, sample_pcs):
    subset = gas_df[gas_df.postal_code == pc]
    ax.scatter(subset.hdd, subset.gas_gj, alpha=0.7, s=30)
    ax.set_title(pc, fontsize=10)
    ax.set_xlabel('Monthly HDD')
    ax.set_ylabel('Gas (GJ)')

plt.suptitle('Gas Consumption vs. HDD — Sample Postal Codes', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()"""),
    md("## 1.6 — Distribution of Customer Counts and Building Types"),
    code("""fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.hist(customer_counts, bins=20, edgecolor='black', alpha=0.7)
ax1.set_xlabel('Residential Customers per Postal Code')
ax1.set_ylabel('Count')
ax1.set_title('Customer Count Distribution')

mpac_df.structure_type.value_counts().plot.barh(ax=ax2, color='steelblue')
ax2.set_xlabel('Number of Postal Codes')
ax2.set_title('Dominant Structure Type')

plt.tight_layout()
plt.show()"""),
    md("## 1.7 — Monthly HDD Pattern"),
    code("fig, ax = plt.subplots(figsize=(12, 4))\nax.bar(range(N_MONTHS), hdd_monthly, color='coral', alpha=0.8)\nax.set_xticks(range(N_MONTHS))\nax.set_xticklabels([m.strftime('%b %y') for m in MONTHS], rotation=45, ha='right')\nax.set_ylabel('HDD18')\nax.set_title('Monthly Heating Degree Days - Regional Weather Station')\nplt.tight_layout()\nplt.show()"),
    md("## 1.8 — Save Intermediate Data"),
    code("gas_df.to_csv('data/ces_gas_consumption.csv', index=False)\nmpac_df.to_csv('data/ces_mpac_summary.csv', index=False)\nprint('Saved: ces_gas_consumption.csv, ces_mpac_summary.csv')"),
    md("---\n**Next:** Notebook 02 runs the HDD regression per postal code, normalizes by building stock, and produces the thermal intensity metric."),
])

# --- Notebook 02: HDD Regression & Normalization ---
nb02 = nb([
    md("# 02 — HDD Regression & Normalization\n\nRun OLS regression per postal code, apply quality filters, normalize slopes by building stock characteristics from the tax roll, and produce a thermal intensity metric for ranking."),
    md("## 2.1 — Load Data"),
    code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nfrom scipy import stats\n\nsns.set_theme(style='whitegrid', palette='colorblind')\n\ngas_df = pd.read_csv('data/ces_gas_consumption.csv', parse_dates=['month'])\nmpac_df = pd.read_csv('data/ces_mpac_summary.csv')\n\nprint(f'Gas data: {gas_df.shape}, MPAC data: {mpac_df.shape}')"),
    md("## 2.2 — Per-Postal-Code OLS Regression"),
    code("""results = []
for pc, group in gas_df.groupby('postal_code'):
    hdd = group.hdd.values
    gas = group.gas_gj.values

    slope, intercept, r_value, p_value, std_err = stats.linregress(hdd, gas)

    results.append({
        'postal_code': pc,
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_value**2,
        'p_value': p_value,
        'std_err': std_err,
        'n_obs': len(group),
    })

reg_df = pd.DataFrame(results)
print(f'Regressions complete: {len(reg_df)} postal codes')
reg_df.describe().round(4)"""),
    md("## 2.3 — Regression Quality Checks"),
    code("""# Quality filters
reg_df['pass_r2'] = reg_df.r_squared > 0.80
reg_df['pass_slope'] = reg_df.slope > 0
reg_df['pass_intercept'] = reg_df.intercept > 0
reg_df['pass_all'] = reg_df.pass_r2 & reg_df.pass_slope & reg_df.pass_intercept

n_pass = reg_df.pass_all.sum()
n_fail = (~reg_df.pass_all).sum()
print(f'Quality check: {n_pass} pass, {n_fail} flagged')

# R² distribution
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(reg_df.r_squared, bins=30, edgecolor='black', alpha=0.7)
ax.axvline(0.80, color='red', linestyle='--', label='R² threshold = 0.80')
ax.set_xlabel('R²')
ax.set_ylabel('Postal Codes')
ax.set_title('Regression R² Distribution')
ax.legend()
plt.tight_layout()
plt.show()"""),
    md("## 2.4 — Merge with MPAC Data and Compute Heated Volume"),
    code("""# Filter to passing postal codes
qualified = reg_df[reg_df.pass_all].merge(mpac_df, on='postal_code')

# Estimate heated volume per property
FLOOR_HEIGHT = 2.7  # m, above grade
BSMT_HEIGHT = 2.4   # m

qualified['above_grade_vol'] = (qualified.avg_footprint_m2
                                 * qualified.avg_storeys
                                 * FLOOR_HEIGHT)
qualified['below_grade_vol'] = (qualified.avg_footprint_m2
                                 * qualified.basement_fraction
                                 * BSMT_HEIGHT)
qualified['heated_vol_m3'] = qualified.above_grade_vol + qualified.below_grade_vol

print(f'Qualified postal codes: {len(qualified)}')
qualified[['postal_code', 'avg_footprint_m2', 'avg_storeys',
           'basement_fraction', 'heated_vol_m3']].describe().round(1)"""),
    md("## 2.5 — Normalize: Per-Property Slope and Thermal Intensity"),
    code("""# Per-property slope
qualified['slope_per_prop'] = qualified.slope / qualified.property_count

# Normalized thermal intensity: gas per HDD per m³ heated volume
qualified['thermal_intensity'] = qualified.slope_per_prop / qualified.heated_vol_m3

print('Thermal intensity statistics:')
qualified.thermal_intensity.describe().round(6)"""),
    md("## 2.6 — Effect of Normalization\n\nCompare raw slope ranking vs. normalized ranking — they should differ substantially."),
    code("""qualified['rank_raw'] = qualified.slope.rank(ascending=False).astype(int)
qualified['rank_normalized'] = qualified.thermal_intensity.rank(ascending=False).astype(int)

fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(qualified.rank_raw, qualified.rank_normalized, alpha=0.5, s=20)
ax.plot([0, len(qualified)], [0, len(qualified)], 'r--', alpha=0.5, label='No change')
ax.set_xlabel('Rank by Raw Slope')
ax.set_ylabel('Rank by Normalized Thermal Intensity')
ax.set_title('Normalization Changes the Ranking')
ax.legend()
plt.tight_layout()
plt.show()

# Rank correlation
from scipy.stats import spearmanr
rho, p = spearmanr(qualified.rank_raw, qualified.rank_normalized)
print(f'Spearman rank correlation: {rho:.3f} (p={p:.4f})')
print('Normalization materially reshuffles the ranking.')"""),
    md("## 2.7 — Thermal Intensity by Structure Type"),
    code("""fig, ax = plt.subplots(figsize=(10, 5))
for stype in ['detached', 'semi-detached', 'row', 'low-rise-apt']:
    subset = qualified[qualified.structure_type == stype]
    ax.hist(subset.thermal_intensity, bins=20, alpha=0.5, label=stype)

ax.set_xlabel('Normalized Thermal Intensity (GJ / HDD / m³)')
ax.set_ylabel('Postal Codes')
ax.set_title('Thermal Intensity Distribution by Structure Type')
ax.legend()
plt.tight_layout()
plt.show()"""),
    md("## 2.8 — Validate Against Ground Truth\n\nBecause this is synthetic data, we can check if the normalized metric correlates with the true slope."),
    code("""fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(qualified.true_slope, qualified.thermal_intensity, alpha=0.5, s=20)
ax.set_xlabel('True Thermal Slope (known ground truth)')
ax.set_ylabel('Normalized Thermal Intensity (computed)')
ax.set_title('Validation: Normalized Metric vs. Ground Truth')

rho, p = spearmanr(qualified.true_slope, qualified.thermal_intensity)
ax.text(0.05, 0.95, f'Spearman ρ = {rho:.3f}', transform=ax.transAxes, va='top',
        fontsize=12, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
plt.tight_layout()
plt.show()"""),
    md("## 2.9 — Save Results"),
    code("qualified.to_csv('data/ces_normalized_results.csv', index=False)\nprint(f'Saved {len(qualified)} qualified postal codes with thermal intensity.')"),
    md("---\n**Next:** Notebook 03 ranks postal codes, identifies priority neighbourhoods, and builds the targeting output."),
])

# --- Notebook 03: Neighbourhood Prioritization & Targeting ---
nb03 = nb([
    md("# 03 — Neighbourhood Prioritization & Targeting\n\nRank postal codes by normalized thermal intensity within structure type groups. Identify priority neighbourhoods for retrofit incentive targeting."),
    md("## 3.1 — Load Normalized Results"),
    code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\n\nsns.set_theme(style='whitegrid', palette='colorblind')\n\ndf = pd.read_csv('data/ces_normalized_results.csv')\nprint(f'Loaded {len(df)} qualified postal codes')"),
    md("## 3.2 — Within-Group Ranking and Priority Quartile"),
    code("""# Rank within each structure type group
df['group_rank'] = df.groupby('structure_type')['thermal_intensity'].rank(
    ascending=False, method='min').astype(int)
df['group_size'] = df.groupby('structure_type')['postal_code'].transform('count')
df['group_percentile'] = 1 - (df.group_rank - 1) / df.group_size

# Priority: top quartile within group
df['priority'] = df.group_percentile >= 0.75

n_priority = df.priority.sum()
print(f'Priority postal codes (top quartile): {n_priority} of {len(df)}')

# Summary by structure type
priority_summary = df.groupby('structure_type').agg(
    total=('postal_code', 'count'),
    priority=('priority', 'sum'),
    mean_intensity=('thermal_intensity', 'mean'),
    p75_intensity=('thermal_intensity', lambda x: x.quantile(0.75)),
).round(6)
print('\\nPriority summary by structure type:')
priority_summary"""),
    md("## 3.3 — Priority Postal Code Map\n\nVisualize which postal codes are flagged as priority vs. non-priority."),
    code("""fig, ax = plt.subplots(figsize=(14, 6))

# Sort by thermal intensity for visual clarity
plot_df = df.sort_values('thermal_intensity', ascending=False).reset_index(drop=True)

colors = ['#e74c3c' if p else '#95a5a6' for p in plot_df.priority]
ax.bar(range(len(plot_df)), plot_df.thermal_intensity, color=colors, width=1.0)
ax.set_xlabel('Postal Code (sorted by thermal intensity)')
ax.set_ylabel('Normalized Thermal Intensity')
ax.set_title('All Postal Codes — Red = Priority Quartile')

# Custom legend
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color='#e74c3c', label='Priority (top 25%)'),
                    Patch(color='#95a5a6', label='Non-priority')],
          loc='upper right')
plt.tight_layout()
plt.show()"""),
    md("## 3.4 — Priority Targeting Table"),
    code("""target_table = (df[df.priority]
    .sort_values('thermal_intensity', ascending=False)
    [['postal_code', 'structure_type', 'avg_storeys', 'avg_footprint_m2',
      'basement_fraction', 'property_count', 'thermal_intensity',
      'r_squared', 'group_rank']]
    .reset_index(drop=True))

target_table.index += 1
target_table.index.name = 'priority_rank'

print(f'Top 15 priority postal codes:')
target_table.head(15)"""),
    md("## 3.5 — Thermal Intensity Distribution: Priority vs. Non-Priority"),
    code("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# By priority flag
for label, color in [('Priority', '#e74c3c'), ('Non-priority', '#95a5a6')]:
    subset = df[df.priority == (label == 'Priority')]
    axes[0].hist(subset.thermal_intensity, bins=20, alpha=0.6, color=color, label=label)
axes[0].set_xlabel('Normalized Thermal Intensity')
axes[0].set_ylabel('Postal Codes')
axes[0].set_title('Distribution by Priority Status')
axes[0].legend()

# By structure type within priority
for stype in df.structure_type.unique():
    subset = df[(df.priority) & (df.structure_type == stype)]
    if len(subset) > 0:
        axes[1].hist(subset.thermal_intensity, bins=10, alpha=0.5, label=stype)
axes[1].set_xlabel('Normalized Thermal Intensity')
axes[1].set_title('Priority Postal Codes by Structure Type')
axes[1].legend()

plt.tight_layout()
plt.show()"""),
    md("## 3.6 — Sensitivity Analysis: Normalization Parameters\n\nHow sensitive is the ranking to the assumed basement heating fraction and floor height?"),
    code("""from scipy.stats import spearmanr

# Baseline ranking
baseline_rank = df.thermal_intensity.rank(ascending=False)

sensitivities = []
for bsmt_mult in [0.0, 0.25, 0.5, 0.75, 1.0]:
    for floor_h in [2.4, 2.7, 3.0]:
        above = df.avg_footprint_m2 * df.avg_storeys * floor_h
        below = df.avg_footprint_m2 * bsmt_mult * 2.4
        vol = above + below
        intensity = (df.slope / df.property_count) / vol
        rho, _ = spearmanr(baseline_rank, intensity.rank(ascending=False))
        sensitivities.append({
            'bsmt_fraction': bsmt_mult,
            'floor_height': floor_h,
            'rank_correlation': rho
        })

sens_df = pd.DataFrame(sensitivities)
print('Rank stability under parameter variation:')
print(f'Min Spearman rho: {sens_df.rank_correlation.min():.3f}')
print(f'Max Spearman rho: {sens_df.rank_correlation.max():.3f}')

pivot = sens_df.pivot(index='bsmt_fraction', columns='floor_height', values='rank_correlation')
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(pivot, annot=True, fmt='.3f', cmap='YlGn', ax=ax, vmin=0.9, vmax=1.0)
ax.set_title('Rank Stability: Spearman ρ vs. Baseline')
ax.set_xlabel('Floor Height (m)')
ax.set_ylabel('Basement Heating Fraction')
plt.tight_layout()
plt.show()"""),
    md("## 3.7 — Year-Over-Year Monitoring Potential\n\nIf the screening is refreshed annually, changes in postal code thermal intensity can serve as a macro-level M&V signal for neighbourhood-scale retrofit programs."),
    code("""# Simulate year 2 with slight improvement in priority postal codes
df['intensity_yr2'] = df.thermal_intensity * np.where(
    df.priority, np.random.uniform(0.90, 0.98, len(df)),
    np.random.uniform(0.97, 1.03, len(df)))

df['pct_change'] = (df.intensity_yr2 - df.thermal_intensity) / df.thermal_intensity * 100

fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df[~df.priority].thermal_intensity, df[~df.priority].pct_change,
           alpha=0.4, s=20, color='#95a5a6', label='Non-priority')
ax.scatter(df[df.priority].thermal_intensity, df[df.priority].pct_change,
           alpha=0.6, s=30, color='#e74c3c', label='Priority')
ax.axhline(0, color='black', linewidth=0.5)
ax.set_xlabel('Baseline Thermal Intensity')
ax.set_ylabel('Year-over-Year Change (%)')
ax.set_title('Simulated Annual Refresh — Priority Areas Show Improvement')
ax.legend()
plt.tight_layout()
plt.show()

print(f'Priority postal codes mean change: {df[df.priority].pct_change.mean():.1f}%')
print(f'Non-priority mean change: {df[~df.priority].pct_change.mean():.1f}%')"""),
    md("## 3.8 — Export Targeting Output"),
    code("# Full output\ncols = ['postal_code', 'structure_type', 'avg_storeys', 'avg_footprint_m2',\n        'basement_fraction', 'property_count', 'slope', 'r_squared',\n        'thermal_intensity', 'group_rank', 'group_percentile', 'priority']\noutput = df[cols]\noutput.to_csv('data/ces_targeting_output.csv', index=False)\n\n# Priority-only\ntarget_only = output[output.priority].sort_values('thermal_intensity', ascending=False)\ntarget_only.to_csv('data/ces_priority_postal_codes.csv', index=False)\n\nprint(f'Exported {len(output)} postal codes ({len(target_only)} priority)')"),
    md("---\n**Summary:** The screening identified the top quartile of postal codes by normalized thermal intensity within each structure type group. These neighbourhoods represent the strongest candidates for targeted retrofit incentive programs — where building envelopes are underperforming relative to their building stock characteristics, and where incentive dollars are most likely to produce measurable gas savings."),
])

# Write notebooks
outdir = os.path.join(os.path.dirname(__file__), '..', 'notebooks', 'source')
pubdir = os.path.join(os.path.dirname(__file__), '..', 'public', 'notebooks')

for d in [outdir, pubdir]:
    os.makedirs(d, exist_ok=True)

for name, notebook in [
    ('ces-01-data-acquisition.ipynb', nb01),
    ('ces-02-regression-normalization.ipynb', nb02),
    ('ces-03-neighbourhood-targeting.ipynb', nb03),
]:
    for d in [outdir, pubdir]:
        path = os.path.join(d, name)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1, ensure_ascii=False)
    print(f'Created: {name}')

print('Done.')
