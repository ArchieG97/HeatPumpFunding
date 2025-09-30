# import data
from pathlib import Path
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# paths
csv_file_path = Path(r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\GeoPlotData.csv")
geojson_path  = Path(r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\Local_Authority_Districts_December_2023_Boundaries_UK_BGC_322188543886714037.geojson")
out_png       = Path(r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\heatpump_candidates_map.png")
out_unmatched = Path(r"C:\Users\Archi\OneDrive\Documents\VS_Personal\JobApplications\talan_epc\unmatched_local_authorities.csv")

# load
df  = pd.read_csv(csv_file_path, low_memory=True)
gdf = gpd.read_file(geojson_path)
print("csv loaded:", df.shape)
print("geojson loaded:", gdf.shape)

# name cleaning
def norm(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
         .str.strip()
         .str.replace(r"\s+", " ", regex=True)
         .str.replace("&", "and", regex=False)
         .str.replace("-", " ", regex=False)
         .str.replace(",", "", regex=False)
         .str.lower()
    )

df["la_clean"]   = norm(df["LOCAL_AUTHORITY_LABEL"])
gdf["lad_clean"] = norm(gdf["LAD23NM"])

# manual fixes (extend as needed)
name_fix = {
    "bristol": "bristol city of",
    "city of westminster": "westminster",
    "herefordshire": "herefordshire county of",
    "kingston upon hull": "kingston upon hull city of",
    "anglesey": "isle of anglesey",
    "derry and strabane": "derry city and strabane",
}
df["la_clean"] = df["la_clean"].replace(name_fix)

# sanity check
if "Qualifying_Count" not in df.columns:
    raise ValueError("Expected column 'Qualifying_Count' not found in CSV.")

agg = df.groupby("la_clean", as_index=False)["Qualifying_Count"].sum()

# check for unmatched LAs
missing_in_map = sorted(set(agg["la_clean"]) - set(gdf["lad_clean"]))
if missing_in_map:
    pd.Series(missing_in_map, name="la_clean").to_csv(out_unmatched, index=False)
    print(f"unmatched LAs written → {out_unmatched}")
else:
    print("all local authorities matched successfully.")

# merge datasets
gdf = gdf.merge(agg, left_on="lad_clean", right_on="la_clean", how="left")
gdf["Qualifying_Count"] = gdf["Qualifying_Count"].fillna(0).astype(int)

# projection
proj = ccrs.PlateCarree()
gdf = gdf.to_crs(epsg=4326)

# custom colormap (linear data scaling, steeper ramp to dark red)
cmap = mcolors.LinearSegmentedColormap.from_list(
    "white_red_steep",
    [
        (0.00, "#ffffff"),  # pure white
        (0.25, "#fcbba1"),  # very light red
        (0.50, "#fc9272"),  # medium red
        (0.75, "#de2d26"),  # strong red
        (1.00, "#67000d"),  # dark red
    ],
)


# vmin/vmax for color scaling
vmin, vmax = 0, gdf["Qualifying_Count"].max()

# plot
fig, ax = plt.subplots(figsize=(11, 13), subplot_kw={"projection": proj})
ax.set_title(
    'Number of "Ideal Candidates" per Local Authority in England',
    fontsize=16
)
ax.set_extent([-8.5, 2.5, 49.5, 59.5], crs=ccrs.PlateCarree())

# base features
ax.add_feature(cfeature.LAND, alpha=0.05)
ax.add_feature(cfeature.COASTLINE, linewidth=0.4)
ax.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.5)

# extract England only
england = gdf[gdf["LAD23CD"].str.startswith("E")].copy()

# dissolve to single outline
england_outline = england.dissolve()

# outline
england_outline.boundary.plot(
    ax=ax,
    transform=ccrs.PlateCarree(),
    color='black',
    linewidth=0.8,
    zorder=5
)

# main plot
gdf.plot(
    ax=ax,
    column="Qualifying_Count",
    transform=ccrs.PlateCarree(),
    cmap=cmap,
    vmin=vmin,
    vmax=vmax,
    linewidth=0.25,
    edgecolor="black",
    legend=True,
    legend_kwds={
        "label": "Candidate Count",
        "orientation": "vertical",
        "shrink": 0.6,
        "pad": 0.02,
        "location": "left"
    },
    missing_kwds={"color": "#dddddd", "hatch": "///", "label": "No data"},
)


# legend font sizes
leg = ax.get_legend()
if leg:
    plt.setp(leg.get_title(), fontsize=10)
    plt.setp(leg.get_texts(), fontsize=9)
    if hasattr(leg, 'ax'):
        cbar = leg.ax
        cbar.yaxis.set_label_position('left')
        cbar.yaxis.tick_right()

#label top counties

# label top N local authorities by Qualifying_Count
N = 5
topN = gdf.nlargest(N, "Qualifying_Count")

for _, row in topN.iterrows():
    # centroid coordinates in PlateCarree
    x, y = row.geometry.centroid.x, row.geometry.centroid.y

    # plot black dot at centroid
    ax.plot(
        x, y,
        marker='o',
        markersize=3,
        color='black',
        transform=ccrs.PlateCarree(),
        zorder=14
    )

    # add text label slightly above dot
    ax.text(
        x,
        y + 0.2,  # vertical offset
        row["LAD23NM"],
        transform=ccrs.PlateCarree(),
        fontsize=8,
        fontweight="bold",
        color="black",
        ha="center",
        va="bottom",
        zorder=15,
        bbox=dict(
            facecolor="white",
            alpha=0.7,
            edgecolor="none",
            boxstyle="round,pad=0.2"
        )
    )

print("\nTop 5 labelled on map:")
print(topN[["LAD23NM", "Qualifying_Count"]])
print('number of local authorities with under ten candidates:', (gdf["Qualifying_Count"] < 10).sum())
print('average number of candidates per local authority:', gdf["Qualifying_Count"].mean())
print('the total number of candidates across all local authorities:', gdf["Qualifying_Count"].sum())
print('the number of candidates in the top 10 local authorities:', topN["Qualifying_Count"].sum())
print('the percentage of candidates in the top 10 local authorities:', (topN["Qualifying_Count"].sum() / gdf["Qualifying_Count"].sum()) * 100)
# layout and save
plt.tight_layout(pad=2.0)
plt.savefig(out_png, dpi=300)
print(f"saved map → {out_png}")
plt.show()
