import pandas as pd
from db_connection import get_connection

engine = get_connection()

query = """
SELECT
    patient_id,
    COUNT(*) AS total_visits
FROM fact_visits
GROUP BY patient_id
HAVING COUNT(*) > 1
ORDER BY total_visits DESC
"""

df = pd.read_sql(query, engine)

df.to_csv(
    "output/retention_report.csv",
    index=False
)

print("Retention report generated.")