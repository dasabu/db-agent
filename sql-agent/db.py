import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

from langchain_community.utilities import SQLDatabase

DB_PATH = './db/salary.db'
TABLE_NAME = 'salaries'
CSV_FILE = 'salaries_2023.csv'

def get_engine(db_path=DB_PATH):
    return create_engine(f'sqlite:///{db_path}')

def setup_db(
    db_path=DB_PATH,
    table_name=TABLE_NAME,
    csv_file=CSV_FILE
):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Create engine to connect to the SQLite database
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Check if table exists and has records
    with engine.connect() as conn:
        try:
            # Count records in the table
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            record_count = result.fetchone()[0]
            table_exists = True
        except:
            # Table does not exist
            table_exists = False
            record_count = 0
    
    # If table does not exist or no records, populate the table with data from DataFrame
    try:
        if not table_exists or record_count == 0:
            st.warning('Table does not exist or no records, populating data...')
            # Read csv file
            df = pd.read_csv(csv_file).fillna(value=0)
            # Convert to sql
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            st.success(f'Populated table {table_name} with {len(df)} records from {csv_file}.')
        else:
            st.info(f'Table {table_name} already exists and contains {record_count} records. No data added.')
        # Return database
        db = SQLDatabase.from_uri(f'sqlite:///{db_path}')
        return db
    except Exception as e:
        st.error(f'Failed to populate table {table_name}: {str(e)}')
        raise e