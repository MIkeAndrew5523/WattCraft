"""
Fix all 7 split notebooks for independent execution, then run and render them.

Fixes applied:
1. matplotlib.use('Agg') in all notebooks before any pyplot import
2. Notebook 01: simplified CSV export path
3. Notebooks 02,04,06: add create_spline() function + needed spline vars
4. Notebook 03: extract df columns to bare arrays (oat, chiller_kw, etc.)
5. Notebook 04: remove forward-reference to d["cluster"]
6. Notebook 07: compute chiller_kw_per_ton column
"""

import json
import os
import subprocess
import sys

NB_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'notebooks')
NB_DIR = os.path.abspath(NB_DIR)

# ── Helper: make a code cell ──────────────────────────────────────────
def make_cell(source):
    return {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "execution_count": None,
        "source": source.strip().splitlines(keepends=True)
    }

# ── Shared code snippets ─────────────────────────────────────────────

AGG_BACKEND = """\
import matplotlib
matplotlib.use('Agg')
"""

CREATE_SPLINE_FUNC = """\
import numpy as np

def create_spline(x, y, num_points=300):
    \"\"\"Create smooth interpolation for plotting (uses numpy interp).\"\"\"
    mask = np.isfinite(x) & np.isfinite(y)
    x_clean, y_clean = np.array(x)[mask], np.array(y)[mask]
    if len(x_clean) < 4:
        return x_clean, y_clean
    x_new = np.linspace(x_clean.min(), x_clean.max(), num_points)
    y_new = np.interp(x_new, x_clean, y_clean)
    return x_new, y_new
"""

SPLINE_VARS_COMMON = """\
# Compute spline variables from df
time_numeric = (df.index - df.index[0]).total_seconds().values
time_spline, _ = create_spline(time_numeric, time_numeric)
"""

EXTRACT_ARRAYS = """\
# Extract columns as bare arrays for regression cells
oat = df['oat_C'].values
chiller_kw = df['chiller_kw'].values
plant_kw = df['plant_kw'].values
tons = df['tons'].values
occ = df['occ'].values
"""

COMPUTE_KW_PER_TON = """\
# Compute derived columns needed for this notebook
df['chiller_kw_per_ton'] = df['chiller_kw'] / df['tons']
"""

# ── Load, patch, and save each notebook ───────────────────────────────

def load_nb(fname):
    path = os.path.join(NB_DIR, fname)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_nb(fname, nb):
    path = os.path.join(NB_DIR, fname)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

def inject_after_markdown(nb, *code_snippets):
    """Insert code cells right after the first markdown cell (the intro)."""
    insert_idx = 1  # default: after cell 0
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'markdown':
            insert_idx = i + 1
            break
    for j, snippet in enumerate(reversed(code_snippets)):
        nb['cells'].insert(insert_idx, make_cell(snippet))

def inject_agg_into_imports(nb):
    """Add matplotlib.use('Agg') into the first code cell that imports matplotlib."""
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        src = ''.join(cell.get('source', []))
        if 'matplotlib' in src and 'matplotlib.use' not in src:
            # Prepend Agg backend
            cell['source'] = AGG_BACKEND.splitlines(keepends=True) + cell.get('source', [])
            return
    # Fallback: insert as new cell after markdown
    inject_after_markdown(nb, AGG_BACKEND)

def replace_scipy_spline(nb):
    """Replace make_interp_spline with np.interp in all cells (scipy hangs on large arrays)."""
    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            continue
        src = ''.join(cell.get('source', []))
        if 'make_interp_spline' in src:
            new_src = src.replace(
                'from scipy.interpolate import make_interp_spline\n', ''
            ).replace(
                'from scipy.interpolate import make_interp_spline', ''
            )
            # Replace spline calls: spl = make_interp_spline(x, y, k=3); ... spl(x_new)
            # with: y_new = np.interp(x_new, x, y)
            # This is a simple text replacement for the common pattern
            import re
            new_src = re.sub(
                r'(\w+)\s*=\s*make_interp_spline\((\w+),\s*(\w+)(?:,\s*k=\d+)?\)',
                r'# Using np.interp instead of make_interp_spline\n    \1 = lambda x_q, _x=\2, _y=\3: np.interp(x_q, _x, _y)',
                new_src
            )
            cell['source'] = new_src.splitlines(keepends=True)


# ── Fix each notebook ─────────────────────────────────────────────────

