import pandas as pd

file_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\clean1_warwick.csv"

#cols = pd.read_csv(file_path, nrows=0).columns.tolist()
#print(cols)

usecols = ['CURRENT_ENERGY_EFFICIENCY', 'POTENTIAL_ENERGY_EFFICIENCY', 'PROPERTY_TYPE', 'BUILT_FORM', 'INSPECTION_DATE',
            'LOCAL_AUTHORITY', 'CONSTITUENCY', 'COUNTY', 'ENVIRONMENT_IMPACT_CURRENT', 'ENVIRONMENT_IMPACT_POTENTIAL',
              'ENERGY_CONSUMPTION_CURRENT', 'ENERGY_CONSUMPTION_POTENTIAL', 'MAINS_GAS_FLAG', 'MAINHEAT_DESCRIPTION',
                'MAIN_FUEL', 'LOCAL_AUTHORITY_LABEL']

df = pd.read_csv(file_path, usecols=usecols)

#print(df.head())
print(len(df))

#remove all with lower than C energy efficiency
df = df[df['CURRENT_ENERGY_EFFICIENCY'] >= 69]
print(len(df))

#remove flats
df = df[df['PROPERTY_TYPE'] != 'Flat']
print(len(df))


#Want the number of properties using off grid fossil fuel supplys (to be replaced by heat pump)
fossil_fuels = [
    # LPG variants
    'LPG (not community)',
    'LPG (community)',
    'Gas: bulk LPG',
    'Gas: bottled LPG',
    'bottled LPG',
    'LPG special condition',
    'LPG - this is for backwards compatibility only and should not be used',

    # Oil variants
    'Oil: heating oil',
    'oil (not community)',
    'oil (community)',
    'oil - this is for backwards compatibility only and should not be used',

    # Solid fuels
    'house coal (not community)',
    'house coal - this is for backwards compatibility only and should not be used',
    'smokeless coal',
    'anthracite',

    # Mixed
    'dual fuel - mineral + wood'
] #this set was detemined by looking at unique values in the column

#filter only those using fossil fuels currently
df_fossil = df[df['MAIN_FUEL'].isin(fossil_fuels)]
print('fossil fuel use:', len(df_fossil))

mask_fossil = df['MAIN_FUEL'].isin(fossil_fuels)
unmatched_fuels = df.loc[~mask_fossil, 'MAIN_FUEL'].unique()
print([x for x in unmatched_fuels if any(k in str(x).lower() for k in ['oil','lpg','coal','anthracite','smokeless','dual'])])


#How many have underfloor heating
underfloor_df = df_fossil['MAINHEAT_DESCRIPTION'].str.contains('underfloor', case=False, na=False)
print(len(underfloor_df[underfloor_df]))

print('ideal candidates:', len(underfloor_df[underfloor_df]))
