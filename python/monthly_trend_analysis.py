import pandas as pd
from db_connection import get_connection

engine = get_connection()

query = """
SELECT
    DATE_FORMAT(visit_date,'%%Y-%%m') AS month_year,
    ROUND(SUM(revenue_amount),2) AS revenue
FROM fact_visits
GROUP BY DATE_FORMAT(visit_date,'%%Y-%%m')
ORDER BY month_year
"""

df = pd.read_sql(query, engine)

df.to_csv(
    "output/monthly_trend.csv",
    index=False
)

print("Monthly trend report generated.")