import streamlit as st
import pandas as pd
import sqlite3

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        st.error(f"Error: {e}")
    return conn

# Function to create a table
def create_table(conn):
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS user_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            city TEXT NOT NULL
        );
        """
        conn.execute(sql_create_table)
    except sqlite3.Error as e:
        st.error(f"Error: {e}")

# Function to insert data into the table
def insert_data(conn, name, age, city):
    try:
        sql_insert_data = """
        INSERT INTO user_data (name, age, city)
        VALUES (?, ?, ?);
        """
        cur = conn.cursor()
        cur.execute(sql_insert_data, (name, age, city))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error: {e}")

# Function to query all data from the table
def select_all_data(conn):
    try:
        sql_select_all = "SELECT * FROM user_data;"
        df = pd.read_sql_query(sql_select_all, conn)
        return df
    except sqlite3.Error as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# Streamlit app
st.title('Data Entry and Save to SQLite')

# Database connection
database = 'user_data.db'
conn = create_connection(database)
if conn:
    create_table(conn)

# User input
name = st.text_input('Enter your name')
age = st.number_input('Enter your age', min_value=0, max_value=100, step=1)
city = st.text_input('Enter your city')

# Insert data
if st.button('Save Data'):
    if name and age and city:
        insert_data(conn, name, age, city)
        st.success('Data saved to SQLite successfully!')
    else:
        st.error('Please fill out all fields')

# Display data
if st.button('Show Data'):
    df = select_all_data(conn)
    if not df.empty:
        st.write(df)
    else:
        st.error('No data found. Please save some data first.')

