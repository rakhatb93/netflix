import pandas as pd

df = pd.read_csv('netflix.csv')

sorted_csv_type = df.sort_values(['type', 'rating'])

sorted_data = sorted_csv_type.to_csv('sorted.csv')