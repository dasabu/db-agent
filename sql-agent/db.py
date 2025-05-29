import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

from langchain_community.utilities import SQLDatabase

def setup_db(
    db_path='./db/salary.db',
    table_name='salaries',
    csv_file='salaries_2023.csv'
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