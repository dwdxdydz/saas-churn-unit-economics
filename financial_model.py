"""
SaaS Financial Modeling Engine:
Calculates key unit economics (CAC, LTV, LTV:CAC, CAC Payback, NRR, GRR, Quick Ratio, Magic Number).
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

class SaaSFinancialModel:
    def __init__(self, df: pd.DataFrame, gross_margin: float = 0.78):
        self.df = df
        self.gross_margin = gross_margin

    def calculate_global_metrics(self) -> Dict[str, Any]:
        """Calculates global SaaS health and unit economics metrics."""
        total_accounts = len(self.df)
        active_accounts = len(self.df[~self.df['is_churned']])
        churned_accounts = len(self.df[self.df['is_churned']])

        avg_cac = self.df['cac'].mean()
        avg_initial_mrr = self.df['initial_mrr'].mean()
        current_total_mrr = self.df['current_mrr'].sum()
        current_arr = current_total_mrr * 12

        # Churn rate (Logo)
        logo_churn_rate = churned_accounts / total_accounts if total_accounts > 0 else 0

        # LTV calculation = (ARPU * Gross Margin) / Churn Rate
        arpu = self.df['initial_mrr'].mean()
        avg_monthly_churn = logo_churn_rate / (self.df['active_months'].mean() or 1)
        ltv = (arpu * self.gross_margin) / (avg_monthly_churn if avg_monthly_churn > 0 else 0.02)

        ltv_cac_ratio = ltv / avg_cac if avg_cac > 0 else 0
        cac_payback_months = avg_cac / (avg_initial_mrr * self.gross_margin) if (avg_initial_mrr * self.gross_margin) > 0 else 0

        # Net Revenue Retention (NRR) and Gross Revenue Retention (GRR)
        # For active accounts, calculate expansion vs contraction
        starting_revenue_base = self.df['initial_mrr'].sum()
        expansion_revenue = self.df['expansion_mrr'].sum()
        contraction_revenue = self.df['contraction_mrr'].sum()
        churned_revenue = self.df[self.df['is_churned']]['initial_mrr'].sum()

        nrr = ((starting_revenue_base + expansion_revenue - contraction_revenue - churned_revenue) / starting_revenue_base * 100) if starting_revenue_base > 0 else 100
        grr = ((starting_revenue_base - contraction_revenue - churned_revenue) / starting_revenue_base * 100) if starting_revenue_base > 0 else 100

        quick_ratio = (expansion_revenue + starting_revenue_base) / (contraction_revenue + churned_revenue) if (contraction_revenue + churned_revenue) > 0 else 5.0

        return {
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'churned_accounts': churned_accounts,
            'current_mrr': round(current_total_mrr, 2),
            'current_arr': round(current_arr, 2),
            'avg_cac': round(avg_cac, 2),
            'estimated_ltv': round(ltv, 2),
            'ltv_cac_ratio': round(ltv_cac_ratio, 2),
            'cac_payback_months': round(cac_payback_months, 1),
            'nrr_pct': round(nrr, 1),
            'grr_pct': round(grr, 1),
            'logo_churn_pct': round(logo_churn_rate * 100, 1),
            'quick_ratio': round(quick_ratio, 2)
        }

    def tier_breakdown(self) -> pd.DataFrame:
        """Calculates unit economics segmented by pricing tier (Starter, Growth, Enterprise)."""
        grouped = self.df.groupby('tier')
        records = []

        for tier, group in grouped:
            total_acc = len(group)
            churned = len(group[group['is_churned']])
            logo_churn = (churned / total_acc * 100) if total_acc > 0 else 0
            avg_cac = group['cac'].mean()
            avg_mrr = group['initial_mrr'].mean()

            arpu = avg_mrr
            monthly_churn = (churned / total_acc) / (group['active_months'].mean() or 1)
            ltv = (arpu * self.gross_margin) / (monthly_churn if monthly_churn > 0 else 0.015)
            ltv_cac = ltv / avg_cac if avg_cac > 0 else 0
            payback = avg_cac / (avg_mrr * self.gross_margin) if (avg_mrr * self.gross_margin) > 0 else 0

            # Tier NRR
            start_rev = group['initial_mrr'].sum()
            exp_rev = group['expansion_mrr'].sum()
            cnt_rev = group['contraction_mrr'].sum()
            churn_rev = group[group['is_churned']]['initial_mrr'].sum()

            tier_nrr = ((start_rev + exp_rev - cnt_rev - churn_rev) / start_rev * 100) if start_rev > 0 else 100

            records.append({
                'Tier': tier,
                'Accounts': total_acc,
                'Active MRR ($)': round(group['current_mrr'].sum(), 2),
                'Avg CAC ($)': round(avg_cac, 2),
                'LTV ($)': round(ltv, 2),
                'LTV:CAC': round(ltv_cac, 2),
                'Payback (Months)': round(payback, 1),
                'Logo Churn (%)': round(logo_churn, 1),
                'NRR (%)': round(tier_nrr, 1)
            })

        return pd.DataFrame(records).sort_values(by='Active MRR ($)', ascending=False)
