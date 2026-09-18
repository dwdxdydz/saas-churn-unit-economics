"""
Cohort Retention and Revenue Matrix Analysis Module.
Builds monthly customer and revenue cohort retention matrices and decay curves.
"""

import pandas as pd
import numpy as np

def build_cohort_retention_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes cohort retention percentage matrix by month offset.
    Index: Cohort Month (YYYY-MM)
    Columns: Months Active (Month 0, Month 1, Month 2, ...)
    """
    cohort_data = []

    # Get unique sorted cohort months
    cohorts = sorted(df['cohort_month'].unique())

    for cohort in cohorts:
        cohort_df = df[df['cohort_month'] == cohort]
        cohort_size = len(cohort_df)
        if cohort_size == 0:
            continue

        row = {'Cohort': cohort, 'Cohort Size': cohort_size}

        # Calculate retention at each month
        for m in range(12):
            retained = len(cohort_df[cohort_df['active_months'] >= (m + 1)])
            retention_rate = (retained / cohort_size) * 100 if cohort_size > 0 else 0
            row[f"M+{m}"] = round(retention_rate, 1)

        cohort_data.append(row)

    matrix_df = pd.DataFrame(cohort_data)
    matrix_df.set_index('Cohort', inplace=True)
    return matrix_df

def build_revenue_retention_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Net Revenue Retention (NRR %) matrix by cohort over time.
    Accounts for expansion and contraction.
    """
    cohorts = sorted(df['cohort_month'].unique())
    cohort_data = []

    for cohort in cohorts:
        cohort_df = df[df['cohort_month'] == cohort]
        base_revenue = cohort_df['initial_mrr'].sum()
        if base_revenue == 0:
            continue

        row = {'Cohort': cohort, 'Base MRR ($)': round(base_revenue, 2)}

        for m in range(12):
            active_at_m = cohort_df[cohort_df['active_months'] >= (m + 1)]
            curr_rev = active_at_m['current_mrr'].sum()
            nrr_rate = (curr_rev / base_revenue) * 100 if base_revenue > 0 else 0
            row[f"M+{m}"] = round(nrr_rate, 1)

        cohort_data.append(row)

    matrix_df = pd.DataFrame(cohort_data)
    matrix_df.set_index('Cohort', inplace=True)
    return matrix_df
