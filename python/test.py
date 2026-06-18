from db_connection import get_connection

try:
    engine = get_connection()

    with engine.connect() as conn:
        print("✅ Connection Successful!")

except Exception as e:
    print("❌ Connection Failed")
    print(e)