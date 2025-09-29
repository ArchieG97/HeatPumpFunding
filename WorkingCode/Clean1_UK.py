import pandas as pd
import zipfile

zip_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\all-domestic-certificates-single-file.zip"

usecols = ['CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY', 'PROPERTY_TYPE', 'BUILT_FORM', 'INSPECTION_DATE', 'LOCAL_AUTHORITY',
        'CONSITUENCY', 'COUNTY', 'ENVIRONMENTAL_IMPACT_CURRENT', 'ENVIRONMENTAL_IMPACT_POTENTIAL', 'ENERGY_CONSUMPTION_CURRENT',
        'ENERGY_CONSUMPTION_POTENTIAL', 'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL']

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
df = df[~df["LOCAL_AUTHORITY_LABEL"].isin(wales_las)]

pd.to_csv(df, "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\clean1_UK.csv", index=False)