def fix_nb01():
    """Fix CSV export path."""
    print("Fixing 01...", end=" ", flush=True)
    nb = load_nb('01-chiller-plant-data-generation.ipynb')
    inject_agg_into_imports(nb)
    replace_scipy_spline(nb)
    # Fix the export cell (last cell)
    for cell in nb['cells']:
        src = ''.join(cell.get('source', []))
        if 'to_csv' in src:
            cell['source'] = [
                "# Export dataset for use in subsequent notebooks\n",
                "df.to_csv('chiller_plant_data.csv')\n",
                "print(f'Exported {len(df)} rows to chiller_plant_data.csv')\n",
            ]
    save_nb('01-chiller-plant-data-generation.ipynb', nb)
    print("OK")

def fix_nb02():
    """Add create_spline + spline vars."""
    print("Fixing 02...", end=" ", flush=True)
    nb = load_nb('02-exploratory-data-analysis.ipynb')
    inject_agg_into_imports(nb)
    replace_scipy_spline(nb)

    spline_vars_02 = SPLINE_VARS_COMMON + """\
_, cw_flow_spline = create_spline(time_numeric, df['cw_flow_m3h'].values)
_, kw_per_ton_spline = create_spline(time_numeric, df['kw_per_ton'].values)
"""
    # Insert spline setup after the data-loading cell
    # Find the CSV load cell
    for i, cell in enumerate(nb['cells']):
        src = ''.join(cell.get('source', []))
        if 'read_csv' in src:
            nb['cells'].insert(i + 1, make_cell(CREATE_SPLINE_FUNC + spline_vars_02))
            break

    save_nb('02-exploratory-data-analysis.ipynb', nb)
    print("OK")

def fix_nb03():
    """Add array extraction from df."""
    print("Fixing 03...", end=" ", flush=True)
    nb = load_nb('03-regression-modeling.ipynb')
    inject_agg_into_imports(nb)
    replace_scipy_spline(nb)

    spline_vars_03 = SPLINE_VARS_COMMON + """\
_, chw_flow_spline = create_spline(time_numeric, df['chw_flow_m3h'].values)
_, chw_dt_spline = create_spline(time_numeric, df['chw_dT_C'].values)
_, cw_flow_spline = create_spline(time_numeric, df['cw_flow_m3h'].values)
_, cw_dt_spline = create_spline(time_numeric, df['cw_dT_C'].values)
_, oat_spline = create_spline(time_numeric, df['oat_C'].values)
_, kw_per_ton_spline = create_spline(time_numeric, df['kw_per_ton'].values)
"""
    # Insert after CSV load cell
    for i, cell in enumerate(nb['cells']):
        src = ''.join(cell.get('source', []))
        if 'read_csv' in src:
            nb['cells'].insert(i + 1, make_cell(EXTRACT_ARRAYS))
            nb['cells'].insert(i + 2, make_cell(CREATE_SPLINE_FUNC + spline_vars_03))
            break

    save_nb('03-regression-modeling.ipynb', nb)
    print("OK")

def fix_nb04():
    """Add create_spline, remove d['cluster'] forward reference."""
    print("Fixing 04...", end=" ", flush=True)
    nb = load_nb('04-hydraulic-regime-detection.ipynb')
    inject_agg_into_imports(nb)
    replace_scipy_spline(nb)

    # Insert spline setup after CSV load
    spline_vars_04 = SPLINE_VARS_COMMON
    for i, cell in enumerate(nb['cells']):
        src = ''.join(cell.get('source', []))
        if 'read_csv' in src:
            nb['cells'].insert(i + 1, make_cell(CREATE_SPLINE_FUNC + spline_vars_04))
            break

    # Remove lines referencing d["cluster"] in the hydraulic coefficient cell
    for cell in nb['cells']:
        src_lines = cell.get('source', [])
        src = ''.join(src_lines)
        if 'k_hyd' in src and 'cluster' in src:
            new_lines = []
            skip = False
            for line in src_lines:
                if 'cluster' in line or 'Cluster' in line:
                    skip = True
                    continue
                # Also skip continuation lines of cluster-related code
                if skip and line.strip().startswith(('d2[', 'ax2', 'for cl', 'mask', 'ax.hist')):
                    if 'cluster' in line.lower() or 'cl ' in line or 'cl,' in line:
                        continue
                skip = False
                new_lines.append(line)
            cell['source'] = new_lines

    save_nb('04-hydraulic-regime-detection.ipynb', nb)
    print("OK")

