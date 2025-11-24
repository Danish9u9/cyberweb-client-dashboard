import pandas as pd

data = pd.read_csv('broken_sales.csv')
data.isnull().sum()
data.info()
data.duplicated().sum()
print(data)