import pytest
import pandas as pd
from generate_saas_data import generate_saas_dataset
from financial_model import SaaSFinancialModel
from cohort_analysis import build_cohort_retention_matrix

@pytest.fixture
def sample_data():
    return generate_saas_dataset(num_accounts=200, seed=123)

def test_dataset_generation(sample_data):
    assert len(sample_data) == 200
    assert 'tier' in sample_data.columns
    assert 'initial_mrr' in sample_data.columns
    assert 'cac' in sample_data.columns

def test_financial_metrics_validity(sample_data):
    model = SaaSFinancialModel(sample_data, gross_margin=0.80)
    metrics = model.calculate_global_metrics()

    assert metrics['current_arr'] > 0
    assert metrics['ltv_cac_ratio'] > 0
    assert 0 <= metrics['logo_churn_pct'] <= 100
    assert metrics['cac_payback_months'] > 0

def test_tier_breakdown_structure(sample_data):
    model = SaaSFinancialModel(sample_data)
    tier_df = model.tier_breakdown()

    assert len(tier_df) > 0
    assert 'Tier' in tier_df.columns
    assert 'LTV:CAC' in tier_df.columns
    assert 'Payback (Months)' in tier_df.columns

def test_cohort_matrix_shape(sample_data):
    matrix = build_cohort_retention_matrix(sample_data)
    assert not matrix.empty
    assert 'Cohort Size' in matrix.columns
    assert 'M+0' in matrix.columns
