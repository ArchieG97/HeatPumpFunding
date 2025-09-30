import pandas as pd
import zipfile

zip_path = r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\all-domestic-certificates-single-file.zip"
out_path = r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\clean1_UK.csv"

usecols = [
    'LMK_KEY', 'CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY',
    'PROPERTY_TYPE', 'BUILT_FORM', 'INSPECTION_DATE', 'LOCAL_AUTHORITY',
    'CONSTITUENCY', 'COUNTY',
    'ENVIRONMENT_IMPACT_CURRENT', 'ENVIRONMENT_IMPACT_POTENTIAL',
    'ENERGY_CONSUMPTION_CURRENT', 'ENERGY_CONSUMPTION_POTENTIAL',
    'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL',
    'LOCAL_AUTHORITY_LABEL'
]

wales_las = [
    "Isle Of Anglesey", "Blaenau Gwent", "Bridgend", "Caerphilly", "Cardiff",
    "Carmarthenshire", "Ceredigion", "Conwy", "Denbighshire", "Flintshire",
    "Gwynedd", "Merthyr Tydfil", "Monmouthshire", "Neath Port Talbot",
    "Newport", "Pembrokeshire", "Powys", "Rhondda Cynon Taf", "Swansea",
    "Torfaen", "Vale Of Glamorgan", "Wrexham"
]

numeric_cols = [
    'LMK_KEY', 'CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY',
    'ENVIRONMENT_IMPACT_CURRENT', 'ENVIRONMENT_IMPACT_POTENTIAL',
    'ENERGY_CONSUMPTION_CURRENT', 'ENERGY_CONSUMPTION_POTENTIAL'
]

string_cols = [
    'PROPERTY_TYPE', 'BUILT_FORM', 'LOCAL_AUTHORITY', 'CONSTITUENCY',
    'COUNTY', 'MAINHEAT_DESCRIPTION', 'MAIN_FUEL'
]

first = True
total_in = 0
total_after_wales = 0

# --- open zip manually ---
with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('certificates.csv') as f:
        reader = pd.read_csv(f, usecols=usecols, chunksize=200_000, low_memory=True)

        for chunk in reader:
            total_in += len(chunk)

            # Clean LA label
            chunk['LOCAL_AUTHORITY_LABEL'] = (
                chunk['LOCAL_AUTHORITY_LABEL']
                .str.strip()
                .str.replace(r'\s+', ' ', regex=True)
                .str.title()
            )

            # Remove Wales
            chunk = chunk[~chunk['LOCAL_AUTHORITY_LABEL'].isin(wales_las)]
            total_after_wales += len(chunk)

            # Datetime
            chunk['INSPECTION_DATE'] = pd.to_datetime(chunk['INSPECTION_DATE'], errors='coerce')

            # Numeric
            for col in numeric_cols:
                if col in chunk.columns:
                    chunk[col] = pd.to_numeric(chunk[col], errors='coerce')

            # Strings
            for col in string_cols:
                if col in chunk.columns:
                    chunk[col] = chunk[col].str.strip().str.replace(r'\s+', ' ', regex=True).str.title()
            
            #GAS FLAG
            if "MAINS_GAS_FLAG" in chunk.columns:
                chunk["MAINS_GAS_FLAG"] = (
                    chunk["MAINS_GAS_FLAG"]
                    .replace({"Y": 1, "N": 0, "": pd.NA, " ": pd.NA})
                    .astype("Int8") )  # nullable int (saves memory, keeps <NA>)
            



            # Optional acronym fix
            # chunk['MAIN_FUEL'] = chunk['MAIN_FUEL'].str.replace(r'\bLpg\b', 'LPG', regex=True)

            # Write chunk
            chunk.to_csv(out_path, mode='w' if first else 'a', header=first, index=False)
            first = False

print(f"Initial rows (all countries): {total_in}")
print(f"Rows after removing Wales:   {total_after_wales}")
print("Saved:", out_path)
