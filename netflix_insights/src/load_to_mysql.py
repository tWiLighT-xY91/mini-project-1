import pandas as pd
import mysql.connector# type: ignore
from mysql.connector import Error# type: ignore
import os
from dotenv import load_dotenv# type: ignore

load_dotenv()

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        print("MySQL connection established")
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return connection

def insert_data(connection, df):
    cursor = connection.cursor()
    # Prepare insert query
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
        # Insert rows one by one or could batch for optimization
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
        connection.commit()
        print(f"{cursor.rowcount} records inserted/updated.")
    except Error as e:
        print(f"Error inserting data: {e}")
    cursor.close()

if __name__ == '__main__':
    cleaned_data_path = 'data/cleaned_netflix_titles.csv'
    df_cleaned = pd.read_csv(cleaned_data_path, parse_dates=['date_added'])
    conn = create_connection()
    if conn:
        insert_data(conn, df_cleaned)
        conn.close()
