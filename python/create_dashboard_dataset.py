import pandas as pd
from db_connection import get_connection

engine = get_connection()

print("Connected to MySQL")

# =====================================================
# KPI SUMMARY
# =====================================================

kpi_query = """
SELECT
    ROUND(SUM(revenue_amount),2) AS total_revenue,
    COUNT(*) AS total_visits,
    COUNT(DISTINCT patient_id) AS unique_patients,
    ROUND(AVG(outcome_score),2) AS avg_outcome_score
FROM fact_visits
"""

kpi_df = pd.read_sql(kpi_query, engine)

kpi_df.to_csv(
    "output/kpi_summary.csv",
    index=False
)

print("kpi_summary.csv created")

# =====================================================
# CLINIC PERFORMANCE
# =====================================================

clinic_query = """
SELECT
    c.clinic_name,
    COUNT(*) AS total_visits,
    ROUND(SUM(f.revenue_amount),2) AS revenue,
    ROUND(AVG(f.outcome_score),2) AS avg_outcome_score
FROM fact_visits f
JOIN dim_clinic c
ON f.clinic_id = c.clinic_id
GROUP BY c.clinic_name
ORDER BY revenue DESC
"""

clinic_df = pd.read_sql(clinic_query, engine)

clinic_df.to_csv(
    "output/clinic_performance.csv",
    index=False
)

print("clinic_performance.csv created")

# =====================================================
# THERAPIST PERFORMANCE
# =====================================================

therapist_query = """
SELECT
    t.therapist_name,
    t.specialty,
    COUNT(*) AS total_visits,
    ROUND(SUM(f.revenue_amount),2) AS revenue,
    ROUND(AVG(f.outcome_score),2) AS avg_outcome_score
FROM fact_visits f
JOIN dim_therapist t
ON f.therapist_id = t.therapist_id
GROUP BY
    t.therapist_name,
    t.specialty
ORDER BY revenue DESC
"""

therapist_df = pd.read_sql(
    therapist_query,
    engine
)

therapist_df.to_csv(
    "output/therapist_performance.csv",
    index=False
)

print("therapist_performance.csv created")

# =====================================================
# MONTHLY REVENUE
# =====================================================

monthly_query = """
SELECT
    visit_date,
    revenue_amount
FROM fact_visits
"""

monthly_df = pd.read_sql(
    monthly_query,
    engine
)

monthly_df["visit_date"] = pd.to_datetime(
    monthly_df["visit_date"]
)

monthly_df["month_year"] = (
    monthly_df["visit_date"]
    .dt.strftime("%Y-%m")
)

monthly_summary = (
    monthly_df
    .groupby("month_year")["revenue_amount"]
    .sum()
    .reset_index()
)

monthly_summary.to_csv(
    "output/monthly_revenue.csv",
    index=False
)

print("monthly_revenue.csv created")

# =====================================================
# INSURANCE ANALYSIS
# =====================================================

insurance_query = """
SELECT
    i.insurance_name,
    COUNT(*) AS total_visits,
    ROUND(SUM(f.revenue_amount),2) AS revenue
FROM fact_visits f
JOIN dim_insurance i
ON f.insurance_id = i.insurance_id
GROUP BY i.insurance_name
ORDER BY revenue DESC
"""

insurance_df = pd.read_sql(
    insurance_query,
    engine
)

insurance_df.to_csv(
    "output/insurance_analysis.csv",
    index=False
)

print("insurance_analysis.csv created")

print("All dashboard datasets generated successfully")