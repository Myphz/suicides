import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from subprocess import run
import os
import sys

def fullscreen():
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

if len(sys.argv) != 2:
    print("USAGE: python "+ __file__ + " CountryName")
    exit()

# Read from csv files
suicides = pd.read_csv("./data/suicides.csv")
pop = pd.read_csv("./data/population.csv")
pop = pop.drop(columns=["LOCATION", "Sex", "Age", "VAR", "Variant", "TIME", "Unit", "PowerCode", "Reference Period Code", "Reference Period", "Flag Codes", "Flags"])
pop = pop[(pop["SEX"] == "TT") & (pop["AGE"] == "D199G5TT")]
pop = pop.groupby(["Country", "Time"])
suicides = suicides.drop(columns=["country-year", "HDI for year", "generation"])
suicides_yr = suicides.groupby("year")
suicides_yr_gender = suicides.groupby(["year", "sex"])
suicides_country = suicides.groupby(["country"])

# Select country
country = sys.argv[-1]
try:
    nation = suicides_country.get_group(country)
except:
    print("Country not found.")
    exit()

nation_yr = nation.groupby(["year"])
nation_yr_sex = nation.groupby(["year", "sex"])
yrs = nation["year"].unique()
nation_suicides_per_yrs = [nation_yr.get_group(yr)["suicides_no"].sum() for yr in yrs]
nation_male_suicides_per_yrs = [nation_yr_sex.get_group((yr, "male"))["suicides_no"].sum() for yr in yrs]
nation_female_suicides_per_yrs = [nation_yr_sex.get_group((yr, "female"))["suicides_no"].sum() for yr in yrs]
time = [x for x in range(len(yrs))]
style.use("ggplot")

# Suicides count by gender over the years in a certain country chart
plt.plot(time, nation_suicides_per_yrs, color="red", label="Total suicides")
plt.plot(time, nation_male_suicides_per_yrs, color="blue", label="Male suicides")
plt.plot(time, nation_female_suicides_per_yrs, color="purple", label="Female suicides")
plt.xticks([x for x in range(0, len(yrs), 5)], yrs[::5], fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel("Year", labelpad=25, fontsize=25)
plt.ylabel("Number of suicides", labelpad=50, fontsize=25)
plt.title(f"Suicides in {country} over the years", fontsize=30, pad=20)
plt.legend(loc="upper right", fontsize=11)
fullscreen()
plt.show()

# Call animation
run(["python", "./animation.py", country])

# Get total population, population over suicides count ratio, male suicides count over total suicides count ratio, female suicides over total suicides count ratio
try:
    total_pop = [pop.get_group((country, yr))["Value"] * 10 ** (pop.get_group((country, yr))["PowerCode Code"]) for yr in yrs]
except:
    print("Couldn't get population data")
    exit()

nation_total_suicide_ratio = [nation_yr.get_group(yr)["suicides_no"].sum() / tot * 100 for yr, tot in zip(yrs, total_pop)]
nation_male_suicide_ratio = [m / t * 100 for m, t in zip(nation_male_suicides_per_yrs, nation_suicides_per_yrs)]
nation_female_suicide_ratio = [m / t * 100 for m, t in zip(nation_female_suicides_per_yrs, nation_suicides_per_yrs)]

# Suicides percentage by gender in a certain country chart
plt.plot(time, nation_male_suicide_ratio, color="blue", label="Male suicides percentage")
plt.plot(time, nation_female_suicide_ratio, color="purple", label="Female suicides percentage")
plt.xticks([x for x in range(0, len(yrs), 5)], yrs[::5])
plt.xlabel("Year", labelpad=25, fontsize=25)
plt.ylabel("% of suicides", labelpad=50, fontsize=25)
plt.yticks([_ for _ in range(0, 101, 10)], [str(s) + "%" for s in range(0, 101, 10)], fontsize=15)
plt.title(f"Suicides by gender in {country} over the years", fontsize=30, pad=20)
plt.legend(loc="upper right", fontsize=15)
fullscreen()
plt.show()

# Total population over suicides count ratio over the years chart
plt.plot(time, nation_total_suicide_ratio)
plt.xticks([x for x in range(0, len(yrs), 5)], yrs[::5], fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel("Year", labelpad=25, fontsize=25)
plt.ylabel("% of suicides", labelpad=50, fontsize=25)
plt.title(f"Suicides over total population ratio in {country} over the years", fontsize=30, pad=20)
fullscreen()
plt.show()

# Get male, female and total amount of suicides per year in the world
yr = [yr for yr in range(1985, 2016)]
yr_enumerate = [x for x,_ in enumerate(yr)]
world_suicides_per_year = [suicides_yr.get_group(yr)["suicides_no"].sum() for yr in range(1985, 2016)]
world_male_suicides_per_year = [suicides_yr_gender.get_group((year, "male"))["suicides_no"].sum() for year in yr]
world_female_suicides_per_year = [suicides_yr_gender.get_group((year, "female"))["suicides_no"].sum() for year in yr]

# Suicides count by gender over the years in the world
plt.plot(yr_enumerate, world_suicides_per_year, color="red", label="Total suicides")
plt.plot(yr_enumerate, world_male_suicides_per_year, color="blue", label="Male suicides")
plt.plot(yr_enumerate, world_female_suicides_per_year, color="purple", label="Female suicides")
plt.xticks([_ for _ in range(0, len(yr), 5)], yr[::5], fontsize=15)
plt.yticks([_ for _ in range(50000, 250001, 50000)], [str(s // 1000) + "k" for s in range(50000, 250001, 50000)], fontsize=15)
plt.xlabel("Year", labelpad=25, fontsize=25)
plt.ylabel("Number of suicides", labelpad=50, fontsize=25)
plt.title("Suicides over the years", fontsize=30, pad=20)
plt.legend(loc="upper right", fontsize=11)
fullscreen()
plt.show()

# Get male suicides over total suicides ratio and female suicides over total suicides ratio
world_male_suicides_ratio = [m / t * 100 for m, t in zip(world_male_suicides_per_year, world_suicides_per_year)]
world_female_suicides_ratio = [f / t * 100 for f, t in zip(world_female_suicides_per_year, world_suicides_per_year)]

# Suicides percentage by gender in the world chart
plt.plot(yr_enumerate, world_male_suicides_ratio, color="blue", label="Male suicides percentage")
plt.plot(yr_enumerate, world_female_suicides_ratio, color="purple", label="Female suicides percentage")
plt.xticks([_ for _ in range(0, len(yr), 5)], yr[::5], fontsize=15)
plt.yticks([_ for _ in range(0, 101, 10)], [str(s) + "%" for s in range(0, 101, 10)], fontsize=15)
plt.xlabel("Year", labelpad=25, fontsize=25)
plt.ylabel("% of suicides", labelpad=50, fontsize=25)
plt.title(f"Suicides by gender", fontsize=30, pad=20)
plt.legend(loc="upper right", fontsize=11)
fullscreen()
plt.show()
