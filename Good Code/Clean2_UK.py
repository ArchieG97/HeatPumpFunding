import pandas as pd

csv_file_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\clean1_UK.csv"

available_cols = [
    'LMK_KEY', 'CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY',
    'PROPERTY_TYPE', 'BUILT_FORM', 'INSPECTION_DATE', 'LOCAL_AUTHORITY',
    'CONSTITUENCY', 'COUNTY',
    'ENVIRONMENT_IMPACT_CURRENT', 'ENVIRONMENT_IMPACT_POTENTIAL',
    'ENERGY_CONSUMPTION_CURRENT', 'ENERGY_CONSUMPTION_POTENTIAL',
    'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL',
    'LOCAL_AUTHORITY_LABEL'
]
usecols = [
    'CURRENT_ENERGY_EFFICIENCY',
    'PROPERTY_TYPE',  'INSPECTION_DATE', 'LOCAL_AUTHORITY',
    'CONSTITUENCY',
    'ENVIRONMENT_IMPACT_CURRENT',
    'ENERGY_CONSUMPTION_CURRENT',
    'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL',
    'LOCAL_AUTHORITY_LABEL'
]

df = pd.read_csv(csv_file_path, usecols=usecols, low_memory=True)


import pandas as pd

# filter first
filtered = df[
    (df['MAINS_GAS_FLAG'] == 'N') &
    (df['CURRENT_ENERGY_EFFICIENCY'] >= 69) &
    (~df['PROPERTY_TYPE'].str.contains('Flat', case=False, na=False))
]

# group and count by local authority
summary = (
    filtered
    .groupby('LOCAL_AUTHORITY_LABEL')
    .size()
    .reset_index(name='Qualifying_Count')
    .sort_values('Qualifying_Count', ascending=False)
)

out_path = r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\GeoPlotData.csv"
summary.to_csv(out_path, index=False)
print(f"Summary saved to {out_path}")