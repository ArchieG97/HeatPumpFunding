import pandas as pd
import zipfile

file_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\clean1_warwick.csv"

usecols = ['CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY', 'PROPERTY_TYPE', 'BUILT_FORM', 'INSPECTION_DATE', 'LOCAL_AUTHORITY',
        'CONSITUENCY', 'COUNTY', 'ENVIRONMENTAL_IMPACT_CURRENT', 'ENVIRONMENTAL_IMPACT_POTENTIAL', 'ENERGY_CONSUMPTION_CURRENT',
        'ENERGY_CONSUMPTION_POTENTIAL', 'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL']

df = pd.read_csv(file_path, usecols=usecols)

print(df.head())
