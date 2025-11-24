import pandas as pd
import os

def clean_client_data(file_path):
    # Check if file exists first
    if not os.path.exists(file_path):
        return "Error: File not found."

    try:
        # LOAD data
        data = pd.read_csv(file_path)

        # CLEAN data (Put your logic here)
        # 1. Fix Dates
        data['Date'] = pd.to_datetime(data['Date'], format='mixed', errors='coerce')
        # 2. Fix Sales (Force numeric first!)
        data['Sales'] = pd.to_numeric(data['Sales'], errors='coerce')
        # 3. Drop Duplicates
        data = data.drop_duplicates(subset='TransactionID', keep='first')
        return data
    
    except Exception as e:
        return f"Critical Error: {e}"

# Test it
cleaned_df = clean_client_data('broken_sales.csv')
print(cleaned_df)