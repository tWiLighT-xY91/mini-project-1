import pandas as pd
import os
from sqlalchemy import create_engine #type: ignore
from dotenv import load_dotenv#type: ignore

load_dotenv()

def create_engine_connection():
    user = os.getenv("MYSQL_ADDON_USER")
    password = os.getenv("MYSQL_ADDON_PASSWORD")
    host = os.getenv("MYSQL_ADDON_HOST")
    port = os.getenv("MYSQL_ADDON_PORT", "3306")
    database = os.getenv("MYSQL_ADDON_DB")
    connection_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_str)
    return engine

def get_top_genres(engine, limit=10):
    query = f"""
        SELECT listed_in, COUNT(*) as count
        FROM netflix_titles
        GROUP BY listed_in
        ORDER BY count DESC
        LIMIT {limit};
    """
    return pd.read_sql(query, engine)

def get_shows_per_country(engine, limit=10):
    query = f"""
        SELECT country, COUNT(*) as count
        FROM netflix_titles
        GROUP BY country
        ORDER BY count DESC
        LIMIT {limit};
    """
    return pd.read_sql(query, engine)

def get_top_directors(engine, limit=10):
    query = f"""
        SELECT director, COUNT(*) as count
        FROM netflix_titles
        GROUP BY director
        ORDER BY count DESC
        LIMIT {limit};
    """
    return pd.read_sql(query, engine)

def get_yearly_trend(engine):
    query = """
        SELECT release_year, COUNT(*) as count
        FROM netflix_titles
        WHERE release_year IS NOT NULL
        GROUP BY release_year
        ORDER BY release_year;
    """
    return pd.read_sql(query, engine)

def get_type_distribution(engine):
    query = """
        SELECT type, COUNT(*) as count
        FROM netflix_titles
        GROUP BY type;
    """
    return pd.read_sql(query, engine)

if __name__ == "__main__":
    engine = create_engine_connection()

    print("Top Genres:")
    print(get_top_genres(engine))

    print("\nShows Per Country:")
    print(get_shows_per_country(engine))

    print("\nTop Directors:")
    print(get_top_directors(engine))

    print("\nYearly Content Trend:")
    print(get_yearly_trend(engine))

    print("\nContent Type Distribution:")
    print(get_type_distribution(engine))
