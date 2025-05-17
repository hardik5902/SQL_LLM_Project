import duckdb
import os


def connect_to_duckdb(db_path='data/enterprise.duckdb'):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return duckdb.connect(db_path)

conn = connect_to_duckdb()

row_count = conn.execute(f"SELECT * FROM customers LIMIT 5").fetchall()
print(row_count)