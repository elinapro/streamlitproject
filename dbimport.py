import sqlite3
import pandas as pd

DB_NAME = 'WS_results.db'
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# cleaned file path
filepath = 'WS_results_clean.csv'


def infer_sqlite_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(series):
        return "REAL"
    else:
        return "TEXT"


try:
    table_name = 'WS_results'
    print(f"Importing {filepath} as table '{table_name}'")

    # Read the CSV
    df = pd.read_csv(filepath)

    # Build CREATE TABLE
    column_defs = ", ".join(
        f'"{col}" {infer_sqlite_type(df[col])}' for col in df.columns
    )
    create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({column_defs});'
    # drop if exists
    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}";')
    cursor.execute(create_table_sql)

    # Insert data using pandas to_sql
    df.to_sql(table_name, conn, if_exists='append', index=False)
    print(f"Imported done!")

except Exception as e:
    print(f"Error importing {filepath}: {e}")

# Finally
conn.commit()
conn.close()
print(f"\nAll done.")
