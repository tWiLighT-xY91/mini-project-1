import pandas as pd
import mysql.connector  # type: ignore
from mysql.connector import Error  # type: ignore
import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

def create_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_ADDON_HOST'),
            user=os.getenv('MYSQL_ADDON_USER'),
            password=os.getenv('MYSQL_ADDON_PASSWORD'),
            database=os.getenv('MYSQL_ADDON_DB'),
            port=int(os.getenv('MYSQL_ADDON_PORT', 3306))
        )
        print("✅ MySQL connection established")
        return conn
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

def create_table(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS netflix_titles (
        show_id VARCHAR(15) PRIMARY KEY,
        type VARCHAR(20),
        title VARCHAR(255),
        director VARCHAR(255),
        cast VARCHAR(1000),
        country VARCHAR(255),
        date_added DATE,
        release_year INT,
        rating VARCHAR(10),
        duration VARCHAR(20),
        listed_in VARCHAR(500),
        description VARCHAR(1000)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("✅ Table checked/created")
        cursor.close()
    except Error as e:
        print(f"❌ Error creating table: {e}")

def insert_data(conn, df):
    insert_query = """
    INSERT INTO netflix_titles 
    (show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        type=VALUES(type),
        title=VALUES(title),
        director=VALUES(director),
        cast=VALUES(cast),
        country=VALUES(country),
        date_added=VALUES(date_added),
        release_year=VALUES(release_year),
        rating=VALUES(rating),
        duration=VALUES(duration),
        listed_in=VALUES(listed_in),
        description=VALUES(description);
    """
    try:
        cursor = conn.cursor()
        for _, row in df.iterrows():
            data_tuple = (
                row['show_id'],
                row['type'],
                row['title'],
                row['director'],
                row['cast'],
                row['country'],
                row['date_added'].date() if pd.notnull(row['date_added']) else None,
                int(row['release_year']) if not pd.isnull(row['release_year']) else None,
                row['rating'],
                row['duration'],
                row['listed_in'],
                row['description']
            )
            cursor.execute(insert_query, data_tuple)
        conn.commit()
        print(f"✅ {cursor.rowcount} records inserted/updated.")
        cursor.close()
    except Error as e:
        print(f"❌ Error inserting data: {e}")

if __name__ == '__main__':
    cleaned_data_path = 'netflix_insights/data/cleaned_netflix_titles.csv'
    df_cleaned = pd.read_csv(cleaned_data_path, parse_dates=['date_added'])
    conn = create_connection()
    if conn:
        create_table(conn)        # <- ensure table exists
        insert_data(conn, df_cleaned)
        conn.close()
