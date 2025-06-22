import sqlite3
import pandas as pd


def get_connection():
    try:
        return sqlite3.connect("WS_results.db")
    except sqlite3.Error as e:
        print(f"Error connecting to DB: {e}")
        return None


def show_menu():
    print("\nChoose a query:")
    print("1. Show all World Series results")
    print("2. Filter results by year")
    print("3. Display the years the Mets won")
    print("4. Display the years the Phillies participated")
    print("5. Exit")


def run_query(conn, sql):
    try:
        df = pd.read_sql_query(sql, conn)
        if df.empty:
            print("⚠️ No results found.")
        else:
            print(df.to_string(index=False))
    except Exception as e:
        print(f"Error: {e}")


def run_command(conn, sql):
    try:
        conn.execute(sql)
        conn.commit()
        print(" Command executed successfully.")
    except Exception as e:
        print(f"Error: {e}")


def all_WS_results(conn):
    run_query(conn, "SELECT * FROM WS_results LIMIT 20")


def WS_results_by_year(conn):
    try:
        year = input("Enter year: ").strip()
        sql = f"""
            SELECT Year, Team1, Score1, Team2, Score2
            FROM WS_results
            WHERE Year LIKE '%{year}%'
        """
        run_query(conn, sql)
    except Exception as e:
        print(f"Error: {e}")


def mets_win(conn):
    try:
        sql = """
            SELECT Year
            FROM WS_results
            WHERE (Team1 LIKE '%Mets%' AND CAST(Score1 AS INTEGER) > CAST(Score2 AS INTEGER))
               OR (Team2 LIKE '%Mets%' AND CAST(Score2 AS INTEGER) > CAST(Score1 AS INTEGER))
            ORDER BY Year;
        """
        run_query(conn, sql)
    except Exception as e:
        print(f"Error: {e}")


def Phils_part(conn):
    try:
        sql = """
            SELECT Year
            FROM WS_results
            WHERE Team1 LIKE '%Phillies%' OR Team2 LIKE '%Phillies%'
            ORDER BY Year;
        """
        run_query(conn, sql)
    except Exception as e:
        print(f"Error: {e}")


def main():
    conn = get_connection()
    if not conn:
        return

    try:
        while True:
            show_menu()
            choice = input("Choice: ").strip()
            if choice == "1":
                all_WS_results(conn)
            elif choice == "2":
                WS_results_by_year(conn)
            elif choice == "3":
                mets_win(conn)
            elif choice == "4":
                Phils_part(conn)
            elif choice == "5":
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid option.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
