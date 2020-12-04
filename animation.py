import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.animation import FuncAnimation
import os
import sys

if len(sys.argv) != 2:
    print("Bad usage.")
    exit()

def anim(i):
    if i <= len(time):
        line.set_xdata(time[:i])
        line.set_ydata(nation_suicides_per_yrs[:i])
        return line,

# Read from csv files
suicides = pd.read_csv(os.path.dirname(__file__) + "/data/suicides.csv")
suicides = suicides.drop(columns=["country-year", "HDI for year", "generation"])
suicides_yr = suicides.groupby("year")
suicides_country = suicides.groupby(["country"])

# Select country
country = sys.argv[1]

nation = suicides_country.get_group(country)
nation_yr = nation.groupby(["year"])
yrs = nation["year"].unique()
nation_suicides_per_yrs = [nation_yr.get_group(yr)["suicides_no"].sum() for yr in yrs]
time = [x for x in range(len(yrs))]
style.use("ggplot")

# Animation
fig, ax = plt.subplots()
ax.set_xlim(0, len(time))
ax.set_ylim(min(nation_suicides_per_yrs) - 100, max(nation_suicides_per_yrs) + 100)
line, = ax.plot(0, 0)
animation = FuncAnimation(fig, func=anim, frames=60, interval=50, repeat=False)
plt.xticks([x for x in range(0, len(yrs), 5)], yrs[::5], fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel("Year", labelpad=25, fontsize=25)
plt.ylabel("Number of suicides", labelpad=50, fontsize=25)
plt.title(f"Suicides in {country} over the years", fontsize=30, pad=20)
animation = FuncAnimation(fig, func=anim, frames=50, interval=50, repeat=False)
mng = plt.get_current_fig_manager()
mng.resize(*mng.window.maxsize())
plt.show()
