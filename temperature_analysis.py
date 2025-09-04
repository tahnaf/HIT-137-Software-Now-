import pandas as pd
import glob, os, re

# Map months to Australian seasons
SEASON_MAP = {
    "DECEMBER":"Summer","JANUARY":"Summer","FEBRUARY":"Summer",
    "MARCH":"Autumn","APRIL":"Autumn","MAY":"Autumn",
    "JUNE":"Winter","JULY":"Winter","AUGUST":"Winter",
    "SEPTEMBER":"Spring","OCTOBER":"Spring","NOVEMBER":"Spring"
}
SEASON_ORDER = ["Summer","Autumn","Winter","Spring"]

# 1) Load all CSVs in folder
folder = "temperature"   # <-- put your CSV files in a folder called "temperature"
files = sorted(glob.glob(os.path.join(folder,"*.csv")))
dfs = []
for f in files:
    year = int(re.search(r"(\d{4})", os.path.basename(f)).group(1))
    df = pd.read_csv(f)
    df["YEAR"] = year
    dfs.append(df)
data = pd.concat(dfs, ignore_index=True)
data.columns = [c.upper() for c in data.columns]

# 2) Melt months into long format
months = ["JANUARY","FEBRUARY","MARCH","APRIL","MAY","JUNE",
          "JULY","AUGUST","SEPTEMBER","OCTOBER","NOVEMBER","DECEMBER"]
long = data.melt(id_vars=["STATION_NAME","STN_ID","YEAR"], value_vars=months,
                 var_name="MONTH", value_name="TEMP")
long["TEMP"] = pd.to_numeric(long["TEMP"], errors="coerce")
long = long.dropna(subset=["TEMP"])
long["SEASON"] = long["MONTH"].map(SEASON_MAP)

# 3) Seasonal Average
seasonal = long.groupby("SEASON")["TEMP"].mean().reindex(SEASON_ORDER)
with open("average_temp.txt","w") as f:
    for s,v in seasonal.items():
        f.write(f"{s}: {v:.1f}°C\n")

# 4) Largest Temp Range
stats = long.groupby("STATION_NAME")["TEMP"].agg(["min","max"])
stats["range"] = stats["max"]-stats["min"]
max_r = stats["range"].max()
top = stats[stats["range"]==max_r]
with open("largest_temp_range_station.txt","w") as f:
    for name,row in top.iterrows():
        f.write(f"{name}: Range {row['range']:.1f}°C (Max: {row['max']:.1f}°C, Min: {row['min']:.1f}°C)\n")

# 5) Temperature Stability
stds = long.groupby("STATION_NAME")["TEMP"].std()
stable = stds[stds==stds.min()]
variable = stds[stds==stds.max()]
with open("temperature_stability_stations.txt","w") as f:
    for name,v in stable.items():
        f.write(f"Most Stable: {name}: StdDev {v:.1f}°C\n")
    for name,v in variable.items():
        f.write(f"Most Variable: {name}: StdDev {v:.1f}°C\n")

print("Done! Files created:")
print(" - average_temp.txt")
print(" - largest_temp_range_station.txt")
print(" - temperature_stability_stations.txt")
