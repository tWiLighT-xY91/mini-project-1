import pandas as pd

def clean_netflix_data(input_path='netflix_insights/data/netflix_titles.csv', output_path='netflix_insights/data/cleaned_netflix_titles.csv'):
    # Load the dataset
    df = pd.read_csv(input_path)
    print(f"Original dataset shape: {df.shape}")
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Handle missing values
    df['director'].fillna('Unknown', inplace=True)
    df['cast'].fillna('Unknown', inplace=True)
    df['country'].fillna('Unknown', inplace=True)
    df['date_added'].fillna(df['date_added'].mode()[0], inplace=True)
    
    # Convert to datetime
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['date_added'].fillna(pd.Timestamp('2000-01-01'), inplace=True)
    
    # Normalize list-like columns
    df['listed_in'] = df['listed_in'].apply(lambda x: [i.strip() for i in x.split(',')] if pd.notnull(x) else [])
    df['country'] = df['country'].apply(lambda x: [i.strip() for i in x.split(',')] if pd.notnull(x) else ['Unknown'])
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Convert lists back to strings for storage
    df['listed_in'] = df['listed_in'].apply(lambda x: ', '.join(x))
    df['country'] = df['country'].apply(lambda x: ', '.join(x))
    
    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")
    print(f"Final dataset shape after cleaning: {df.shape}")

if __name__ == '__main__':
    clean_netflix_data()
