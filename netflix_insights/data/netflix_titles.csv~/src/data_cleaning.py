import pandas as pd

def clean_netflix_data(input_path='data/netflix_titles.csv~', output_path='data/cleaned_netflix_titles.csv'):
    # Load the dataset
    df = pd.read_csv(input_path)
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Handle missing values - fill director and cast with 'Unknown'
    df['director'].fillna('Unknown', inplace=True)
    df['cast'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['date_added'].fillna(df['date_added'].mode()[0], inplace=True)  # fill with most common date_added
    
    # Convert date_added to datetime, errors='coerce' to handle invalid formats
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    
    # For any remaining NaT, fill with a default date (or drop)
    df['date_added'].fillna(pd.Timestamp('2000-01-01'), inplace=True)
    
    # Split listed_in and country columns from string to list for further use if needed
    df['listed_in'] = df['listed_in'].apply(lambda x: [i.strip() for i in x.split(',')] if pd.notnull(x) else [])
    df['country'] = df['country'].apply(lambda x: [i.strip() for i in x.split(',')] if pd.notnull(x) else ['Unknown'])
    
    # Standardize columns format: strip and lower case column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Convert list columns back to comma-separated strings for database storage
    df['listed_in'] = df['listed_in'].apply(lambda x: ', '.join(x))
    df['country'] = df['country'].apply(lambda x: ', '.join(x))
    
    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f'Cleaned data saved to {output_path}')
    
if __name__ == '__main__':
    clean_netflix_data()

