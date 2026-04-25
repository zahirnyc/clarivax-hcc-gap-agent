import os
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()

def get_snowflake_connection():
    """Create and return a Snowflake connection."""
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

def query_member_conditions(member_id: str) -> str:
    """
    Query all HCC conditions for a specific member.
    Returns a formatted string summary.
    """
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                MEMBER_ID,
                AGE,
                GENDER,
                YEAR,
                HCC_CODE,
                HCC_NAME,
                ICD10_CODE,
                RAF_WEIGHT
            FROM MEMBER_CONDITIONS
            WHERE MEMBER_ID = %s
            ORDER BY YEAR DESC, RAF_WEIGHT DESC
        """, (member_id,))
        
        rows = cursor.fetchall()
        
        if not rows:
            return f"No conditions found for member {member_id}"
        
        result = f"Member {member_id} — Age: {rows[0][1]}, Gender: {rows[0][2]}\n"
        result += "-" * 50 + "\n"
        result += f"{'Year':<6} {'HCC':<6} {'Condition':<35} {'ICD-10':<10} {'RAF':>6}\n"
        result += "-" * 50 + "\n"
        
        total_raf = 0
        for row in rows:
            result += f"{row[3]:<6} {row[4]:<6} {row[5]:<35} {row[6]:<10} {row[7]:>6.3f}\n"
            total_raf += row[7]
        
        result += "-" * 50 + "\n"
        result += f"Total RAF Weight: {total_raf:.3f}\n"
        return result
        
    finally:
        conn.close()

def find_hcc_gaps(hcc_code: int) -> str:
    """
    Find members who have one HCC but may be missing 
    a related HCC — classic gap identification pattern.
    Returns top 10 members by RAF weight.
    """
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                a.MEMBER_ID,
                a.AGE,
                a.HCC_NAME as CODED_CONDITION,
                a.RAF_WEIGHT,
                a.YEAR
            FROM MEMBER_CONDITIONS a
            WHERE a.HCC_CODE = %s
            AND a.YEAR = 2023
            ORDER BY a.RAF_WEIGHT DESC
            LIMIT 10
        """, (hcc_code,))
        
        rows = cursor.fetchall()
        
        if not rows:
            return f"No members found with HCC {hcc_code}"
        
        result = f"Top 10 members with HCC {hcc_code}:\n"
        result += "-" * 55 + "\n"
        result += f"{'Member ID':<12} {'Age':<5} {'Condition':<30} {'RAF':>6}\n"
        result += "-" * 55 + "\n"
        
        for row in rows:
            result += f"{row[0]:<12} {row[1]:<5} {row[2]:<30} {row[3]:>6.3f}\n"
        
        return result
        
    finally:
        conn.close()

def get_population_summary() -> str:
    """
    Get a high-level summary of the full Medicare 
    member population — HCC distribution and RAF stats.
    """
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                HCC_CODE,
                HCC_NAME,
                COUNT(DISTINCT MEMBER_ID) as MEMBER_COUNT,
                ROUND(AVG(RAF_WEIGHT), 3) as AVG_RAF,
                ROUND(SUM(RAF_WEIGHT), 2) as TOTAL_RAF
            FROM MEMBER_CONDITIONS
            WHERE YEAR = 2023
            GROUP BY HCC_CODE, HCC_NAME
            ORDER BY MEMBER_COUNT DESC
        """)
        
        rows = cursor.fetchall()
        result = "Population HCC Summary (2023):\n"
        result += "-" * 65 + "\n"
        result += f"{'HCC':<6} {'Condition':<35} {'Members':<10} {'Avg RAF':>8}\n"
        result += "-" * 65 + "\n"
        
        for row in rows:
            result += f"{row[0]:<6} {row[1]:<35} {row[2]:<10} {row[3]:>8.3f}\n"
        
        return result
        
    finally:
        conn.close()


# ── Test all three functions ──────────────────────────
if __name__ == "__main__":
    print("TEST 1: Single member lookup")
    print("=" * 55)
    print(query_member_conditions("MBR00001"))

    print("\nTEST 2: Find members with Diabetes (HCC 19)")
    print("=" * 55)
    print(find_hcc_gaps(19))

    print("\nTEST 3: Full population summary")
    print("=" * 55)
    print(get_population_summary())