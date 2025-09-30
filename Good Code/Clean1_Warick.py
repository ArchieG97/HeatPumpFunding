import pandas as pd
import zipfile

zip_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\domestic-E07000222-Warwick.zip"

usecols = ['LMK_KEY', 'CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY', 'PROPERTY_TYPE', 'BUILT_FORM', 'INSPECTION_DATE', 'LOCAL_AUTHORITY',
        'CONSTITUENCY', 'COUNTY', 'ENVIRONMENT_IMPACT_CURRENT', 'ENVIRONMENT_IMPACT_POTENTIAL', 'ENERGY_CONSUMPTION_CURRENT',
        'ENERGY_CONSUMPTION_POTENTIAL', 'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL', 'LOCAL_AUTHORITY_LABEL']

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('certificates.csv') as f:
        df = pd.read_csv(f, usecols=usecols)

#clean  LOCAL_AUTHORITY_LABEL
df['LOCAL_AUTHORITY_LABEL'] = df['LOCAL_AUTHORITY_LABEL'].str.strip().str.replace(r'\s+', ' ', regex=True).str.title()


#count rows
print(f"Initial number of rows: {len(df)}")

#Reduce dataset by removing Welsh records based on LOCAL_AUTHORITY_LABEL (note LOCAL_AUTHORITY_LABEL cannot be relied apon as per columns.csv but it is good enough for this purpose)
wales_las = [
    "Anglesey", "Blaenau Gwent", "Bridgend", "Caerphilly", "Cardiff",
    "Carmarthenshire", "Ceredigion", "Conwy", "Denbighshire", "Flintshire",
    "Gwynedd", "Merthyr Tydfil", "Monmouthshire", "Neath Port Talbot",
    "Newport", "Pembrokeshire", "Powys", "Rhondda Cynon Taf", "Swansea",
    "Torfaen", "Vale Of Glamorgan", "Wrexham"
]
# Remove Welsh records
df = df[~df["LOCAL_AUTHORITY_LABEL"].isin(wales_las)]

#count rows
print(f"Number of rows after removing Welsh records: {len(df)}")

#Clean the rest of the columns

#Datetime first
df['INSPECTION_DATE'] = pd.to_datetime(df['INSPECTION_DATE'], errors='coerce')

#Decide which of usecols are numeric and convert them
numeric_cols = ['LMK_KEY','CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY','ENVIRONMENT_IMPACT_CURRENT',
                 'ENVIRONMENT_IMPACT_POTENTIAL','ENERGY_CONSUMPTION_CURRENT', 'ENERGY_CONSUMPTION_POTENTIAL'
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

#Remaining columns as strings
string_cols = [
    'PROPERTY_TYPE', 'BUILT_FORM', 'LOCAL_AUTHORITY', 'CONSTITUENCY',
    'COUNTY', 'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL'
] # Exclude 'LOCAL_AUTHORITY_LABEL' as it's already cleaned
for col in string_cols:
    df[col] = df[col].str.strip().str.replace(r'\s+', ' ', regex=True).str.title()


#save to csv
out_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\clean1_warwick.csv"
df.to_csv(out_path, index=False)
print("Saved:", out_path)