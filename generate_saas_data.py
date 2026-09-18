"""
Synthetic B2B SaaS subscription and customer lifecycle data generator.
Generates 24 months of customer subscriptions, expansion, contraction, churn, and unit economics data.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_saas_dataset(num_accounts: int = 1200, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)

    tiers = {
        'Starter': {'base_mrr': 150, 'cac': 450, 'churn_prob': 0.045, 'expand_prob': 0.08},
        'Growth': {'base_mrr': 800, 'cac': 2400, 'churn_prob': 0.025, 'expand_prob': 0.15},
        'Enterprise': {'base_mrr': 3500, 'cac': 12000, 'churn_prob': 0.012, 'expand_prob': 0.22}
    }

    channels = ['Organic Inbound', 'Paid Search', 'Outbound Sales', 'Partner Referral']
    channel_cac_mult = {'Organic Inbound': 0.6, 'Paid Search': 1.2, 'Outbound Sales': 1.6, 'Partner Referral': 0.9}

    start_date = datetime(2023, 1, 1)
    records = []

    for account_id in range(1, num_accounts + 1):
        tier_choice = np.random.choice(['Starter', 'Growth', 'Enterprise'], p=[0.55, 0.35, 0.10])
        tier_info = tiers[tier_choice]

        channel = np.random.choice(channels, p=[0.35, 0.30, 0.20, 0.15])

        # Acquisition month between 0 and 23
        acq_month_offset = int(np.random.triangular(0, 8, 23))
        cohort_month = (start_date + timedelta(days=acq_month_offset * 30.5)).strftime('%Y-%m')

        base_cac = tier_info['cac'] * channel_cac_mult[channel] * np.random.uniform(0.85, 1.25)
        initial_mrr = tier_info['base_mrr'] * np.random.uniform(0.9, 1.1)

        current_mrr = initial_mrr
        is_churned = False
        churn_month = None
        churn_reason = None

        active_months = 0
        total_revenue = 0.0
        expansion_mrr = 0.0
        contraction_mrr = 0.0

        support_tickets = int(np.random.poisson(lam=2.5 if tier_choice == 'Starter' else 5.0))
        nps_score = int(np.clip(np.random.normal(loc=8 if tier_choice == 'Enterprise' else 7, scale=2), 0, 10))
        discount_pct = np.random.choice([0.0, 0.10, 0.20, 0.35], p=[0.5, 0.25, 0.15, 0.10])

        # Simulate each month following acquisition
        for m in range(acq_month_offset, 24):
            month_str = (start_date + timedelta(days=m * 30.5)).strftime('%Y-%m')

            if is_churned:
                break

            active_months += 1
            total_revenue += current_mrr * (1 - discount_pct)

            # Monthly event: Churn, Expansion, Contraction, or Steady
            rand = np.random.rand()
            adjusted_churn = tier_info['churn_prob'] * (1.5 if discount_pct > 0.2 else 1.0) * (1.4 if nps_score < 6 else 0.8)

            if rand < adjusted_churn:
                is_churned = True
                churn_month = month_str
                churn_reason = np.random.choice([
                    'Price / Budget Cut', 'Switched to Competitor', 'Low Product Adoption',
                    'Missing Enterprise Features', 'Poor Onboarding Support'
                ], p=[0.30, 0.25, 0.20, 0.15, 0.10])
            elif rand < (adjusted_churn + tier_info['expand_prob']):
                # Expansion
                add_mrr = current_mrr * np.random.uniform(0.15, 0.40)
                expansion_mrr += add_mrr
                current_mrr += add_mrr
            elif rand < (adjusted_churn + tier_info['expand_prob'] + 0.04):
                # Contraction
                drop_mrr = current_mrr * np.random.uniform(0.10, 0.25)
                contraction_mrr += drop_mrr
                current_mrr = max(tier_info['base_mrr'] * 0.5, current_mrr - drop_mrr)

        records.append({
            'account_id': f"ACC-{account_id:04d}",
            'tier': tier_choice,
            'channel': channel,
            'cohort_month': cohort_month,
            'cac': round(base_cac, 2),
            'initial_mrr': round(initial_mrr, 2),
            'current_mrr': round(0.0 if is_churned else current_mrr, 2),
            'peak_mrr': round(current_mrr, 2),
            'expansion_mrr': round(expansion_mrr, 2),
            'contraction_mrr': round(contraction_mrr, 2),
            'is_churned': is_churned,
            'churn_month': churn_month,
            'churn_reason': churn_reason,
            'active_months': active_months,
            'total_lifetime_revenue': round(total_revenue, 2),
            'support_tickets_count': support_tickets,
            'nps_score': nps_score,
            'discount_pct': discount_pct
        })

    df = pd.DataFrame(records)
    return df

if __name__ == '__main__':
    df = generate_saas_dataset()
    df.to_csv('saas_customer_data.csv', index=False)
    print(f"Dataset generated: {len(df)} accounts saved to saas_customer_data.csv")
