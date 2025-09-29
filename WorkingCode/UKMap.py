import pandas as pd
import zipfile
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

zip_path = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\all-domestic-certificates-single-file.zip"

with zipfile.ZipFile(zip_path, 'r') as z:
    with z.open('certificates.csv') as f:
        df1 = pd.read_csv(f, usecols=[0,4,5,8,9,10,11,12,13,14,]) #change usecols to select specific columns

#look at data
'''print(df.head())
print(list(df1.columns))
print('number of columns loaded:', len(df1.columns))
print('no of datapoints:',len(df1))
print(df1.dtypes)'''

#create new column
df1['EE_POTENTIAL_PERCENTAGE_INCREASE'] = (df1['POTENTIAL_ENERGY_EFFICIENCY'] - df1['CURRENT_ENERGY_EFFICIENCY']) / df1['CURRENT_ENERGY_EFFICIENCY'] * 100
#print(df['DELTA_ENERGY_EFFICIENCY'].describe())

#standardise the postcode column
df1['POSTCODE'] = df1['POSTCODE'].str.upper() #makes string and all uppercase
df1['POSTCODE'] = df1['POSTCODE'].str.strip() #removes any spaces at start or end
df1['POSTCODE'] = df1['POSTCODE'].str.replace(' ','') #removes all spaces
df1['POSTCODE'] = df1['POSTCODE'].str[:-3] + " " + df1['POSTCODE'].str[-3:] #adds space before last 3 characters
#now should align with ONSPD format
#print(df1['POSTCODE'].head(20))

#import postcode lat/long data
zip_path2 = "C:\\Users\\Archi\\OneDrive\\Documents\\VS_Personal\\JobApplications\\talan_epc\\postcode_latlong.csv"
df2 = pd.read_csv(zip_path2)

#merge the two dataframes on postcode to get lat/long into main df
df = pd.merge(df1, df2, left_on='POSTCODE', right_on='pcds', how='left')
print(df.head())

#background map
ccrs.PlateCarree()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
ax.coastlines(resolution='10m')
ax.add_feature(cartopy.feature.STATES, edgecolor='black', linewidth=0.3, alpha=0.3)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='black', linewidth=0.3, alpha=0.8)
ax.set_extent([-10, 2, 49, 60], crs=ccrs.PlateCarree()) #UK extent

#plot data points
sc = plt.scatter(df['long'], df['lat'], c=df['EE_POTENTIAL_PERCENTAGE_INCREASE'], cmap='viridis', s=10, alpha=0.7, transform=ccrs.PlateCarree())
plt.colorbar(sc, label='Potential Energy Efficiency Increase (%)')
plt.title('EPC Data Points in Warwick with Potential Energy Efficiency Increase')
plt.show()