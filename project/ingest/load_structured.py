import os
import pandas as pd
import duckdb

def connect_to_duckdb(db_path='data/enterprise.duckdb'):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return duckdb.connect(db_path)

def load_csv(file_path, table_name):
    try:
        df = pd.read_csv(file_path)
        print(f"Loaded {len(df)} rows from {file_path}")
        
        conn = connect_to_duckdb()
        
        conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
        
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"Created table '{table_name}' with {row_count} rows")

        conn.close()
        return True
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return False

def normalize_tables():
    conn = connect_to_duckdb()
    
    conn.execute("""
    CREATE OR REPLACE TABLE staging_customers AS
    SELECT 
        customer_id,
        first_name,
        last_name,
        email,
        signup_date
    FROM customers
    """)

    conn.execute("""
    CREATE OR REPLACE TABLE staging_orders AS
    SELECT 
        order_id,
        customer_id,
        order_datetime,
        order_total as total_amount
    FROM orders
    """)
    
    conn.close()
    print("Created normalized tables: staging_customers, staging_orders")

if __name__ == "__main__":
    load_csv('data/customers.csv', 'customers')
    load_csv('data/orders.csv', 'orders')
    normalize_tables()