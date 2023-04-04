# Crop the file  air-quality-data-continuous.csv to delete any records before 00:00 1 Jan 2010

import pandas as pd

# Read the file
df = pd.read_csv('air-quality-data-continuous.csv', sep=';')

print(len(df))

# delete any records before 00:00 1 Jan 2010
df = df[df['Date Time'] >= '2010-01-01 00:00:00']

print(df.head())

# Count the number of records in the file
print(len(df))

# Save the file into crop.csv
df.to_csv('crop.csv', index=False, sep=';')
