# Netflix Insights

A mini analytics system to analyze Netflix titles dataset with MySQL, Python, Pandas, and Flask.

## Project structure

- `data/`: raw and cleaned datasets
- `src/`: scripts for cleaning, loading data, and analysis
- `sql/`: database schema and queries
- `app.py`: Flask interactive dashboard
- `.env`: environment variables for DB credentials
- `requirements.txt`: Python dependencies

## Setup

1. Download Netflix dataset from [Kaggle Netflix Titles](https://www.kaggle.com/shivamb/netflix-shows) and place the CSV in `data/netflix_titles.csv`.
2. Create a MySQL database and update `.env` with your credentials.
3. Install dependencies: `pip install -r requirements.txt`.
4. Run `src/data_cleaning.py` to clean dataset.
5. Execute the schema in `sql/create_table.sql` in your MySQL database.
6. Run `src/load_to_mysql.py` to load cleaned data into MySQL.
7. Run `app.py` to launch the dashboard: `python app.py`.

## Features

- Data cleaning of raw Netflix dataset
- Loading data into MySQL with schema
- SQL and Pandas queries for analysis
- Interactive visual dashboard with Plotly charts

Enjoy exploring Netflix trends!