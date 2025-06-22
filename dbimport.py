import sqlite3
import pandas as pd
import os
import glob


DB_NAME = os.path.join('WS_results.db')

# SQLite
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Function to infer column types for SQLite


def infer_sqlite_type(series):
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(series):
        return "REAL"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "TEXT"  # or use DATETIME with proper formatting
    else:
        return "TEXT"


# Loop over all CSV files in the directory
for filepath in glob.glob(os.path.join('*.csv')):
    try:
        table_name = os.path.splitext(os.path.basename(filepath))[0]
        print(f"Importing {filepath} as table '{table_name}'")

        # Read the CSV
        df = pd.read_csv(filepath)

        # Build CREATE TABLE with inferred types
        column_defs = ", ".join(
            f'"{col}" {infer_sqlite_type(df[col])}' for col in df.columns
        )
        create_table_sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({column_defs});'
        # optional: drop if exists
        cursor.execute(f'DROP TABLE IF EXISTS "{table_name}";')
        cursor.execute(create_table_sql)

        # Insert data using pandas to_sql
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"✓ Imported {len(df)} rows into '{table_name}'")

    except Exception as e:
        print(f"⚠️ Error importing {filepath}: {e}")

# Final
conn.commit()
conn.close()
print(f"\nAll done. Data imported into {DB_NAME}")
