# SaaS / Subscription B2B Unit Economics & Churn Diagnosis Engine

A full-lifecycle B2B SaaS analytics and financial modeling engine built to diagnose Net Revenue Retention (NRR) leaks, calculate unit economics (CAC, LTV, Payback), and perform cohort retention decay analysis.

---

## 🎯 The Business Problem
Subscription businesses frequently struggle with declining Net Revenue Retention (NRR) without knowing whether the root cause is acquisition channel quality, price-tier mismatch, aggressive discounting traps, or onboarding friction. This system provides executive-level decision support through automated financial modeling and cohort diagnosis.

---

## 🏗️ Architecture & Pipeline

```
Synthetic B2B SaaS Lifecycle (24 Months)
                 │
  ┌──────────────┴──────────────┐
  ▼                             ▼
Financial Model Engine       Cohort Analysis Engine
• MRR / ARR Waterfall        • Logo Retention Decay
• CAC / LTV / Payback        • Net Revenue Retention Matrix
• NRR / GRR / Magic Number   • Expansion & Contraction
  │                             │
  └──────────────┬──────────────┘
                 ▼
     Root-Cause Churn Engine
     • Discount Friction Analysis
     • Onboarding Milestone Drop
     • NPS & Ticket Correlation
                 │
                 ▼
     Streamlit Executive Dashboard + 5-Slide Leadership Deck
```

---

## 📊 Core Capabilities

1. **SaaS Unit Economics Modeling:**
   - $\text{LTV} = \frac{\text{ARPU} \times \text{Gross Margin}}{\text{Monthly Churn Rate}}$
   - $\text{CAC Payback Period} = \frac{\text{CAC}}{\text{ARPU} \times \text{Gross Margin}}$
   - $\text{NRR} = \frac{\text{Beginning ARR} + \text{Expansion} - \text{Contraction} - \text{Churn}}{\text{Beginning ARR}} \times 100\%$
2. **Cohort Retention Heatmap:**
   - Visual triangular retention matrix mapping customer cohort survival from $M+0$ to $M+12$.
3. **Discount Sensitivity & Churn Correlation:**
   - Quantifies the impact of sales discounting on churn velocity.
4. **Interactive Dashboard:**
   - Built with Streamlit & Plotly for scenario simulation (adjustable gross margin, tier filters).

---

## 🚀 Quickstart

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run unit tests
pytest tests/

# 3. Launch interactive dashboard
streamlit run app.py
```

---

## 📂 Project Structure

```
├── generate_saas_data.py    # Synthetic customer lifecycle generator
├── financial_model.py       # Core SaaS metrics & tier economics
├── cohort_analysis.py       # Triangular cohort matrices (Logo & Revenue)
├── root_cause_diagnosis.py  # Churn driver & discount sensitivity engine
├── app.py                   # Streamlit executive dashboard
├── executive_deck/          # 5-slide markdown presentation for leadership
├── tests/                   # Pytest test suite
└── requirements.txt         # Project dependencies
```
