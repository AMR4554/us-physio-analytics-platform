from sqlalchemy import create_engine
from sqlalchemy.engine import URL

def get_connection():
    url = URL.create(
        drivername="mysql+pymysql",
        username="root",
        password="Abhishek1510",
        host="localhost",
        database="physio_analytics"
    )

    return create_engine(url)