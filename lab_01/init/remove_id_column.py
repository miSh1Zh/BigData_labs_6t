import pandas as pd
import glob
import os

# Get all MOCK_DATA CSV files
csv_files = glob.glob('MOCK_DATA*.csv')

for file in csv_files:
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Drop the first column (id)
    df = df.drop(df.columns[0], axis=1)
    
    # Create new filename with '_no_id' suffix
    new_filename = os.path.splitext(file)[0] + '_no_id.csv'
    
    # Save the modified dataframe to a new CSV file
    df.to_csv(new_filename, index=False)
    
    print(f'Processed {file} -> {new_filename}') 