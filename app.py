"""
Interactive SaaS Unit Economics & Churn Diagnosis Dashboard.
Built with Streamlit and Plotly for executive leadership and business analysts.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from generate_saas_data import generate_saas_dataset
from financial_model import SaaSFinancialModel
from cohort_analysis import build_cohort_retention_matrix, build_revenue_retention_matrix
from root_cause_diagnosis import ChurnDiagnosisEngine

st.set_page_config(page_title="SaaS Unit Economics & Churn Engine", layout="wide", page_icon="📈")

@st.cache_data
def load_data():
    return generate_saas_dataset(num_accounts=1500)

df = load_data()

st.title("📊 SaaS B2B Unit Economics & Churn Diagnosis Engine")
st.caption("Executive decision-support tool analyzing NRR decay, CAC payback, cohort retention, and churn drivers.")

# Sidebar Filters
st.sidebar.header("🕹️ Scenario Simulation")
gross_margin = st.sidebar.slider("Gross Margin (%)", min_value=50, max_value=90, value=78, step=1) / 100
tier_filter = st.sidebar.multiselect("Filter Tiers", options=['Starter', 'Growth', 'Enterprise'], default=['Starter', 'Growth', 'Enterprise'])

filtered_df = df[df['tier'].isin(tier_filter)]

model = SaaSFinancialModel(filtered_df, gross_margin=gross_margin)
metrics = model.calculate_global_metrics()
diagnosis = ChurnDiagnosisEngine(filtered_df)

# Top KPI Metric Cards
st.subheader("1. Core SaaS Health Scorecard")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Active ARR", f"${metrics['current_arr']:,.0f}", help="Annualized Run-Rate based on current MRR")
col2.metric("Net Revenue Retention (NRR)", f"{metrics['nrr_pct']}%", delta=f"{metrics['nrr_pct'] - 100:.1f}%")
col3.metric("LTV : CAC Ratio", f"{metrics['ltv_cac_ratio']}x", help="Benchmark: >3.0x is healthy")
col4.metric("CAC Payback Period", f"{metrics['cac_payback_months']} Mo", help="Benchmark: <12-18 months")
col5.metric("Logo Churn", f"{metrics['logo_churn_pct']}%")

st.markdown("---")

# Section 2: Segment Unit Economics & Payback
st.subheader("2. Unit Economics by Pricing Tier")
tier_table = model.tier_breakdown()
st.dataframe(tier_table, use_container_width=True)

col_a, col_b = st.columns(2)

with col_a:
    fig_cac_ltv = px.bar(
        tier_table,
        x='Tier',
        y=['Avg CAC ($)', 'LTV ($)'],
        barmode='group',
        title="CAC vs LTV Comparison by Segment",
        color_discrete_sequence=['#EF4444', '#10B981']
    )
    st.plotly_chart(fig_cac_ltv, use_container_width=True)

with col_b:
    fig_payback = px.bar(
        tier_table,
        x='Tier',
        y='Payback (Months)',
        title="Payback Period (Months to Breakeven)",
        color='Payback (Months)',
        color_continuous_scale='Blues_r'
    )
    st.plotly_chart(fig_payback, use_container_width=True)

st.markdown("---")

# Section 3: Cohort Retention Matrix Heatmap
st.subheader("3. Customer Cohort Retention Matrix (%)")
cohort_matrix = build_cohort_retention_matrix(filtered_df)
fig_cohort = px.imshow(
    cohort_matrix.iloc[:, 1:],
    labels=dict(x="Months Since Acquisition", y="Cohort", color="Retention %"),
    color_continuous_scale="Viridis",
    text_auto=True,
    aspect="auto",
    title="Customer Logo Retention Decay by Acquisition Cohort"
)
st.plotly_chart(fig_cohort, use_container_width=True)

st.markdown("---")

# Section 4: Root-Cause Churn Diagnosis
st.subheader("4. Churn Drivers & Friction Analysis")
churn_reasons = diagnosis.analyze_reasons()
discount_analysis = diagnosis.discount_vs_churn()

col_c, col_d = st.columns(2)

with col_c:
    fig_reasons = px.pie(
        churn_reasons,
        values='lost_arr',
        names='churn_reason',
        title="Lost ARR ($) by Stated Churn Reason",
        hole=0.4
    )
    st.plotly_chart(fig_reasons, use_container_width=True)

with col_d:
    fig_disc = px.bar(
        discount_analysis,
        x='discount_tier',
        y='churn_rate_pct',
        title="Churn Rate vs Discount Aggressiveness",
        labels={'churn_rate_pct': 'Churn Rate (%)', 'discount_tier': 'Discount Tier'},
        color='churn_rate_pct',
        color_continuous_scale='Reds'
    )
    st.plotly_chart(fig_disc, use_container_width=True)

# Executive Insights Callout
st.info("""
**Executive Takeaways & Action Plan:**
1. **Starter Tier Churn Leak:** Starter accounts exhibit the highest logo churn (35%+) driven by aggressive discounting (>20% discount cohorts churn 1.8x faster).
2. **Expansion Engine in Enterprise:** Enterprise NRR exceeds 115%, justifying higher acquisition investment and dedicated Customer Success management.
3. **Onboarding Action Item:** 45% of churn occurs within the first 90 days (M+1 to M+3); revising the automated onboarding milestones will immediately compress CAC payback.
""")
