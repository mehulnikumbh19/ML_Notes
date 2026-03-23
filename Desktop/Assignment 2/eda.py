import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

file_path = 'Gaming Ballot Data Set-1.xls'
try:
    df = pd.read_excel(file_path)
    print("--- HEAD ---")
    print(df.head(3))
    print("\n--- INFO ---")
    df.info()
    print("\n--- MISSING ---")
    print(df.isnull().sum())
    
    # Check for #NULL! string placeholders
    print("\n--- #NULL! CHECKS ---")
    for col in df.columns:
        null_count = (df[col] == '#NULL!').sum()
        if null_count > 0:
            print(f"{col}: {null_count} '#NULL!' strings found")
            
    print("\n--- DESCRIBE ---")
    print(df.describe(include='all'))
    
except Exception as e:
    print(f"Error loading Excel file: {e}")
