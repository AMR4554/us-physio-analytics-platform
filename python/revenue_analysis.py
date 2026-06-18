import pandas as pd
from db_connection import get_connection

engine = get_connection()

query = """
SELECT
    c.clinic_name,
    ROUND(SUM(f.revenue_amount),2) AS revenue
FROM fact_visits f
JOIN dim_clinic c
ON f.clinic_id = c.clinic_id
GROUP BY c.clinic_name
ORDER BY revenue DESC
"""

df = pd.read_sql(query, engine)

print(df.head())

df.to_csv(
    "output/revenue_report.csv",
    index=False
)

print("Revenue report generated.")