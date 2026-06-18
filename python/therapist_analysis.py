import pandas as pd
from db_connection import get_connection

engine = get_connection()

query = """
SELECT
    t.therapist_name,
    COUNT(*) AS total_visits,
    ROUND(SUM(f.revenue_amount),2) AS revenue,
    ROUND(AVG(f.outcome_score),2) AS avg_outcome_score
FROM fact_visits f
JOIN dim_therapist t
ON f.therapist_id = t.therapist_id
GROUP BY t.therapist_name
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)

df.to_csv(
    "output/therapist_performance.csv",
    index=False
)

print("Therapist report generated.")