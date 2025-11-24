import pandas as pd
import numpy as np

# Creating a dirty dataset
data = {
    'TransactionID': [101, 102, 103, 104, 101, 106, 107],  # Duplicate 101
    'Date': ['2025-11-01', '2025-11-01', '2025-11-02', 'Nov 3, 2025', '2025-11-04', '2025-11-05', '2025-11-06'], # Inconsistent format
    'Sales': [500, 200, np.nan, 400, 500, '600', 700], # Mixed types (String '600') and NaN
    'Region': ['North', 'South', 'North', 'East', 'North', 'West', 'West']
}

df = pd.DataFrame(data)
df.to_csv('broken_sales.csv', index=False)
print("File 'broken_sales.csv' created successfully.")