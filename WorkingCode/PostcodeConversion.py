import pandas as pd
import zipfile

zip_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\ONSPD_MAY_2025.zip"

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('Data/ONSPD_MAY_2025_UK.csv') as f:
        df = pd.read_csv(f, usecols=['pcds','lat','long'])

#look at data
print(list(df.columns))
print(df.head())

#save to new csv to be used in other scripts
df.to_csv('C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\postcode_latlong.csv', index=False)
print('Finished!')