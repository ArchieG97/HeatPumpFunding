#imports
import pandas as pd
import matplotlib.pyplot as plt
from itertools import cycle

#--- load
csv_file_path = r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\clean1_UK.csv"
usecols = [
    'CURRENT_ENERGY_EFFICIENCY','PROPERTY_TYPE','INSPECTION_DATE','LOCAL_AUTHORITY',
    'CONSTITUENCY','ENVIRONMENT_IMPACT_CURRENT','ENERGY_CONSUMPTION_CURRENT',
    'MAINS_GAS_FLAG','MAINHEAT_DESCRIPTION','MAIN_FUEL','LOCAL_AUTHORITY_LABEL'
]
df = pd.read_csv(csv_file_path, usecols=usecols, low_memory=True)

#--- filter (off-gas, EPC ≥69, not flats)
filtered = df[
    (df['MAINS_GAS_FLAG'] == 'N') &
    (df['CURRENT_ENERGY_EFFICIENCY'] >= 69) &
    (~df['PROPERTY_TYPE'].str.contains('Flat', case=False, na=False))
]

#--- aggregate
summary = (
    filtered
    .groupby('LOCAL_AUTHORITY_LABEL')
    .size()
    .reset_index(name='Qualifying_Count')
    .sort_values('Qualifying_Count', ascending=False)
)

print(summary)

#--- top N
N = 10
top_summary = summary.head(N).copy()  # copy to avoid chained assignment

#--- region mapping (expand as needed)
region_map = {
    # South West
    'Cornwall': 'South West',
    'Wiltshire': 'South West',
    'Dorset': 'South West',
    'South Somerset': 'South West',
    # West Midlands
    'Shropshire': 'West Midlands',
    # East of England
    "King's Lynn and West Norfolk": 'East of England',
    'Mid Suffolk': 'East of England',
    'West Suffolk': 'East of England',
    'South Norfolk': 'East of England',
    # North East
    'Northumberland': 'North East',
}
top_summary['Region'] = top_summary['LOCAL_AUTHORITY_LABEL'].map(region_map).fillna('Other')

#--- colours per region + fallback
region_colors = {
    'South West':    '#1f77b4',
    'West Midlands': '#ff7f0e',
    'East of England':'#2ca02c',
    'North East':    '#9467bd',
    'Other':         '#8c564b'
}
colors = top_summary['Region'].map(region_colors)

#--- plot
plt.figure(figsize=(10, 6))
plt.barh(top_summary['LOCAL_AUTHORITY_LABEL'],
         top_summary['Qualifying_Count'],
         color=colors)

plt.xlabel('Number of "Ideal Candidates"')
plt.ylabel('Local Authority')
plt.title(f'Top {N} Local Authorities (coloured by region)')
plt.gca().invert_yaxis()
plt.tight_layout()

# legend
handles = [plt.Rectangle((0,0),1,1, color=c) for c in region_colors.values()]
labels  = list(region_colors.keys())
plt.legend(handles, labels, title='Region', loc='lower right')

plt.savefig(r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\ideal_candidates_barchart.png", dpi=300, bbox_inches='tight')
plt.show()
