"""
Root-Cause Churn Diagnosis and Pricing Friction Analysis.
Analyzes churn drivers across segments, discounts, NPS, and support volume.
"""

import pandas as pd
from typing import Dict, Any

class ChurnDiagnosisEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def analyze_reasons(self) -> pd.DataFrame:
        """Returns distribution of stated churn reasons and associated lost ARR."""
        churned = self.df[self.df['is_churned'] & self.df['churn_reason'].notna()]
        breakdown = churned.groupby('churn_reason').agg(
            churn_count=('account_id', 'count'),
            lost_mrr=('initial_mrr', 'sum')
        ).reset_index()

        breakdown['lost_arr'] = breakdown['lost_mrr'] * 12
        breakdown['pct_of_total_churn'] = (breakdown['churn_count'] / breakdown['churn_count'].sum()) * 100
        return breakdown.sort_values(by='lost_arr', ascending=False)

    def discount_vs_churn(self) -> pd.DataFrame:
        """Analyzes how aggressive discounting impacts retention."""
        grouped = self.df.groupby('discount_pct').agg(
            total_accounts=('account_id', 'count'),
            churned_accounts=('is_churned', lambda x: (x == True).sum()),
            avg_lifetime_revenue=('total_lifetime_revenue', 'mean')
        ).reset_index()

        grouped['churn_rate_pct'] = (grouped['churned_accounts'] / grouped['total_accounts']) * 100
        grouped['discount_tier'] = grouped['discount_pct'].apply(lambda d: f"{int(d*100)}% Discount" if d > 0 else "Full Price (0% Disc)")
        return grouped

    def nps_and_support_correlation(self) -> Dict[str, Any]:
        """Correlates support ticket volume and NPS with churn likelihood."""
        churned = self.df[self.df['is_churned']]
        retained = self.df[~self.df['is_churned']]

        return {
            'churned_avg_nps': round(churned['nps_score'].mean(), 1),
            'retained_avg_nps': round(retained['nps_score'].mean(), 1),
            'churned_avg_support_tickets': round(churned['support_tickets_count'].mean(), 1),
            'retained_avg_support_tickets': round(retained['support_tickets_count'].mean(), 1)
        }
