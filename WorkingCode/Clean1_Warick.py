import pandas as pd
import zipfile

zip_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\domestic-E07000222-Warwick.zip"

usecols = ['CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY', 'PROPERTY_TYPE', 'BUILT_FORM', 'INSPECTION_DATE', 'LOCAL_AUTHORITY',
        'CONSTITUENCY', 'COUNTY', 'ENVIRONMENT_IMPACT_CURRENT', 'ENVIRONMENT_IMPACT_POTENTIAL', 'ENERGY_CONSUMPTION_CURRENT',
        'ENERGY_CONSUMPTION_POTENTIAL', 'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL', 'LOCAL_AUTHORITY_LABEL']

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('certificates.csv') as f:
        df = pd.read_csv(f, usecols=usecols)


#Reduce dataset by removing Welsh records based on LOCAL_AUTHORITY_LABEL
wales_las = [
    "Anglesey", "Blaenau Gwent", "Bridgend", "Caerphilly", "Cardiff",
    "Carmarthenshire", "Ceredigion", "Conwy", "Denbighshire", "Flintshire",
    "Gwynedd", "Merthyr Tydfil", "Monmouthshire", "Neath Port Talbot",
    "Newport", "Pembrokeshire", "Powys", "Rhondda Cynon Taf", "Swansea",
    "Torfaen", "Vale of Glamorgan", "Wrexham"
]

# Remove Welsh records
df = df[~df["LOCAL_AUTHORITY_LABEL"].isin(wales_las)] #LOCAL_AUTHORITY_LABEL is said not to be reliable,however is fine for our purpose


out_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\clean1_warwick.csv"
df.to_csv(out_path, index=False)
print("Saved:", out_path)