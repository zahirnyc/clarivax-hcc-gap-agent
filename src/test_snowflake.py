from dotenv import load_dotenv
import snowflake.connector
import os

load_dotenv()

conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)

cursor = conn.cursor()
cursor.execute("""
    SELECT HCC_NAME, COUNT(*) as members, 
           ROUND(AVG(RAF_WEIGHT), 3) as avg_raf
    FROM MEMBER_CONDITIONS
    GROUP BY HCC_NAME
    ORDER BY members DESC
""")

print("HCC Condition Summary from Snowflake:")
print("-" * 50)
for row in cursor.fetchall():
    print(f"{row[0]:<40} Members: {row[1]:>4}  RAF: {row[2]}")

conn.close()
print("\nSnowflake connection successful!")