def fix_nb05():
    """Just add Agg backend."""
    print("Fixing 05...", end=" ", flush=True)
    nb = load_nb('05-low-delta-t-syndrome.ipynb')
    inject_agg_into_imports(nb)
    replace_scipy_spline(nb)
    save_nb('05-low-delta-t-syndrome.ipynb', nb)
    print("OK")

def fix_nb06():
    """Add create_spline + CW spline vars."""
    print("Fixing 06...", end=" ", flush=True)
    nb = load_nb('06-cooling-tower-performance.ipynb')
    inject_agg_into_imports(nb)
    replace_scipy_spline(nb)

    spline_vars_06 = SPLINE_VARS_COMMON + """\
_, cw_flow_spline = create_spline(time_numeric, df['cw_flow_m3h'].values)
_, cw_dt_spline = create_spline(time_numeric, df['cw_dT_C'].values)
"""
    for i, cell in enumerate(nb['cells']):
        src = ''.join(cell.get('source', []))
        if 'read_csv' in src:
            nb['cells'].insert(i + 1, make_cell(CREATE_SPLINE_FUNC + spline_vars_06))
            break

    save_nb('06-cooling-tower-performance.ipynb', nb)
    print("OK")

def fix_nb07():
    """Add chiller_kw_per_ton derived column."""
    print("Fixing 07...", end=" ", flush=True)
    nb = load_nb('07-plant-efficiency-summary.ipynb')
    inject_agg_into_imports(nb)
    replace_scipy_spline(nb)

    for i, cell in enumerate(nb['cells']):
        src = ''.join(cell.get('source', []))
        if 'read_csv' in src:
            nb['cells'].insert(i + 1, make_cell(COMPUTE_KW_PER_TON))
            break

    save_nb('07-plant-efficiency-summary.ipynb', nb)
    print("OK")


# ── Execute notebooks ─────────────────────────────────────────────────

def execute_notebook(fname):
    """Execute a single notebook using jupyter nbconvert."""
    print(f"Executing {fname}...", end=" ", flush=True)
    fpath = os.path.join(NB_DIR, fname)
    result = subprocess.run(
        [
            sys.executable, '-m', 'jupyter', 'nbconvert',
            '--to', 'notebook',
            '--execute',
            '--ExecutePreprocessor.timeout=300',
            '--ExecutePreprocessor.kernel_name=python3',
            '--output', fname,
            fpath,
        ],
        cwd=NB_DIR,
        capture_output=True,
        text=True,
        env={**os.environ, 'MPLBACKEND': 'Agg'},
        timeout=600,
    )
    if result.returncode != 0:
        print(f"FAILED")
        print(result.stderr[-500:] if result.stderr else "No stderr")
        return False
    print("OK")
    return True


def convert_to_html(fname):
    """Convert executed notebook to HTML."""
    print(f"Rendering {fname} -> HTML...", end=" ", flush=True)
    fpath = os.path.join(NB_DIR, fname)
    result = subprocess.run(
        [
            sys.executable, '-m', 'jupyter', 'nbconvert',
            '--to', 'html',
            '--no-input',  # Hide code cells, show only output
            fpath,
        ],
        cwd=NB_DIR,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        print(f"FAILED")
        print(result.stderr[-300:] if result.stderr else "No stderr")
        return False
    print("OK")
    return True


# ── Main ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 60)
    print("STEP 1: Fixing notebook dependencies")
    print("=" * 60)
    fix_nb01()
    fix_nb02()
    fix_nb03()
    fix_nb04()
    fix_nb05()
    fix_nb06()
    fix_nb07()

    print()
    print("=" * 60)
    print("STEP 2: Executing notebooks (01 first, then 02-07)")
    print("=" * 60)

    notebooks = sorted(f for f in os.listdir(NB_DIR) if f.endswith('.ipynb'))

    all_ok = True
    for fname in notebooks:
        if not execute_notebook(fname):
            all_ok = False
            print(f"\n*** Stopping: {fname} failed ***")
            break

    if all_ok:
        print()
        print("=" * 60)
        print("STEP 3: Converting to HTML")
        print("=" * 60)
        for fname in notebooks:
            convert_to_html(fname)

    print()
    print("=" * 60)
    if all_ok:
        print("ALL DONE — notebooks fixed, executed, and rendered!")
    else:
        print("PARTIAL — fix the failing notebook and re-run")
    print("=" * 60)
