import pandas as pd

#load data
certificate_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\domestic-E07000222-Warwick\\certificates.csv"
df = pd.read_csv(certificate_path)

#look at data
#print(df.head())
#print(list(df.columns), len(df.columns))
#print(len(df))
#print(df.dtypes)

#check unique values in each column
for col in df.columns:
    if df[col].dtype == 'object':
        num_unique_values = len(df[col].unique())
        print(f"{col}: {num_unique_values} unique values")
        #print(df[col].unique())
    else:
        print(f"{col}: {df[col].dtype}")

#make every row in needed column have set data type
#integers first
for col in ['CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    num_non_numeric = df[col].isna().sum()
    print(f"{col}: {num_non_numeric} non-numeric values")

df['DELTA_ENERGY_EFFICIENCY'] = df['POTENTIAL_ENERGY_EFFICIENCY'] - df['CURRENT_ENERGY_EFFICIENCY']
print(df['DELTA_ENERGY_EFFICIENCY'].describe())
