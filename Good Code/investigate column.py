import pandas as pd

file_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\clean1_warwick.csv"
#herefordshire_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\certificates.csv"

df = pd.read_csv(file_path, usecols=['MAIN_FUEL'])

# View unique heating system types
unique_values = df['MAIN_FUEL'].unique()
print(len(unique_values))
print(unique_values[:50])  # show first 50